from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from api.authentication import jwt_token_generator  # Update the path if different


class BaseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        tokens = jwt_token_generator.make_tokens(self.user)
        self.access_token = tokens.access
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {self.access_token}")
