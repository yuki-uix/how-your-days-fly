#!/usr/bin/env python3
"""Produce layout-independent Gregorian data for year/month/week/day views.

Only Python's standard library is required. Supported anchor years are 2–9998
so adjacent days in a month grid or week remain representable by datetime.
No lunar dates, solar terms, public holidays, or timezone instants are inferred.
"""

from __future__ import annotations

import argparse
import calendar
from datetime import date, timedelta
import json
import sys

VIEWS = ("year", "month", "week", "day")
WEEK_STARTS = {"monday": calendar.MONDAY, "sunday": calendar.SUNDAY}


def day_record(value: date) -> dict:
    iso = value.isocalendar()
    return {
        "date": value.isoformat(),
        "year": value.year,
        "month": value.month,
        "day": value.day,
        "weekday_monday0": value.weekday(),
        "iso_week_year": iso.year,
        "iso_week": iso.week,
    }


def month_record(year: int, month: int, week_start: str) -> dict:
    cal = calendar.Calendar(WEEK_STARTS[week_start])
    weeks = []
    for week in cal.monthdatescalendar(year, month):
        cells = []
        for value in week:
            cell = day_record(value)
            cell["in_month"] = value.year == year and value.month == month
            cells.append(cell)
        weeks.append(cells)
    return {"year": year, "month": month, "weeks": weeks}


def calendar_data(view: str, anchor: date, week_start: str = "monday") -> dict:
    """Build inclusive period dates plus month grids where applicable.

    `days` contains every date in the requested period exactly once. Month
    grids also include adjacent-month dates; use their `in_month` flag.
    ISO week metadata always follows ISO rules, independently of week_start.
    """
    if view not in VIEWS:
        raise ValueError(f"view must be one of {', '.join(VIEWS)}")
    if week_start not in WEEK_STARTS:
        raise ValueError(f"week_start must be one of {', '.join(WEEK_STARTS)}")
    if not 2 <= anchor.year <= 9998:
        raise ValueError("anchor year must be between 2 and 9998")

    if view == "year":
        start, end = date(anchor.year, 1, 1), date(anchor.year, 12, 31)
        months = [month_record(anchor.year, month, week_start) for month in range(1, 13)]
    elif view == "month":
        start = anchor.replace(day=1)
        end = anchor.replace(day=calendar.monthrange(anchor.year, anchor.month)[1])
        months = [month_record(anchor.year, anchor.month, week_start)]
    elif view == "week":
        offset = (anchor.weekday() - WEEK_STARTS[week_start]) % 7
        start = anchor - timedelta(days=offset)
        end = start + timedelta(days=6)
        months = []
    else:
        start = end = anchor
        months = []

    days = [day_record(start + timedelta(days=n)) for n in range((end-start).days + 1)]
    return {
        "schema_version": 1,
        "calendar_system": "proleptic-gregorian",
        "view": view,
        "anchor_date": anchor.isoformat(),
        "week_start": week_start,
        "period": {"start": start.isoformat(), "end": end.isoformat()},
        "days": days,
        "months": months,
    }


def parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("use a valid ISO date such as 2027-01-01") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--view", required=True, choices=VIEWS)
    parser.add_argument("--date", required=True, type=parse_date, dest="anchor")
    parser.add_argument("--week-start", choices=tuple(WEEK_STARTS), default="monday")
    args = parser.parse_args(argv)
    try:
        model = calendar_data(args.view, args.anchor, args.week_start)
    except ValueError as exc:
        parser.error(str(exc))
    json.dump(model, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
