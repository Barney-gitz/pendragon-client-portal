# ADR-006: Equipment-Centred Domain Model

## Status

Accepted

## Context

Pendragon work is ultimately centred around individual machines identified by serial number.

A single customer job may contain one or more machines. Each machine can have its own work type, technician, status, jobsheet entries, files, and history.

Pendragon confirmed that each machine has its own jobsheet. Jobsheets are not shared across multiple machines.

## Decision

We will model equipment as the primary long-lived business entity.

Service jobs represent the overall customer work order or visit.

Service job items represent individual machines within that job.

Jobsheet entries, generated jobsheets, attachments, and item-level history should belong to the service job item wherever possible.

This allows the application to show a complete history for a specific serial number, including:

- All jobs involving that serial number
- A preview of that machine's history from each job
- Jobsheet entries
- Generated jobsheets
- Attached files
- Status and history events

## Consequences

The backend can support both simple and complex workflows.

For a single-machine job, the user interface can remain simple and feel similar to the current Workshop Tracker.

For multi-machine jobs, staff can update each machine individually or use bulk actions where appropriate.

The trade-off is that more logic moves to the `ServiceJobItem` level rather than the `ServiceJob` level. This is acceptable because it better reflects how Pendragon actually works.