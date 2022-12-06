import factory

from pokemon.models import Pokemon


class PokemonFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    slug = factory.Faker("slug")
    identifier = 2

    class Meta:
        model = Pokemon
