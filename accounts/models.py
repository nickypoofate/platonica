from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Platonica user; intentionally retains Django's standard authentication fields."""

