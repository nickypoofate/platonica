from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.test import TestCase

from organizations.access import (
    get_organization_for_user,
    organizations_for_user,
    user_can_manage_organization,
)
from organizations.models import Organization, OrganizationMembership


class OrganizationAccessTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.admin_user = user_model.objects.create_user(username="admin-member")
        self.staff_user = user_model.objects.create_user(username="staff-member")
        self.outsider = user_model.objects.create_user(username="outsider")
        self.first = Organization.objects.create(name="First", slug="first")
        self.second = Organization.objects.create(name="Second", slug="second")
        OrganizationMembership.objects.create(
            organization=self.first,
            user=self.admin_user,
            role=OrganizationMembership.Role.ADMIN,
        )
        OrganizationMembership.objects.create(
            organization=self.first,
            user=self.staff_user,
            role=OrganizationMembership.Role.STAFF,
        )
        OrganizationMembership.objects.create(
            organization=self.second,
            user=self.outsider,
            role=OrganizationMembership.Role.ADMIN,
        )

    def test_user_only_lists_their_organizations(self):
        self.assertQuerySetEqual(
            organizations_for_user(self.staff_user),
            [self.first],
        )

    def test_member_can_resolve_their_organization_by_permanent_id(self):
        result = get_organization_for_user(self.staff_user, self.first.id)
        self.assertEqual(result, self.first)

    def test_member_cannot_resolve_another_organization(self):
        with self.assertRaises(PermissionDenied):
            get_organization_for_user(self.staff_user, self.second.id)

    def test_outsider_cannot_resolve_organization(self):
        with self.assertRaises(PermissionDenied):
            get_organization_for_user(self.outsider, self.first.id)

    def test_anonymous_user_has_no_organization_access(self):
        from django.contrib.auth.models import AnonymousUser

        self.assertFalse(organizations_for_user(AnonymousUser()).exists())

    def test_admin_member_can_manage_organization(self):
        self.assertTrue(user_can_manage_organization(self.admin_user, self.first))

    def test_staff_member_cannot_manage_organization(self):
        self.assertFalse(user_can_manage_organization(self.staff_user, self.first))

    def test_admin_role_does_not_cross_organization_boundary(self):
        self.assertFalse(user_can_manage_organization(self.admin_user, self.second))

