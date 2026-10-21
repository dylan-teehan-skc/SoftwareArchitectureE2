from analysis import (
    categorise,
    compare_countries,
    country_total,
    cumulative_series,
)


class EvaApp:
    def __init__(self, user_input, output, load_evas, plot_cumulative):
        self.user_input = user_input
        self.output = output
        self.load_evas = load_evas
        self.plot_cumulative = plot_cumulative

    def run(self):
        evas = self.user_input.ask_evas(self.load_evas)
        countries = sorted({eva.country for eva in evas})
        country = self.user_input.ask_country(countries)

        self.output.show_country_total(country, country_total(evas, country))
        self.output.show_categories(categorise(evas))

        dates, cumulative_hours = cumulative_series(evas)
        self.plot_cumulative(dates, cumulative_hours)

        self.output.show_comparison_heading()
        country_a = self.user_input.ask_country(countries, "Country A: ")
        country_b = self.user_input.ask_country(countries, "Country B: ")
        start_year, end_year = self.user_input.ask_year_range()
        a, b, leader = compare_countries(
            evas, country_a, country_b, start_year, end_year
        )
        self.output.show_comparison(a, b, leader, start_year, end_year)
