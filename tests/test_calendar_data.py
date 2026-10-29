import importlib.util
from datetime import date, timedelta
from pathlib import Path
import subprocess
import sys
import unittest
import json


SCRIPT = Path(__file__).resolve().parents[1] / ".agents/skills/calendar-design-lab/scripts/calendar_data.py"
spec = importlib.util.spec_from_file_location("calendar_data", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
build = module.calendar_data


class CalendarDataTests(unittest.TestCase):
    def test_2027_full_year_has_no_missing_or_repeated_days(self):
        model = build("year", date(2027, 8, 9))
        days = model["days"]
        self.assertEqual(len(days), 365)
        self.assertEqual(len({d["date"] for d in days}), 365)
        self.assertEqual(days[0]["date"], "2027-01-01")
        self.assertEqual(days[-1]["date"], "2027-12-31")
        self.assertEqual(sum(d["weekday_monday0"] >= 5 for d in days), 104)
        for current, following in zip(days, days[1:]):
            self.assertEqual(date.fromisoformat(following["date"]) - date.fromisoformat(current["date"]), timedelta(days=1))

    def test_gregorian_leap_year_boundaries(self):
        for year, count in [(1900, 28), (2000, 29), (2027, 28), (2028, 29), (2100, 28)]:
            with self.subTest(year=year):
                model = build("month", date(year, 2, 14))
                self.assertEqual(len(model["days"]), count)
        self.assertEqual(len(build("year", date(2028, 1, 1))["days"]), 366)

    def test_six_row_months_keep_the_final_dates(self):
        for month, last_dates in [(5, ["2027-05-31"]), (8, ["2027-08-30", "2027-08-31"])]:
            with self.subTest(month=month):
                grid = build("month", date(2027, month, 1))["months"][0]["weeks"]
                self.assertEqual(len(grid), 6)
                self.assertEqual([d["date"] for d in grid[-1] if d["in_month"]], last_dates)

    def test_week_crosses_year_with_correct_iso_metadata(self):
        model = build("week", date(2027, 1, 1))
        self.assertEqual(model["period"], {"start": "2026-12-28", "end": "2027-01-03"})
        new_year = model["days"][4]
        self.assertEqual((new_year["iso_week_year"], new_year["iso_week"]), (2026, 53))
        self.assertEqual(new_year["weekday_monday0"], 4)

    def test_sunday_start_changes_grouping_without_changing_iso_metadata(self):
        model = build("week", date(2027, 1, 1), "sunday")
        self.assertEqual(model["period"], {"start": "2026-12-27", "end": "2027-01-02"})
        grid = build("month", date(2027, 8, 1), "sunday")["months"][0]["weeks"]
        self.assertEqual(grid[0][0]["date"], "2027-08-01")
        self.assertEqual(grid[0][0]["weekday_monday0"], 6)
        self.assertEqual(len(grid), 5)

    def test_adjacent_dates_are_real_dates_and_flagged(self):
        grid = build("month", date(2027, 1, 1))["months"][0]["weeks"]
        self.assertEqual(grid[0][0]["date"], "2026-12-28")
        self.assertFalse(grid[0][0]["in_month"])
        self.assertTrue(grid[0][4]["in_month"])
        self.assertEqual(sum(d["in_month"] for week in grid for d in week), 31)
        for week in grid:
            self.assertEqual(len(week), 7)

    def test_day_view_has_one_day_and_no_month_layout(self):
        model = build("day", date(2028, 2, 29))
        self.assertEqual(len(model["days"]), 1)
        self.assertEqual(model["days"][0]["date"], "2028-02-29")
        self.assertEqual(model["months"], [])

    def test_supported_extremes_keep_adjacent_days_representable(self):
        for anchor in [date(2, 1, 1), date(9998, 12, 31)]:
            for view in module.VIEWS:
                with self.subTest(anchor=anchor, view=view):
                    self.assertTrue(build(view, anchor)["days"])
        for year in [1, 9999]:
            with self.assertRaises(ValueError):
                build("year", date(year, 1, 1))

    def test_cli_emits_json_and_rejects_invalid_date(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--view", "day", "--date", "2028-02-29"], capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(result.stdout)["days"][0]["date"], "2028-02-29")
        bad = subprocess.run([sys.executable, str(SCRIPT), "--view", "day", "--date", "2027-02-29"], capture_output=True, text=True)
        self.assertNotEqual(bad.returncode, 0)
        self.assertNotIn("Traceback", bad.stderr)


if __name__ == "__main__":
    unittest.main()
