from django.contrib.auth import get_user_model
from django.test import TestCase


class UserModelTests(TestCase):
    def test_configured_user_model_is_custom(self):
        self.assertEqual(get_user_model()._meta.label, "accounts.User")

