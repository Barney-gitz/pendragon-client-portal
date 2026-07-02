from app.db.session import SessionLocal
from app.models.company import Company
from app.models.user import User, UserRole


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


def main():
    session = SessionLocal()

    try:
        seed_companies(session)
        seed_users(session)
    finally:
        session.close()


if __name__ == "__main__":
    main()