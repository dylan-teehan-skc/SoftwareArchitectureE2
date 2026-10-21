import sys
import unittest
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from app import EvaApp  # noqa: E402
from console import ConsoleInput, ConsoleOutput  # noqa: E402
from eva_data import Eva, load_evas  # noqa: E402


def fake_read(*answers):
    answers = iter(answers)
    return lambda prompt: next(answers)


class InvalidInputTests(unittest.TestCase):
    def test_start_after_end_is_asked_again(self):
        messages = []
        user_input = ConsoleInput(
            fake_read("2010", "1990", "1990", "2000"), messages.append
        )
        self.assertEqual(user_input.ask_year_range(), (1990, 2000))
        self.assertEqual(messages, ["Start year must not be after end year."])

    def test_non_numeric_year_is_asked_again(self):
        messages = []
        user_input = ConsoleInput(fake_read("abc", "1990", "2000"), messages.append)
        self.assertEqual(user_input.ask_year_range(), (1990, 2000))
        self.assertEqual(len(messages), 1)

    def test_unknown_country_is_asked_again(self):
        messages = []
        user_input = ConsoleInput(fake_read("France", "usa"), messages.append)
        self.assertEqual(user_input.ask_country(["Russia", "USA"]), "USA")
        self.assertEqual(messages, ["Unknown country. Choose from: Russia, USA"])

    def test_missing_file_is_asked_again(self):
        messages = []
        path = str(Path(__file__).resolve().parent.parent / "data" / "eva-data.json")
        user_input = ConsoleInput(fake_read("missing.json", path), messages.append)
        self.assertEqual(len(user_input.ask_evas(load_evas)), 374)
        self.assertTrue(messages[0].startswith("Cannot open missing.json"))


class AppTests(unittest.TestCase):
    def test_full_run_without_files_or_plot_window(self):
        evas = [
            Eva("USA", datetime(2000, 1, 1), 6.0),
            Eva("Russia", datetime(2000, 1, 1), 2.0),
        ]
        shown = []
        plotted = []
        app = EvaApp(
            ConsoleInput(fake_read("any.json", "USA", "USA", "Russia", "2000", "2000")),
            ConsoleOutput(shown.append),
            load_evas=lambda path: evas,
            plot_cumulative=lambda dates, hours: plotted.append(hours),
        )
        app.run()
        self.assertEqual(plotted, [[6.0, 8.0]])
        self.assertIn("Total EVA duration for USA: 6.00 hours", shown)
        self.assertIn("Russia: 1 EVAs, 2.00 hours total, average 2.00 hours", shown)
        self.assertEqual(shown[-1], "Greater total EVA duration: USA")


if __name__ == "__main__":
    unittest.main()
