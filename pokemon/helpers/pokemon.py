from json import JSONDecodeError

from django.db import transaction
import requests

from pokemon import settings as app_settings
from pokemon.models import Pokemon


class PokemonException(Exception):
    pass


def fetcher_url(path, params=None):
    api_url = app_settings.POKEMON_API_BASE_URL + path

    json_response = None
    param = params if params else None
    response = requests.get(api_url, params=param)
    status_code = response.status_code
    if status_code == 200:
        try:
            json_response = response.json()
            if json_response == "Not found":
                status_code = 404
        except JSONDecodeError:
            status_code = 500

    if status_code == 404:
        raise PokemonException("URL not found")
    elif status_code >= 400 or status_code < 200:
        raise PokemonException("Error fetching product data")

    return json_response


def get_pokemon(path, params):
    return fetcher_url(path, params)


@transaction.atomic
def created_pokemon(data_results):
    existing_pokemon = Pokemon.objects.all().values_list("name", flat=True)

    bulk_pokemon = []
    for pokemon in data_results:
        if pokemon["name"] in existing_pokemon:
            continue

        bulk_pokemon.append(
            Pokemon(
                name=pokemon["name"].replace("-", " ").title(),
                slug=pokemon["name"],
                identifier=pokemon["url"].split("/")[6],
            )
        )
    Pokemon.objects.bulk_create(bulk_pokemon)
