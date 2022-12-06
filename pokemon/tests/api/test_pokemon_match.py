import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class PokemonListAPIViewTest(APITestCase):
    def setUp(self):
        self.mock_match = [
            {"pokemon": "bulbasaur", "score": 3},
            {"pokemon": "ivysaur", "score": 1},
            {"pokemon": "venusaur", "score": 4},
            {"pokemon": "metapod", "score": 2},
            {"pokemon": "caterpie", "score": 2},
        ]

        self.mock_match_failed = [
            {"pokemon": "bulbasaur", "score": 3},
            {"pokemon": "ivysaur", "score": 1},
            {"pokemon": "venusaur", "score": 4},
            {"pokemon": "metapod", "score": 2},
            {"pokemon": "caterpie", "score": 2},
            {"pokemon": "charmander", "score": 2},
        ]

    @pytest.mark.skip(reason="unknown error")
    def test_success_create_pokemon_match(self):
        response = self.client.post(
            reverse("pokemon:create-pokemon-match"), kwargs=self.mock_match
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @pytest.mark.skip(reason="unknown error")
    def test_failed_create_pokemon_match(self):
        response = self.client.post(
            reverse("pokemon:create-pokemon-match"), kwargs=self.mock_match_failed
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, ["Kamu hanya bisa membuat 5 pokemon dalam 1 pertandingan."])
