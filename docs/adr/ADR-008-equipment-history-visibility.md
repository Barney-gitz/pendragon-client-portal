# ADR-008: Equipment History Visibility

## Status

Accepted

## Context

One of the primary selling points of the Pendragon Client Portal is the ability to retrieve the complete lifetime history of any machine using its serial number.

Equipment history serves two distinct audiences:

- Pendragon staff
- Customers

These audiences have different requirements.

Engineers require a complete diagnostic record to understand previous faults, repairs, engineer actions, fitted parts, and historical context.

Customers require visibility of completed work carried out on their equipment, but should not have access to internal operational notes or sensitive information.

## Decision

Equipment history will be treated as an event stream representing the lifetime of a machine.

Every event recorded against a machine will be considered part of its permanent history.

Each event will carry a visibility classification.

Examples include:

- Internal only
- Customer visible

The staff history endpoint will return every event.

Future customer-facing endpoints will return only events explicitly marked as customer visible.

## Consequences

Advantages:

- Engineers have access to the complete diagnostic history of every machine.
- Customers receive an appropriate service history without exposing internal discussions.
- Additional event types (jobsheets, labour, files, PDFs, quotations, engineer notes, status changes, etc.) can be added without redesigning the API.
- The history model becomes a long-term read model for the entire lifetime of a machine.

Trade-offs:

- Every new history event type must define its visibility.
- Customer APIs must filter events appropriately.
- Internal notes remain protected by design rather than by convention.

## Future Work

Future event types are expected to include:

- Status changes
- Timeline events
- Jobsheet entries
- Labour records
- Parts fitted
- Uploaded files
- Generated PDFs
- Customer approvals
- Quotations
- Engineer notes
- Site visits
- Calibration certificates