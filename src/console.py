def parse_year(text):
    if not text.isdigit():
        raise ValueError("Please enter a year as a whole number, e.g. 1990.")
    return int(text)


class ConsoleInput:
    def __init__(self, read=input, write=print):
        self.read = read
        self.write = write

    def _ask_until(self, prompt, parse):
        while True:
            try:
                return parse(self.read(prompt).strip())
            except ValueError as error:
                self.write(error)

    def ask_evas(self, load_evas):
        return self._ask_until("Enter the data filename: ", load_evas)

    def ask_country(self, countries, prompt="Enter a country (USA or Russia): "):
        by_key = {country.casefold(): country for country in countries}

        def parse_country(text):
            if text.casefold() not in by_key:
                raise ValueError(
                    f"Unknown country. Choose from: {', '.join(countries)}"
                )
            return by_key[text.casefold()]

        return self._ask_until(prompt, parse_country)

    def ask_year_range(self):
        while True:
            start = self._ask_until("Start year: ", parse_year)
            end = self._ask_until("End year: ", parse_year)
            if start <= end:
                return start, end
            self.write("Start year must not be after end year.")


class ConsoleOutput:
    def __init__(self, write=print):
        self.write = write

    def show_country_total(self, country, hours):
        self.write(f"Total EVA duration for {country}: {hours:.2f} hours")

    def show_categories(self, counts):
        classified = sum(counts.values())
        self.write("EVA duration categories (all EVAs with a duration):")
        for category, count in counts.items():
            percentage = count / classified * 100 if classified else 0
            self.write(f"{category}: {count} EVAs ({percentage:.2f}%)")

    def show_comparison_heading(self):
        self.write("\nCompare EVA activity between two countries")

    def show_comparison(self, a, b, leader, start_year, end_year):
        self.write(f"EVA comparison {start_year}-{end_year} (dated EVAs only):")
        for summary in (a, b):
            if summary.average_hours is None:
                average = "unavailable"
            else:
                average = f"{summary.average_hours:.2f} hours"
            self.write(
                f"{summary.country}: {summary.count} EVAs, "
                f"{summary.total_hours:.2f} hours total, average {average}"
            )
        if leader is None:
            self.write("Result: tie")
        else:
            self.write(f"Greater total EVA duration: {leader}")
