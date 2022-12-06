from django.urls import path

from pokemon import (
    views as pokemon_view,
)

app_name = "pokemon"


urlpatterns = [
    path(
        "pokedex/",
        pokemon_view.pokedex_list_view,
        name="list-pokedex",
    ),
    path(
        "pokemon/",
        pokemon_view.PokemonListView.as_view(),
        name="list-pokemon",
    ),
    path(
        "matches/",
        pokemon_view.CreatePokemonMatchView.as_view(),
        name="create-pokemon-match",
    ),
    path(
        "matches/<uuid:uuid>/",
        pokemon_view.UpdatedPokemonMatchView.as_view(),
        name="update-pokemon-match",
    ),
    path(
        "pokemon-matches/",
        pokemon_view.PokemonMatchesListView.as_view(),
        name="create-pokemon-match",
    ),
]
