from datetime import datetime, time

from django.db.models import Count, IntegerField, OuterRef, Subquery, Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from pokemon import settings as app_settings
from pokemon.helpers.pokemon import fetcher_url
from pokemon.models import Pokemon, PokemonArena, PokemonMatch
from pokemon.pagination import PokemonMatchPagination, PokemonPagination
from pokemon.serializers import (
    PokedexSerializer,
    PokemonArenaSerializers,
    PokemonMatchCreateSerializer,
    PokemonSerializer,
)


@api_view()
def pokedex_list_view(request):
    fetch_pokedex = fetcher_url(
        app_settings.URL_LIST_POKEDEX,
        params={"limit": app_settings.QUERY_LIMIT_POKEDEX},
    )

    pokedex_list = []
    for i in fetch_pokedex.get("results", []):
        get_pokemon = fetcher_url(app_settings.URL_LIST_POKEDEX + "/" + i["name"])

        i["stock_pokemon"] = len(get_pokemon.get("pokemon_entries"))

        pokedex_list.append(i)

    pokedex_list.sort(key=lambda x: x["name"])

    serializer = PokedexSerializer(pokedex_list, many=True)
    return Response(serializer.data)


class PokemonListView(generics.ListAPIView):
    serializer_class = PokemonSerializer
    pagination_class = PokemonPagination
    queryset = Pokemon.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["name"]

    def get_queryset(self):
        recommend = self.request.query_params.get("recommend")

        qs = self.queryset
        if recommend:
            count_matches = qs.annotate(match_sum=Count("matches")).filter(
                pk=OuterRef("pk")
            )
            count_score = qs.annotate(score_sum=Sum("matches__score")).filter(
                pk=OuterRef("pk")
            )
            qs = qs.annotate(
                total_match=Subquery(
                    count_matches.values("match_sum"), output_field=IntegerField()
                ),
                total_scores=Subquery(
                    count_score.values("score_sum"), output_field=IntegerField()
                ),
            ).order_by("-total_scores")

        return qs


class CreatePokemonMatchView(generics.CreateAPIView):
    serializer_class = PokemonMatchCreateSerializer
    queryset = PokemonMatch.objects.all()

    def get_data(self, data):
        create_arena = PokemonArena.objects.create()
        value = dict()

        for items in data:
            key = items["pokemon"]
            if key not in value:
                value[key] = items
            items["arena"] = create_arena.id

            if items["score"] > 5:
                raise serializers.ValidationError(
                    "Kamu hanya bisa memberi skor maximal 5."
                )

        data = list(value.values())
        if len(data) > 5:
            raise serializers.ValidationError(
                "Kamu hanya bisa membuat 5 pokemon dalam 1 pertandingan."
            )

        return data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=self.get_data(request.data), many=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class UpdatedPokemonMatchView(generics.CreateAPIView):
    serializer_class = PokemonMatchCreateSerializer
    queryset = PokemonMatch.objects.all()

    def get_arena(self):
        return get_object_or_404(PokemonArena, uuid=str(self.kwargs["uuid"]))

    def create(self, request, *args, **kwargs):
        data = request.data
        match_result = PokemonMatch.objects.filter(
            arena=self.get_arena(), pokemon__slug=data["pokemon"]
        )

        if not match_result:
            raise serializers.ValidationError("Pokemon tidak ditemukan dalam pertandingan ini.")

        if data["score"] > 5:
            raise serializers.ValidationError("Kamu hanya bisa memberi skor maximal 5.")

        if match_result:
            match_result.update(
                score=data["score"], is_win=data.get("winner", False), updated_at=datetime.now()
            )
            return Response(status=status.HTTP_204_NO_CONTENT)


class PokemonMatchesListView(generics.ListAPIView):
    serializer_class = PokemonArenaSerializers
    pagination_class = PokemonMatchPagination
    queryset = PokemonArena.objects.all().order_by("-created_at")

    def get_queryset(self):
        uuid = self.request.query_params.get("uuid")
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        qs = self.queryset
        if uuid:
            qs = qs.filter(uuid=str(uuid))

        if start_date and end_date:
            from_date = datetime.combine(
                datetime.strptime(start_date, "%Y-%m-%d"), time.min
            )
            to_date = datetime.combine(
                datetime.strptime(end_date, "%Y-%m-%d"), time.max
            )
            qs = qs.filter(created_at__range=(from_date, to_date))

        return qs
