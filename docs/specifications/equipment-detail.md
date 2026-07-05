# Equipment Detail

## Status

Draft

---

# Purpose

The Equipment Detail page is intended to become the primary view of an individual piece of equipment throughout its lifetime.

Unlike service jobs, which are temporary containers for work, equipment exists for many years.

The equipment page should allow Pendragon staff and customers to understand everything that has happened to a specific serial number.

---

# Business Goals

The page should answer five questions.

## 1. What is this equipment?

Display:

- Make
- Model
- Serial Number
- Company
- Primary Contact

---

## 2. Where is it now?

If the equipment is currently on an active job display:

- Current Job
- Current Status
- Assigned Engineer
- Location (Workshop / On Site)

---

## 3. What has happened to it before?

Display a chronological history of all previous work involving this serial number.

Each entry should provide a summary of:

- Job Number
- Job Type
- Date
- Outcome

---

## 4. Can I access previous work?

Each historical job should expose:

- Jobsheet
- Repair Report
- Calibration Certificate
- Photographs
- Other attached documents

---

## 5. Does this equipment have recurring issues?

The page should eventually highlight useful insights such as:

- Repeat repairs
- Repeat faults
- Frequent calibrations
- Warranty history

This is a future enhancement.

---

# Domain Model

Equipment is the primary long-lived entity.

```
Equipment
    │
    ├── Service Job Item
    │      ├── Timeline
    │      ├── Jobsheet Entries
    │      ├── Documents
    │      └── Status History
    │
    └── Service Job
```

Service Jobs organise customer work.

Service Job Items represent work performed on a specific machine.

---

# Design Principles

- Equipment history should always be centred around the serial number.
- Every jobsheet belongs to one machine.
- Every generated jobsheet should be reproducible from database data.
- Documents should be attached to machines rather than only to jobs.
- Staff should only see the information required to perform today's work.

---

# Planned API Evolution

## Version 1

GET /equipment/{id}

Returns equipment details.

---

## Version 2

Returns equipment details plus previous jobs.

---

## Version 3

Returns current active job.

---

## Version 4

Returns document summaries.

---

## Version 5

Returns equipment insights and analytics.

---

# Notes

The existing Pendragon Workshop Tracker has demonstrated that technicians work most effectively when interacting with individual machines rather than large, complex jobs.

The new Client Portal should preserve this simplicity while supporting multi-machine customer jobs through Service Job Items.