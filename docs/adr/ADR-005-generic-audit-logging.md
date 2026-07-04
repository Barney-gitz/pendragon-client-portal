# ADR-005: Generic Audit Logging

## Status

Accepted

## Context

Pendragon needs a reliable way to record important changes made across the system.

Examples include:

- Service job creation
- Service job status changes
- Equipment updates
- Invitation acceptance
- User role changes
- Future document uploads and downloads

This information is useful for support, security, compliance, debugging, and customer accountability.

Pendragon already has a service job timeline, but that serves a different purpose. The timeline tells the business story of a service job. Audit logging tells the system story of who changed what and when.

## Decision

We will implement a generic `audit_logs` table.

The audit log will record:

- The user who performed the action
- The entity type affected
- The entity ID affected
- The action performed
- Previous values where relevant
- New values where relevant
- Timestamp

We will use one reusable audit logging service rather than creating separate audit tables for each feature.

## Consequences

This gives Pendragon a consistent auditing approach across the whole platform.

It also makes future admin filtering straightforward by:

- Actor
- Entity type
- Entity ID
- Action
- Date range

The trade-off is that `old_values` and `new_values` are generic structured data rather than strongly typed columns. This is acceptable because audit logs are primarily used for traceability, investigation, and reporting rather than core transactional workflows.

## Alternatives Considered

### Separate audit tables per feature

Rejected because it would duplicate logic, create inconsistent schemas, and make cross-system auditing harder.

### Only using service job timelines

Rejected because timelines and audit logs serve different purposes. Timeline events are business-facing workflow history. Audit logs are internal system records.

### External logging only

Rejected because application logs are not a reliable substitute for structured, queryable business audit records stored in the database.