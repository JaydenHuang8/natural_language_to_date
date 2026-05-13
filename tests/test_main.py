import sys
from pathlib import Path
from datetime import date, timedelta

#sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from nldate import parse


def test_tomorrow():
    assert parse("tomorrow", today=None) == date.today() + timedelta(days=1)


def test_empty_input():
    assert parse("", today=None) == date.today()


def test_date1():
    assert parse("5 days before December 1st, 2025", today=None) == date(2025, 11, 26)


def test_in_num_days_today():
    assert parse("in 3 days", today=None) == date.today() + timedelta(days=3)


def test_in_num_days_set_day():
    assert parse("in 2 days", today=date(2004, 12, 31)) == date(2005, 1, 2)


# ---------


def test_in_num_weeks():
    assert parse("in a week", today=None) == date.today() + timedelta(days=7)


def test_in_num_months():
    assert parse("in two months", today=date(2005, 1, 1)) == date(2005, 3, 1)


def test_in_num_months2():
    assert parse("in a month", today=date(2005, 1, 31)) == date(2005, 2, 28)


def test_days_after_a_date():
    assert parse("5 days after December 1st, 2025", today=date(2025, 12, 1)) == date(
        2025, 12, 6
    )


def test_days_before_a_date():
    assert parse("5 days before December 1st, 2025", today=date(2025, 12, 1)) == date(
        2025, 11, 26
    )


def test_next_week_day():
    assert parse("next tuesday", today=date(2026, 5, 11)) == date(2026, 5, 12)


def test_next_week_day2():
    assert parse("next friday", today=date(2026, 5, 11)) == date(2026, 5, 15)
