from tests.fixtures.users import admin_user


def test_admin_user_fixture(admin_user):
    assert admin_user.email == "admin@test.com"
    assert admin_user.first_name == "Test"