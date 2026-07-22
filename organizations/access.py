from django.core.exceptions import PermissionDenied

from .models import Organization, OrganizationMembership


def organizations_for_user(user):
    if not user.is_authenticated:
        return Organization.objects.none()
    return Organization.objects.filter(memberships__user=user)


def get_organization_for_user(user, organization_id):
    try:
        return organizations_for_user(user).get(id=organization_id)
    except Organization.DoesNotExist as error:
        raise PermissionDenied from error


def user_can_manage_organization(user, organization):
    if not user.is_authenticated:
        return False
    return OrganizationMembership.objects.filter(
        user=user,
        organization=organization,
        role=OrganizationMembership.Role.ADMIN,
    ).exists()

