"""
Seed the database from src/seed_data.json.

Reads the JSON file of real Birmingham services and loads it into the
database. Safe to re-run: if a Category slug or a Service name already
exists, it's updated in place rather than duplicated.

Usage:
    python -m src.seed_loader              # from the repo root
    python src/seed_loader.py              # also works

The script wraps everything in an app context so models can be used as
they would inside a request.
"""

from __future__ import annotations

import json
from datetime import time
from pathlib import Path

from src.app import create_app
from src.models import Category, OpeningHours, Service, db


SEED_FILE = Path(__file__).parent / "seed_data.json"


def parse_time(value: str | None) -> time | None:
    """Parse 'HH:MM' into a datetime.time, or None if value is None."""
    if value is None:
        return None
    hours, minutes = value.split(":")
    return time(int(hours), int(minutes))


def load_categories(category_data: list[dict]) -> dict[str, Category]:
    """Insert or update categories. Returns slug -> Category mapping."""
    categories_by_slug: dict[str, Category] = {}
    for entry in category_data:
        existing = Category.query.filter_by(slug=entry["slug"]).first()
        if existing:
            existing.display_name = entry["display_name"]
            categories_by_slug[entry["slug"]] = existing
        else:
            category = Category(slug=entry["slug"], display_name=entry["display_name"])
            db.session.add(category)
            categories_by_slug[entry["slug"]] = category
    db.session.flush()  # ensure new categories get IDs before services reference them
    return categories_by_slug


def load_service(
    service_data: dict, categories_by_slug: dict[str, Category]
) -> Service:
    """Insert or update a single service. Returns the Service instance."""
    # Find an existing service by name (the JSON's `id` field is for human
    # reference; we match on name for idempotency).
    existing = Service.query.filter_by(name=service_data["name"]).first()
    service = existing if existing else Service()

    service.name = service_data["name"]
    service.description = service_data["description"]
    service.address = service_data["address"]
    service.postcode = service_data.get("postcode")
    service.phone = service_data.get("phone")
    service.website = service_data.get("website")
    service.latitude = service_data.get("latitude")
    service.longitude = service_data.get("longitude")
    service.requires_voucher = service_data.get("requires_voucher", False)
    service.requires_referral = service_data.get("requires_referral", False)
    service.is_drop_in = service_data.get("is_drop_in", True)
    service.eligibility_notes = service_data.get("eligibility_notes")
    service.is_active = service_data.get("is_active", True)
    service.needs_verification = service_data.get("needs_verification", False)
    service.data_sourced_from = service_data.get("data_sourced_from")

    # Reset and reassign categories from the JSON.
    service.categories = [
        categories_by_slug[slug]
        for slug in service_data.get("categories", [])
        if slug in categories_by_slug
    ]

    if not existing:
        db.session.add(service)
    db.session.flush()  # ensure service has an ID before we attach hours

    # Replace opening hours wholesale. Simpler than diffing, and rare enough
    # in a re-seed that the cost doesn't matter.
    service.opening_hours = []
    for hours_data in service_data.get("opening_hours", []):
        service.opening_hours.append(
            OpeningHours(
                day_of_week=hours_data["day_of_week"],
                opens_at=parse_time(hours_data.get("opens_at")),
                closes_at=parse_time(hours_data.get("closes_at")),
                is_closed=hours_data.get("is_closed"),
            )
        )

    return service


def seed() -> dict:
    """Run the full seed process. Returns a small summary dict for logging."""
    with SEED_FILE.open() as f:
        data = json.load(f)

    categories_by_slug = load_categories(data["categories"])
    for service_data in data["services"]:
        load_service(service_data, categories_by_slug)

    db.session.commit()

    return {
        "categories_loaded": len(data["categories"]),
        "services_loaded": len(data["services"]),
        "metadata": data.get("_metadata", {}),
    }


def main() -> None:
    """Entry point when run from the command line."""
    app = create_app()
    with app.app_context():
        summary = seed()
        print(
            f"Seeded {summary['services_loaded']} services "
            f"across {summary['categories_loaded']} categories."
        )
        if "data_sourced_date" in summary["metadata"]:
            print(f"Data sourced: {summary['metadata']['data_sourced_date']}")


if __name__ == "__main__":
    main()
