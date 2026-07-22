from django.conf import settings
from django.db import models
from django.db.models import Q


class Organization(models.Model):
    """A tenant in Platonica's shared database.

    The primary key is the permanent internal identifier. ``slug`` is mutable and
    exists only for human-readable URLs; it is not an external identifier or an
    authorization boundary.
    """

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class OrganizationMembership(models.Model):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        STAFF = "staff", "Staff"

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organization_memberships",
    )
    role = models.CharField(max_length=5, choices=Role.choices, default=Role.STAFF)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "user"),
                name="unique_organization_membership",
            ),
            models.CheckConstraint(
                check=Q(role__in=("admin", "staff")),
                name="organization_membership_valid_role",
            ),
        ]

    def __str__(self):
        return f"{self.user} in {self.organization} ({self.role})"

