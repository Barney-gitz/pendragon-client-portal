import pytest

from app.models.equipment import Equipment


@pytest.fixture
def equipment(db, company, admin_user):
    machine = Equipment(
        company_id=company.id,
        primary_contact_user_id=admin_user.id,
        make="Thermo",
        model="Veriti",
        serial_number="TEST-SERIAL-001",
        is_active=True,
    )

    db.add(machine)
    db.commit()
    db.refresh(machine)

    return machine