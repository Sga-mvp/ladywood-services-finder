"""
Create the first OrgAdmin account.

Run from the repo root:

    python -m src.create_admin <email> <password> [<organisation_name>]

If no organisation name is given, the email's local part is used.
Safe to re-run: if the email already exists, the script updates the
password instead of creating a duplicate.

This is a development helper. In production a real signup or invitation
flow would replace it.
"""

from __future__ import annotations

import sys

from src.app import create_app
from src.models import OrgAdmin, db


def create_or_update(email: str, password: str, organisation_name: str | None = None) -> OrgAdmin:
    """Create or update an OrgAdmin with the given credentials."""
    email = email.strip().lower()
    if organisation_name is None:
        organisation_name = email.split("@")[0]

    admin = OrgAdmin.query.filter_by(email=email).first()
    if admin is None:
        admin = OrgAdmin(email=email, organisation_name=organisation_name)
        db.session.add(admin)
        verb = "Created"
    else:
        admin.organisation_name = organisation_name
        verb = "Updated"

    admin.set_password(password)
    db.session.commit()

    print(f"{verb} admin: {admin.email} (org: {admin.organisation_name})")
    return admin


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: python -m src.create_admin <email> <password> [<organisation_name>]")
        sys.exit(1)

    email = sys.argv[1]
    password = sys.argv[2]
    org_name = sys.argv[3] if len(sys.argv) >= 4 else None

    app = create_app()
    with app.app_context():
        create_or_update(email, password, org_name)


if __name__ == "__main__":
    main()
