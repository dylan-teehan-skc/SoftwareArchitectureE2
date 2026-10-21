from analysis import categorise, country_total, cumulative_series


class EvaApp:
    def __init__(self, user_input, output, load_evas, plot_cumulative):
        self.user_input = user_input
        self.output = output
        self.load_evas = load_evas
        self.plot_cumulative = plot_cumulative

    def run(self):
        evas = self.load_evas(self.user_input.ask_filename())
        country = self.user_input.ask_country()

        self.output.show_country_total(country, country_total(evas, country))
        self.output.show_categories(categorise(evas))

        dates, cumulative_hours = cumulative_series(evas)
        self.plot_cumulative(dates, cumulative_hours)
