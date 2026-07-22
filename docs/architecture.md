# Architecture

Platonica is a hosted multi-tenant Django application using one PostgreSQL
database. The initial implementation is a modular monolith. Internal boundaries
should remain clean so later capabilities can be added without introducing a
repository framework, granular permission system, public API, domain-event
infrastructure, or background-job system now.

## Tenant identity and authorization

`Organization.id` is the permanent internal identifier for an organization.
`Organization.slug` is mutable and exists only to make human-readable URLs. A
slug must not be used as an external-system identifier or as an authorization
boundary.

Access is established through `OrganizationMembership`. An `admin` membership
may manage organization settings and memberships. A `staff` membership has
ordinary organization access. No granular permission system is part of V1.

Tenant authorization uses small plain functions in `organizations/access.py`.
Tenant-owned records must be reached through a membership-scoped query rather
than an unrestricted lookup based on an ID or slug supplied by a user.
