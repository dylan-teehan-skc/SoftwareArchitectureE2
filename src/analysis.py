from typing import NamedTuple, Optional


def duration_category(hours):
    if hours < 4:
        return "Short"
    if hours < 7:
        return "Standard"
    return "Long"


def categorise(evas):
    counts = {"Short": 0, "Standard": 0, "Long": 0}
    for eva in evas:
        counts[duration_category(eva.hours)] += 1
    return counts


def is_country(eva, country):
    return eva.country.casefold() == country.casefold()


def country_total(evas, country):
    return sum(eva.hours for eva in evas if is_country(eva, country))


def cumulative_series(evas):
    dated = sorted((eva for eva in evas if eva.date), key=lambda eva: eva.date)

    dates = []
    cumulative_hours = []
    total_hours = 0
    for eva in dated:
        total_hours += eva.hours
        dates.append(eva.date)
        cumulative_hours.append(total_hours)
    return dates, cumulative_hours


class Summary(NamedTuple):
    country: str
    count: int
    total_hours: float
    average_hours: Optional[float]


def in_years(evas, start_year, end_year):
    return [eva for eva in evas if eva.date and start_year <= eva.date.year <= end_year]


def summarise(evas, country):
    count = sum(1 for eva in evas if is_country(eva, country))
    total = country_total(evas, country)
    return Summary(country, count, total, total / count if count else None)


def compare_countries(evas, country_a, country_b, start_year, end_year):
    period = in_years(evas, start_year, end_year)
    a = summarise(period, country_a)
    b = summarise(period, country_b)
    if a.total_hours > b.total_hours:
        leader = a.country
    elif b.total_hours > a.total_hours:
        leader = b.country
    else:
        leader = None
    return a, b, leader
