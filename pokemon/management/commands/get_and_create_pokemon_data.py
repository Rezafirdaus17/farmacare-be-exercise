from urllib.parse import parse_qs, urlparse

from django.core.management import BaseCommand

from pokemon import settings as apps_settings
from pokemon.helpers.pokemon import created_pokemon, get_pokemon


class Command(BaseCommand):
    help = "Get And Create All Data Of Pokemon"

    def handle(self, *args, **options):
        offset = apps_settings.QUERY_OFFSET_POKEMON
        while offset:
            offsets = int(offset) - 1
            pokemon = get_pokemon(
                apps_settings.URL_LIST_POKEMON,
                params={
                    "offset": str(offsets) if not offsets else str(offset),
                    "limit": apps_settings.QUERY_LIMIT_POKEMON,
                },
            )

            # Query save in here
            created_pokemon(pokemon.get("results", []))

            if pokemon.get("next"):
                parsed_url = urlparse(pokemon["next"])
                offset = parse_qs(parsed_url.query)["offset"][0]
            else:
                offset = None
