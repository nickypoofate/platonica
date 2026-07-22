2026-07-22

We use iframe embeds.

Reason:
Keeps organizations on their own websites.

Contacts are created from Orders.

Reason:
Orders are primary.

Stripe Connect Standard.

Reason:
Organizations own payouts.

V1 decisions:

1. Platonica is a hosted multi-tenant SaaS using one PostgreSQL database.
2. Organizations may have multiple staff users, but detailed role design can wait.
3. One order may contain multiple ticket types.
4. Each purchased admission produces its own independently scannable ticket.
5. V1 records the purchaser as a Contact. Individual attendee names are not required.
6. Stripe webhooks are authoritative for payment completion and refunds.
7. The scanner is browser-based and online-only in V1.
8. Essential transactional email is included.
9. Offline scanning, ticket transfers, discounts, multi-currency, custom checkout fields, and bespoke tax behavior are out of scope unless separately approved.

Organization identity and access:

- `Organization.id` is the permanent internal identifier.
- `Organization.slug` is mutable and is used only for human-readable URLs. It is not an external-system identifier or an authorization boundary.
- Organization memberships have only two roles: `admin` and `staff`.
- Admins may manage organization settings and memberships. Staff have ordinary organization access.
- V1 does not include a granular permission system.
