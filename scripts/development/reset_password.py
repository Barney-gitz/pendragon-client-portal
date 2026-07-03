import getpass

from app.auth.hashing import hash_password
from app.db.session import SessionLocal
from app.models.user import User


def main() -> None:
    email = input("Email: ").strip().lower()
    password = getpass.getpass("New password: ")
    confirm_password = getpass.getpass("Confirm password: ")

    if password != confirm_password:
        print("Passwords do not match.")
        return

    db = SessionLocal()

    try:
        user = db.query(User).filter(User.email == email).first()

        if user is None:
            print("User not found.")
            return

        user.password_hash = hash_password(password)

        db.commit()

        print(f"Password reset successfully for {email}.")

    finally:
        db.close()


if __name__ == "__main__":
    main()