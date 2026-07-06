# ADR-009: Separate Machine History from Job Timeline

## Status

Accepted

## Context

Pendragon Scientific services equipment over many years. A single machine may be repaired dozens of times across multiple service jobs.

Two distinct questions exist:

1. "What has happened to this machine throughout its life?"
2. "What happened during this repair?"

These questions require different levels of detail.

Attempting to answer both using a single timeline would produce an interface that is either too noisy for diagnosis or too limited for repair management.

## Decision

The application will maintain two separate timelines.

### Machine History

Machine History represents the permanent engineering record of a serial-numbered machine.

It is intended to provide engineers with a concise overview of previous faults, repairs and significant engineering events.

Machine History is diagnostic.

Typical events include:

- Machine logged
- Repair completed
- Major part fitted
- Calibration completed
- Certificate issued
- Returned to customer

Machine History deliberately excludes operational workflow events.

### Job Timeline

Each Service Job Item maintains its own Job Timeline.

The Job Timeline records the detailed workflow of a repair.

Typical events include:

- Status changes
- Engineer assignments
- Internal notes
- Waiting for parts
- Parts received
- File uploads
- Jobsheet updates

The Job Timeline represents everything that occurred during that repair.

## Consequences

Advantages

- Engineers can quickly understand the history of a machine.
- Diagnostic information remains concise.
- Workflow detail is preserved without cluttering machine history.
- Future event types can be added independently.

Trade-offs

- Some information exists in both contexts.
- History builders must decide whether an event is diagnostic or operational.
- APIs remain intentionally separate.

## Future Work

Machine History will become the primary search experience when locating equipment by serial number.

Job Timeline will remain the detailed engineering record for each repair.