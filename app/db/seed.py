from app.db.session import SessionLocal
from app.models.company import Company
from app.models.equipment import Equipment
from datetime import datetime, timezone
import re
from app.models.service_job import (
    JobStatus,
    JobType,
    ServiceJob,
)
from app.models.user import User, UserRole
from app.models.service_job_item import ServiceJobItem


def seed_companies(session):
    company_names = [
        "Pendragon Ltd",
        "University of Oxford",
        "NHS Bristol",
        "BioLab Ltd",
    ]

    for name in company_names:
        existing_company = session.query(Company).filter_by(name=name).first()

        if existing_company is None:
            session.add(Company(name=name, is_active=True))

    session.commit()


def get_company(session, name: str) -> Company:
    return session.query(Company).filter_by(name=name).one()


def get_user(session, email: str) -> User:
    return session.query(User).filter_by(email=email.lower()).one()


def get_equipment(session, serial_number: str) -> Equipment:
    return session.query(Equipment).filter_by(serial_number=serial_number).one()


def get_service_job(session, reference_number: str) -> ServiceJob:
    return (
        session.query(ServiceJob)
        .filter_by(reference_number=reference_number)
        .one()
    )


def generate_sir(started_at: datetime, engineer: User, equipment: Equipment) -> str:
    date_part = started_at.strftime("%d%m%y")
    cleaned_serial = re.sub(r"[^A-Za-z0-9]", "", equipment.serial_number)
    serial_suffix = cleaned_serial[-4:]

    return f"{date_part}{engineer.sir_initials}{serial_suffix}"


def seed_users(session):
    pendragon = get_company(session, "Pendragon Ltd")
    oxford = get_company(session, "University of Oxford")
    nhs = get_company(session, "NHS Bristol")
    biolab = get_company(session, "BioLab Ltd")

    users = [
        (
            "Adam",
            "Johns",
            "adamjohns2006@icloud.com",
            "Software Developer",
            "AJ",
            UserRole.PENDRAGON_ADMIN,
            pendragon,
        ),
        (
            "Rachael",
            "Johns",
            "rachael@pendragonscientific.com",
            "Director",
            "RJ",
            UserRole.PENDRAGON_ADMIN,
            pendragon,
        ),
        (
            "Caroline",
            "Jones",
            "caroline@pendragonscientific.com",
            "Quality Manager",
            "CJ",
            UserRole.PENDRAGON_ADMIN,
            pendragon,
        ),
        (
            "Richard",
            "Johns",
            "richard@pendragonscientific.com",
            "Director",
            "RJH",
            UserRole.PENDRAGON_MANAGER,
            pendragon,
        ),
        (
            "Remi",
            "Guest",
            "remi@pendragonscientific.com",
            "Workshop Manager",
            "RG",
            UserRole.PENDRAGON_MANAGER,
            pendragon,
        ),
        (
            "Russell",
            "Page",
            "russell@pendragonscientific.com",
            "Field Service Engineer",
            "RP",
            UserRole.PENDRAGON_ENGINEER,
            pendragon,
        ),
        (
            "Jake",
            "Simons",
            "jake@pendragonscientific.com",
            "Field Service Engineer",
            "JS",
            UserRole.PENDRAGON_ENGINEER,
            pendragon,
        ),
        (
            "Sarah",
            "Ostler",
            "sarah@pendragonscientific.com",
            "Office Administrator",
            "SO",
            UserRole.PENDRAGON_OFFICE_ADMIN,
            pendragon,
        ),
        (
            "Ashleigh",
            "Skinner",
            "ashleigh@pendragonscientific.com",
            "Office Manager",
            "AS",
            UserRole.PENDRAGON_OFFICE_ADMIN,
            pendragon,
        ),
        (
            "John",
            "Williams",
            "john.williams@oxford.example.com",
            "Laboratory Manager",
            "JW",
            UserRole.CUSTOMER_USER,
            oxford,
        ),
        (
            "Emily",
            "Carter",
            "emily.carter@oxford.example.com",
            "Senior Technician",
            "EC",
            UserRole.CUSTOMER_USER,
            oxford,
        ),
        (
            "Sarah",
            "Collins",
            "sarah.collins@nhsbristol.example.com",
            "Biomedical Engineer",
            "SC",
            UserRole.CUSTOMER_USER,
            nhs,
        ),
        (
            "Daniel",
            "Green",
            "daniel.green@nhsbristol.example.com",
            "Laboratory Supervisor",
            "DG",
            UserRole.CUSTOMER_USER,
            nhs,
        ),
        (
            "Lisa",
            "Turner",
            "lisa.turner@biolab.example.com",
            "Research Scientist",
            "LT",
            UserRole.CUSTOMER_USER,
            biolab,
        ),
        (
            "Michael",
            "Harris",
            "michael.harris@biolab.example.com",
            "Laboratory Manager",
            "MH",
            UserRole.CUSTOMER_USER,
            biolab,
        ),
    ]

    for (
        first_name,
        last_name,
        email,
        job_title,
        sir_initials,
        role,
        company,
    ) in users:
        existing_user = session.query(User).filter_by(email=email).first()

        if existing_user is None:
            session.add(
                User(
                    first_name=first_name,
                    last_name=last_name,
                    email=email.lower(),
                    job_title=job_title,
                    sir_initials=sir_initials,
                    role=role,
                    company_id=company.id,
                    is_active=True,
                )
            )

    session.commit()


