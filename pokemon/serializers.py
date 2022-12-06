from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import transaction
from rest_framework import serializers

from pokemon.models import Pokemon, PokemonMatch


class SimplePokemonMatchSerializer(serializers.ModelSerializer):
    pokemon = serializers.CharField(source="pokemon.name")

    class Meta:
        model = PokemonMatch
        fields = [
            "uuid",
            "pokemon",
            "score",
        ]


class PokedexSerializer(serializers.Serializer):
    pokedex_name = serializers.SerializerMethodField()
    slug = serializers.CharField(source="name")
    stock_pokemon = serializers.IntegerField()

    def get_pokedex_name(self, obj):
        name = obj.get("name").replace("-", " ").title()
        return name


class PokemonSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    slug = serializers.CharField(read_only=True)
    identifier = serializers.IntegerField(read_only=True)
    total_match = serializers.IntegerField(read_only=True)
    total_scores = serializers.IntegerField(read_only=True)

    class Meta:
        model = Pokemon
        fields = (
            "name",
            "slug",
            "identifier",
            "total_match",
            "total_scores",
            "created_at",
        )


class PokemonMatchCreateSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField(read_only=True)
    pokemon = serializers.SlugRelatedField(
        slug_field="slug", queryset=Pokemon.objects.all(), allow_null=True
    )
    score = serializers.DecimalField(
        required=False,
        default=0.0,
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )

    class Meta:
        model = PokemonMatch
        fields = [
            "uuid",
            "pokemon",
            "arena",
            "score",
            "is_win",
            "created_at",
            "updated_at",
        ]

    @transaction.atomic
    def create(self, validated_data):
        return super().create(validated_data)


class PokemonArenaSerializers(serializers.ModelSerializer):
    pokemons = SimplePokemonMatchSerializer(many=True, source="arenas")

    class Meta:
        model = PokemonMatch
        fields = [
            "uuid",
            "pokemons",
            "created_at",
        ]
