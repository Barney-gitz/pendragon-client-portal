from app.db.session import SessionLocal
from app.models.company import Company
from app.models.equipment import Equipment
from app.models.user import User, UserRole
from app.models.service_job import (
    JobStatus,
    JobType,
    ServiceJob,
)


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


def seed_users(session):
    pendragon = get_company(session, "Pendragon Ltd")
    oxford = get_company(session, "University of Oxford")
    nhs = get_company(session, "NHS Bristol")
    biolab = get_company(session, "BioLab Ltd")

    users = [
        ("Adam", "Admin", "adam@pendragon.co.uk", UserRole.PENDRAGON_ADMIN, pendragon),
        ("Rachael", "Admin", "rachael@pendragon.co.uk", UserRole.PENDRAGON_ADMIN, pendragon),
        ("Caroline", "Admin", "caroline@pendragon.co.uk", UserRole.PENDRAGON_ADMIN, pendragon),
        ("Richard", "Manager", "richard@pendragon.co.uk", UserRole.PENDRAGON_MANAGER, pendragon),
        ("Remi", "Manager", "remi@pendragon.co.uk", UserRole.PENDRAGON_MANAGER, pendragon),
        ("Jake", "Engineer", "jake@pendragon.co.uk", UserRole.PENDRAGON_ENGINEER, pendragon),
        ("Russell", "Engineer", "russell@pendragon.co.uk", UserRole.PENDRAGON_ENGINEER, pendragon),
        ("Sarah", "Office", "sarah@pendragon.co.uk", UserRole.PENDRAGON_OFFICE_ADMIN, pendragon),
        ("Ashleigh", "Office", "ashleigh@pendragon.co.uk", UserRole.PENDRAGON_OFFICE_ADMIN, pendragon),

        ("John", "Williams", "john.williams@oxford.example.com", UserRole.CUSTOMER_USER, oxford),
        ("Emily", "Carter", "emily.carter@oxford.example.com", UserRole.CUSTOMER_USER, oxford),

        ("Sarah", "Collins", "sarah.collins@nhsbristol.example.com", UserRole.CUSTOMER_USER, nhs),
        ("Daniel", "Green", "daniel.green@nhsbristol.example.com", UserRole.CUSTOMER_USER, nhs),

        ("Lisa", "Turner", "lisa.turner@biolab.example.com", UserRole.CUSTOMER_USER, biolab),
        ("Michael", "Harris", "michael.harris@biolab.example.com", UserRole.CUSTOMER_USER, biolab),
    ]

    for first_name, last_name, email, role, company in users:
        existing_user = session.query(User).filter_by(email=email).first()

        if existing_user is None:
            session.add(
                User(
                    first_name=first_name,
                    last_name=last_name,
                    email=email.lower(),
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

        existing = (
            session.query(Equipment)
            .filter_by(serial_number=serial)
            .first()
        )

        if existing:
            continue

        company = get_company(session, company_name)

        contact = (
            session.query(User)
            .filter_by(email=email)
            .one()
        )

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


def main():
    session = SessionLocal()

    try:
        seed_companies(session)
        seed_users(session)
        seed_equipment(session)
        seed_service_jobs(session)
    finally:
        session.close()


if __name__ == "__main__":
    main()