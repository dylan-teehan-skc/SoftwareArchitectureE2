import json
from datetime import datetime
from typing import NamedTuple, Optional


class Eva(NamedTuple):
    country: str
    date: Optional[datetime]
    hours: float


def parse_duration(text):
    hours, minutes = map(int, text.split(":"))
    return hours + minutes / 60


def load_evas(path):
    with open(path, "r", encoding="utf-8") as file:
        records = json.load(file)

    evas = []
    for record in records:
        duration_text = record.get("duration")
        if not duration_text:
            continue

        date_text = record.get("date")
        evas.append(
            Eva(
                country=record.get("country", ""),
                date=datetime.fromisoformat(date_text) if date_text else None,
                hours=parse_duration(duration_text),
            )
        )
    return evas
