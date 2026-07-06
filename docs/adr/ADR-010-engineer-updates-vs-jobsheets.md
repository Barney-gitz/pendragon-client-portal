# ADR-010: Separate Engineer Updates from Jobsheets

## Status

Accepted

## Context

During a repair, engineers need to record observations as work progresses.

These notes are informal, technical and primarily intended for internal engineering use.

At the completion of a repair, a professional repair summary may be required for the customer.

These two purposes have different audiences and should not share the same data model.

## Decision

Engineer Updates and Jobsheets are separate concepts.

### Engineer Updates

Engineer Updates represent informal notes recorded throughout a repair.

Examples include:

- PSU output unstable.
- Suspect failed regulator.
- Replacement board fitted.
- Calibration running.

Engineer Updates are internal only.

They form part of the engineering record for the repair.

### Jobsheets

Jobsheets represent the official repair summary.

Jobsheets are written after the repair has been completed.

They are professional in tone and may be provided directly to customers.

Jobsheets may reference information contained within Engineer Updates but remain independent records.

## Consequences

Advantages

- Engineers can record information naturally during repairs.
- Customer-facing documentation remains professional.
- Future AI summarisation becomes possible.
- Machine history can be built from meaningful engineering information.

Trade-offs

- Some information may exist in both Engineer Updates and Jobsheets.
- The application must clearly distinguish internal and customer-facing records.