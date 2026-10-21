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
