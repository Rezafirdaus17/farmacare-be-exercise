from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from pokemon.tests.factories import PokemonFactory


class PokemonListAPIViewTest(APITestCase):
    def test_success_get_list_of_pokemon(self):
        PokemonFactory.create_batch(5)

        response = self.client.get(reverse("pokemon:list-pokemon"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 5)
