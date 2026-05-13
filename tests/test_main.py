from datetime import date, timedelta
import pytest
from nldate import parse


def test_tomorrow():
    assert parse("tomorrow", today=None) == date.today() + timedelta(days=1)


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


def test_in_num_years():
    assert parse("in a year", today=date(2005, 1, 31)) == date(2006, 1, 31)


def test_in_num_years2():
    assert parse("in 1 year", today=date(2005, 1, 31)) == date(2006, 1, 31)


def test_in_num_years3():
    assert parse("in 2 year", today=date(2005, 1, 31)) == date(2007, 1, 31)


def test_days_ago():
    assert parse("2 days ago", today=date(2004, 12, 31)) == date(2004, 12, 29)


def test_days_before():
    assert parse("2 days before", today=date(2004, 12, 31)) == date(2004, 12, 29)


def test_weeks_ago():
    assert parse("1 week ago", today=date(2004, 12, 31)) == date(2004, 12, 24)


def test_weeks_before():
    assert parse("2 weeks before", today=date(2004, 12, 31)) == date(2004, 12, 17)


def test_months_ago():
    assert parse("a month ago", today=date(2004, 12, 31)) == date(2004, 11, 30)


def test_months_before():
    assert parse("2 months before", today=date(2004, 12, 31)) == date(2004, 10, 31)


def test_years_ago():
    assert parse("a year ago", today=date(2004, 12, 31)) == date(2003, 12, 31)


def test_years_before():
    assert parse("2 years ago", today=date(2004, 12, 31)) == date(2002, 12, 31)


def test_days_from():
    assert parse("a day from now") == date.today() + timedelta(days=1)


def test_days_from_2():
    assert parse("1 day from now") == date.today() + timedelta(days=1)


def test_days_from_3():
    assert parse("10 day from now") == date.today() + timedelta(days=10)


def test_weeks_from():
    assert parse("a week from now") == date.today() + timedelta(days=7)


def test_weeks_from_2():
    assert parse("1 week from now") == date.today() + timedelta(days=7)


def test_weeks_from_3():
    assert parse("10 week from now") == date.today() + timedelta(days=7 * 10)


def test_months_from():
    assert parse("a month from now", today=date(2025, 1, 15)) == date(2025, 2, 15)


def test_months_from_2():
    assert parse("1 month from now", today=date(2025, 1, 15)) == date(2025, 2, 15)


def test_months_from_3():
    assert parse("10 months from now", today=date(2025, 1, 15)) == date(2025, 11, 15)


def test_month_rollover():
    assert parse("1 month from now", today=date(2025, 12, 15)) == date(2026, 1, 15)


def test_years_from():
    assert parse("a year from now", today=date(2025, 5, 12)) == date(2026, 5, 12)


def test_years_from_2():
    assert parse("1 year from now", today=date(2025, 5, 12)) == date(2026, 5, 12)


def test_years_from_3():
    assert parse("10 years from now", today=date(2025, 5, 12)) == date(2035, 5, 12)


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


def test_word_digit_dates_short():
    assert parse("Dec 3, 2025") == date(2025, 12, 3)


def test_word_digit_dates_short_2():
    assert parse("Nov 3rd, 2025") == date(2025, 11, 3)


def test_word_digit_dates_short_period_indicator():
    assert parse("Dec. 3, 2025") == date(2025, 12, 3)


def test_word_digit_dates_short_period_indicator_2():
    assert parse("Feb. 12, 2025") == date(2025, 2, 12)


def test_last_friday():
    today = date(2025, 5, 12)  # Monday
    assert parse("last friday", today=today) == date(2025, 5, 9)


def test_last_monday():
    today = date(2025, 5, 15)  # Thursday
    assert parse("last monday", today=today) == date(2025, 5, 12)


def test_last_weekday_wraparound():
    today = date(2025, 5, 11)  # Sunday
    assert parse("last tuesday", today=today) == date(2025, 5, 6)


def test_last_friday_when_today_is_friday():
    today = date(2025, 5, 9)  # Friday
    assert parse("last friday", today=today) == date(2025, 5, 2)


def test_weeks_after_a_date():
    assert parse("2 weeks after December 1st, 2025", today=date(2025, 12, 1)) == date(
        2025, 12, 15
    )


def test_weeks_before_a_date():
    assert parse("2 weeks before December 1st, 2025", today=date(2025, 12, 1)) == date(
        2025, 11, 17
    )


def test_months_after_a_date():
    assert parse("2 months after December 1st, 2025", today=date(2025, 12, 1)) == date(
        2026, 2, 1
    )


def test_months_before_a_date():
    assert parse("2 months before December 1st, 2025", today=date(2025, 12, 1)) == date(
        2025, 10, 1
    )


