from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer


RECIPES_URL = reverse('recipe:recipe-list')


def sample_recipe(user, **params):
    """
    Create and return a sample recipe
    """
    defaults ={
        'title': 'Sample recipe',
        'time_minutes': 10,
        'price': 5.00
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeApiTests(TestCase):
    """
    Test unauthenticated recipe API access
    """
    def setUp(self):
        self.client = APIClient()
    
    def test_auth_required(self):
        """
        Test that authentication is required
        """
        resp = self.client.get(RECIPES_URL)

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """
    Test authenticated user recipe api tests
    """
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@domain.tld',
            'testpassword',
        )
        self.client.force_authenticate(self.user)
    
    def test_retrieve_recipse(self):
        """
        Test retrieving list of recipes
        """
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        resp = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serializer.data)
    
    def test_recipes_limited_to_user(self):
        """
        Test retrieving recipes for user
        """
        user2 = get_user_model().objects.create_user(
            'other@domain.tld',
            'password123'
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        resp = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data, serializer.data)
