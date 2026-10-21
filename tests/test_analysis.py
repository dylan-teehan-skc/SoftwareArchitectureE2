import sys
import unittest
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from analysis import categorise, compare_countries, country_total  # noqa: E402
from eva_data import Eva, load_evas, parse_duration  # noqa: E402


def eva(country, year, hours):
    return Eva(country, datetime(year, 6, 1) if year else None, hours)


SAMPLE = [
    eva("USA", 1999, 10.0),  # before the range
    eva("USA", 2000, 5.0),
    eva("USA", 2001, 3.0),
    eva("Russia", 2000, 4.0),
    eva("USA", None, 20.0),  # undated, never in a year range
]


class CompareCountriesTests(unittest.TestCase):
    def test_counts_totals_averages_and_leader(self):
        usa, russia, leader = compare_countries(SAMPLE, "USA", "Russia", 2000, 2001)
        self.assertEqual((usa.count, usa.total_hours, usa.average_hours), (2, 8.0, 4.0))
        self.assertEqual(
            (russia.count, russia.total_hours, russia.average_hours), (1, 4.0, 4.0)
        )
        self.assertEqual(leader, "USA")

    def test_start_and_end_years_are_included(self):
        usa, _, _ = compare_countries(SAMPLE, "USA", "Russia", 1999, 2000)
        self.assertEqual((usa.count, usa.total_hours), (2, 15.0))

    def test_country_with_no_matches_is_zero_and_unavailable(self):
        usa, russia, leader = compare_countries(SAMPLE, "USA", "Russia", 2001, 2001)
        self.assertEqual(
            (russia.count, russia.total_hours, russia.average_hours), (0, 0, None)
        )
        self.assertEqual(leader, "USA")

    def test_equal_totals_are_a_tie(self):
        evas = [eva("USA", 2000, 4.0), eva("Russia", 2000, 4.0)]
        _, _, leader = compare_countries(evas, "USA", "Russia", 2000, 2000)
        self.assertIsNone(leader)

    def test_country_match_ignores_case(self):
        usa, _, _ = compare_countries(SAMPLE, "usa", "Russia", 2000, 2001)
        self.assertEqual(usa.count, 2)


class ExistingAnalysisTests(unittest.TestCase):
    def test_category_boundaries(self):
        evas = [eva("USA", 2000, h) for h in (3.99, 4.0, 6.99, 7.0)]
        self.assertEqual(categorise(evas), {"Short": 1, "Standard": 2, "Long": 1})

    def test_country_total_includes_undated(self):
        self.assertEqual(country_total(SAMPLE, "USA"), 38.0)

    def test_parse_duration(self):
        self.assertEqual(parse_duration("1:30"), 1.5)

    def test_supplied_dataset_matches_handoff_figures(self):
        evas = load_evas(ROOT / "data" / "eva-data.json")
        self.assertAlmostEqual(country_total(evas, "USA"), 1360.07, places=2)
        self.assertAlmostEqual(country_total(evas, "Russia"), 626.58, places=2)
        self.assertEqual(categorise(evas), {"Short": 84, "Standard": 214, "Long": 76})


if __name__ == "__main__":
    unittest.main()