def test_month_after_31st_goes_to_latest_day():
    assert parse("1 month after January 31st, 2025", today=date(2025, 1, 31)) == date(
        2025, 2, 28
    )


def test_month_before_31st_goes_to_latest_day():
    assert parse("1 month before March 31st, 2025", today=date(2025, 3, 31)) == date(
        2025, 2, 28
    )


def test_month_after_31st_goes_to_30th():
    assert parse("1 month after August 31st, 2025", today=date(2025, 8, 31)) == date(
        2025, 9, 30
    )


def test_month_after_31st_leap_year():
    assert parse("1 month after January 31st, 2024", today=date(2024, 1, 31)) == date(
        2024, 2, 29
    )


def test_years_after_a_date():
    assert parse("2 years after December 1st, 2025", today=date(2025, 12, 1)) == date(
        2027, 12, 1
    )


def test_years_before_a_date():
    assert parse("2 years before December 1st, 2025", today=date(2025, 12, 1)) == date(
        2023, 12, 1
    )


def test_year_after_leap_day():
    assert parse("1 year after February 29th, 2024", today=date(2024, 2, 29)) == date(
        2025, 2, 28
    )


def test_year_before_leap_day():
    assert parse("1 year before February 29th, 2024", today=date(2024, 2, 29)) == date(
        2023, 2, 28
    )


def test_multiple_years_after():
    assert parse("10 years after January 15th, 2025", today=date(2025, 1, 15)) == date(
        2035, 1, 15
    )


def test_multiple_years_before():
    assert parse("10 years before January 15th, 2025", today=date(2025, 1, 15)) == date(
        2015, 1, 15
    )


def test_years_months_before():
    assert parse(
        "2 years, 3 months before Dec. 1, 2025",
        today=date(2025, 12, 1),
    ) == date(2023, 9, 1)


def test_years_months_after():
    assert parse(
        "2 years, 3 months after Dec. 1, 2025",
        today=date(2025, 12, 1),
    ) == date(2028, 3, 1)


def test_years_months_days_before():
    assert parse(
        "1 year, 2 months, 5 days before December 15th, 2025",
        today=date(2025, 12, 15),
    ) == date(2024, 10, 10)


def test_years_months_days_after():
    assert parse(
        "1 year, 2 months, 5 days after December 15th, 2025",
        today=date(2025, 12, 15),
    ) == date(2027, 2, 20)


def test_mixed_with_month_rollover():
    assert parse(
        "1 year, 1 month after January 31st, 2024",
        today=date(2024, 1, 31),
    ) == date(2025, 2, 28)


def test_mixed_before_with_leap_year():
    assert parse(
        "1 year, 1 month before March 31st, 2024",
        today=date(2024, 3, 31),
    ) == date(2023, 2, 28)


def test_years_months_after_yesterday():
    assert parse(
        "1 year and 2 months after yesterday",
        today=date(2025, 12, 1),
    ) == date(2027, 1, 30)


def test_years_months_before_tomorrow():
    assert parse(
        "1 year and 2 months before tomorrow",
        today=date(2025, 12, 1),
    ) == date(2024, 10, 2)


def test_years_months_days_after_yesterday():
    assert parse(
        "1 year, 2 months, and 5 days after yesterday",
        today=date(2025, 12, 1),
    ) == date(2027, 2, 4)


def test_years_months_days_before_tomorrow():
    assert parse(
        "1 year, 2 months, and 5 days before tomorrow",
        today=date(2025, 12, 1),
    ) == date(2024, 9, 27)


def test_mixed_after_last_friday():
    assert parse(
        "1 year and 2 months after last friday",
        today=date(2025, 12, 1),  # Monday; last Friday is 2025-11-28
    ) == date(2027, 1, 28)


def test_mixed_before_last_friday():
    assert parse(
        "1 year and 2 months before last friday",
        today=date(2025, 12, 1),  # Monday; last Friday is 2025-11-28
    ) == date(2024, 9, 28)


def test_mixed_after_tomorrow_with_day():
    assert parse(
        "2 years, 3 months, and 10 days after tomorrow",
        today=date(2025, 12, 1),
    ) == date(2028, 3, 12)


def test_mixed_before_yesterday_with_day():
    assert parse(
        "2 years, 3 months, and 10 days before yesterday",
        today=date(2025, 12, 1),
    ) == date(2023, 8, 20)


def test_the_day_after_tomorrow():
    assert parse(
        "the day after tomorrow",
        today=date(2025, 5, 12),
    ) == date(2025, 5, 14)


def test_the_day_before_yesterday():
    assert parse(
        "the day before yesterday",
        today=date(2025, 5, 12),
    ) == date(2025, 5, 10)


def test_empty_string():
    with pytest.raises(ValueError):
        parse("")


def test_whitespace_string():
    with pytest.raises(ValueError):
        parse("   ")