def seed_equipment(session):
    equipment = [
        (
            "University of Oxford",
            "john.williams@oxford.example.com",
            "Thermo Scientific",
            "Sorvall ST8",
            "TS-10293",
        ),
        (
            "University of Oxford",
            "emily.carter@oxford.example.com",
            "Eppendorf",
            "5810R",
            "EP-5810-42",
        ),
        (
            "University of Oxford",
            "john.williams@oxford.example.com",
            "Sartorius",
            "Cubis II",
            "SA-78213",
        ),
        (
            "NHS Bristol",
            "sarah.collins@nhsbristol.example.com",
            "Mettler Toledo",
            "XPR204",
            "MT-22091",
        ),
        (
            "NHS Bristol",
            "daniel.green@nhsbristol.example.com",
            "Binder",
            "BD56",
            "BD-55671",
        ),
        (
            "BioLab Ltd",
            "lisa.turner@biolab.example.com",
            "Leica",
            "CM1950",
            "LC-88342",
        ),
        (
            "BioLab Ltd",
            "michael.harris@biolab.example.com",
            "Thermo Scientific",
            "Heracell VIOS",
            "HV-77419",
        ),
    ]

    for company_name, email, make, model, serial in equipment:
        existing = session.query(Equipment).filter_by(serial_number=serial).first()

        if existing:
            continue

        company = get_company(session, company_name)

        contact = session.query(User).filter_by(email=email).one()

        session.add(
            Equipment(
                company_id=company.id,
                primary_contact_user_id=contact.id,
                make=make,
                model=model,
                serial_number=serial,
                is_active=True,
            )
        )

    session.commit()


def seed_service_jobs(session):
    jobs = [
        (
            "University of Oxford",
            "JOB-2026-0001",
            JobType.ONSITE_SERVICE,
            JobStatus.COMPLETED,
            "Annual preventative maintenance visit.",
        ),
        (
            "NHS Bristol",
            "JOB-2026-0002",
            JobType.WORKSHOP_REPAIR,
            JobStatus.WAITING_FOR_PARTS,
            "Temperature instability reported.",
        ),
        (
            "BioLab Ltd",
            "JOB-2026-0003",
            JobType.ONSITE_CALIBRATION,
            JobStatus.AWAITING_CUSTOMER_APPROVAL,
            "Annual calibration visit.",
        ),
    ]

    for company_name, reference, job_type, status, description in jobs:
        existing = (
            session.query(ServiceJob)
            .filter_by(reference_number=reference)
            .first()
        )

        if existing:
            continue

        company = get_company(session, company_name)

        session.add(
            ServiceJob(
                company_id=company.id,
                reference_number=reference,
                job_type=job_type,
                status=status,
                description=description,
                is_active=True,
            )
        )

    session.commit()


def seed_service_job_items(session):
    started_at = datetime(2026, 7, 2, 9, 0, tzinfo=timezone.utc)
    completed_at = datetime(2026, 7, 2, 16, 30, tzinfo=timezone.utc)

    items = [
        (
            "JOB-2026-0001",
            "TS-10293",
            "john.williams@oxford.example.com",
            "jake@pendragonscientific.com",
            started_at,
            completed_at,
        ),
        (
            "JOB-2026-0001",
            "EP-5810-42",
            "emily.carter@oxford.example.com",
            "jake@pendragonscientific.com",
            started_at,
            completed_at,
        ),
        (
            "JOB-2026-0001",
            "SA-78213",
            "john.williams@oxford.example.com",
            "russell@pendragonscientific.com",
            started_at,
            completed_at,
        ),
        (
            "JOB-2026-0002",
            "BD-55671",
            "daniel.green@nhsbristol.example.com",
            "russell@pendragonscientific.com",
            datetime(2026, 7, 10, 10, 0, tzinfo=timezone.utc),
            None,
        ),
        (
            "JOB-2026-0003",
            "LC-88342",
            "lisa.turner@biolab.example.com",
            None,
            None,
            None,
        ),
    ]

    for (
        reference_number,
        serial_number,
        contact_email,
        engineer_email,
        item_started_at,
        item_completed_at,
    ) in items:
        service_job = get_service_job(session, reference_number)
        equipment = get_equipment(session, serial_number)
        contact_user = get_user(session, contact_email)

        existing = (
            session.query(ServiceJobItem)
            .filter_by(
                service_job_id=service_job.id,
                equipment_id=equipment.id,
            )
            .first()
        )

        if existing:
            continue

        assigned_engineer = (
            get_user(session, engineer_email)
            if engineer_email is not None
            else None
        )

        sir_number = (
            generate_sir(item_started_at, assigned_engineer, equipment)
            if item_started_at is not None and assigned_engineer is not None
            else None
        )

        session.add(
            ServiceJobItem(
                service_job_id=service_job.id,
                equipment_id=equipment.id,
                contact_user_id=contact_user.id,
                assigned_engineer_id=(
                    assigned_engineer.id if assigned_engineer is not None else None
                ),
                sir_number=sir_number,
                started_at=item_started_at,
                completed_at=item_completed_at,
            )
        )

    session.commit()


def main():
    session = SessionLocal()

    try:
        seed_companies(session)
        seed_users(session)
        seed_equipment(session)
        seed_service_jobs(session)
        seed_service_job_items(session)
    finally:
        session.close()


if __name__ == "__main__":
    main()