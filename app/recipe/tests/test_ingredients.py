from urllib import response
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that an unauthorized user cannot get list"""
        response = self.client.get(INGREDIENTS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PriveIngredientsApiTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test@gmail.com",
            "password123"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='Orange')

        res = self.client.get(INGREDIENTS_URL)

        tags = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tags returned are for authenticated user"""
        user2 = get_user_model().objects.create_user(
            'other@londonappdev.com',
            'testpass'
        )
        Ingredient.objects.create(user=user2, name='Salt')
        tag = Ingredient.objects.create(user=self.user, name='Pepper')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_ingredient_successful(self):
        """Test creating a new ingredient"""
        payload = {'name': 'Potato'}
        self.client.post(INGREDIENTS_URL, payload)

        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """Test creating a new ingredient with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
