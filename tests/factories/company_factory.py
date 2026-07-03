from app.models.company import Company


def create_company(
    *,
    name: str = "Test Company",
    is_active: bool = True,
) -> Company:
    return Company(
        name=name,
        is_active=is_active,
    )