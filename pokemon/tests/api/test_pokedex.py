from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class PokedexListAPIViewTest(APITestCase):
    def test_success_get_list_of_pokedex(self):
        response = self.client.get(reverse("pokemon:list-pokedex"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
