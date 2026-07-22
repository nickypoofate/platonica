from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase

from organizations.models import Organization, OrganizationMembership


class OrganizationModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="member")
        self.organization = Organization.objects.create(name="Example", slug="example")

    def test_slug_can_change_without_changing_permanent_id(self):
        organization_id = self.organization.id
        self.organization.slug = "renamed"
        self.organization.save()
        self.assertEqual(self.organization.id, organization_id)

    def test_membership_defaults_to_staff(self):
        membership = OrganizationMembership.objects.create(
            organization=self.organization,
            user=self.user,
        )
        self.assertEqual(membership.role, OrganizationMembership.Role.STAFF)

    def test_duplicate_membership_is_rejected(self):
        OrganizationMembership.objects.create(
            organization=self.organization,
            user=self.user,
        )
        with self.assertRaises(IntegrityError), transaction.atomic():
            OrganizationMembership.objects.create(
                organization=self.organization,
                user=self.user,
            )

    def test_role_outside_admin_and_staff_is_rejected(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            OrganizationMembership.objects.create(
                organization=self.organization,
                user=self.user,
                role="owner",
            )

