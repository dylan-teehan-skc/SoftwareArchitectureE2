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
    try:
        with open(path, "r", encoding="utf-8") as file:
            return parse_records(json.load(file))
    except OSError as error:
        raise ValueError(f"Cannot open {path}: {error.strerror}.") from error
    except (ValueError, TypeError, AttributeError) as error:
        raise ValueError(f"{path} is not a valid EVA data file.") from error


def parse_records(records):
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
