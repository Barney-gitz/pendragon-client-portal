# ADR-004: Authentication and Account Lifecycle

## Status

Accepted

## Context

Pendragon Client Portal needs secure customer and staff authentication.

Users should not self-register freely. Access should begin from a Pendragon-controlled invitation so that every user is attached to the correct company and role.

The portal also needs password reset, MFA, account activation, auditability, and protection against common authentication attacks.

## Decision

We will use an invitation-based account lifecycle.

The planned flow is:

1. A Pendragon admin creates or selects a company.
2. A Pendragon admin invites a user by email.
3. The system creates a single-use invitation token.
4. The user receives an invitation email.
5. The user clicks the invite link.
6. The user sets a password.
7. The user account is activated.
8. The user is prompted to configure authenticator app MFA.
9. The user logs in using a secure server-side session cookie.

The invite token also confirms the user's email address because the invitation is delivered to that email account.

## Authentication Strategy

Passwords will never be stored directly.

Password hashes will be stored using a strong password hashing algorithm such as Argon2 or bcrypt.

Invitation and password reset tokens will also not be stored directly. The application will store only hashed token values.

Sessions will be stored server-side and referenced by secure HTTP-only cookies.

MFA will use authenticator apps using time-based one-time passwords.

SMS MFA is out of scope for the initial version.

Email MFA is not preferred because compromise of the email account may allow both password reset and MFA access.

## Account States

A user may be:

- Invited
- Active
- Disabled
- Locked

Users are not deleted as part of normal operation. They are disabled so audit history and service history remain intact.

## Security Considerations

The system must support:

- Unique email addresses
- Lowercase email normalization
- Strong password hashing
- Single-use invitation tokens
- Invitation expiry
- Password reset expiry
- Failed login tracking
- Account lockout
- Audit logging for security-sensitive actions
- MFA reset by authorized administrators only

Sensitive values such as passwords, invitation tokens, reset tokens, MFA secrets, and backup codes must not be stored in plaintext.

Names and email addresses are not hashed because the application needs to display, search, invite, and email users. They are protected through authorization, HTTPS, database permissions, and careful logging.

## Consequences

This approach is more complex than simple username/password login, but it better matches a commercial customer portal.

It prevents uncontrolled self-registration and ensures every customer user belongs to the correct company from the start.

It also gives us a clear foundation for MFA, password reset, audit logs, and admin account management.