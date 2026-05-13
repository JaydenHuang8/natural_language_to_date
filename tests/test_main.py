from datetime import date, timedelta

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

def test_iso_date_with_spaces():
    assert parse(" 2025-12-31 ") == date(2025, 12, 31)

def test_single_digit_month_day():
    assert parse("2025-1-7") == date(2025, 1, 7)

def test_single_digit_month_day_slash():
    assert parse("2025/1/7") == date(2025, 1, 7)

def test_single_digit_month_day_slash_us_format():
    assert parse("1/7/2025") == date(2025, 1, 7)

def test_single_digit_month_day_dash_us_format():
    assert parse("2-5-2025") == date(2025, 2, 5)

def test_word_digit_dates():
    assert parse("December 1, 2025") == date(2025, 12, 1)

def test_word_digit_dates_2():
    assert parse("March 2nd, 2025") == date(2025, 3, 2)

def test_word_digit_dates_3():
    assert parse("April 3rd, 2025") == date(2025, 4, 3)