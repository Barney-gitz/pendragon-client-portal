from app.db.session import SessionLocal
from app.models.company import Company


def main():
    session = SessionLocal()

    try:
        oxford = (
            session.query(Company)
            .filter_by(name="University of Oxford")
            .one()
        )

        print(f"\nCompany: {oxford.name}\n")

        for equipment in oxford.equipment:
            print(
                f"{equipment.make} "
                f"{equipment.model} "
                f"({equipment.serial_number})"
            )

    finally:
        session.close()


if __name__ == "__main__":
    main()