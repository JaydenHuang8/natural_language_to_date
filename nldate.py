from datetime import date, timedelta
import re
import calendar

NUMBER_WORDS = {
    "a": 1,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
}


def word_or_number_to_int(x: str) -> int:
    if x.isdigit():
        return int(x)

    if x in NUMBER_WORDS:
        return NUMBER_WORDS[x]

    raise ValueError(f"Invalid number: {x}")


def add_months(start: date, months: int) -> date:
    new_month = start.month + months
    new_year = start.year + (new_month - 1) // 12
    new_month = (new_month - 1) % 12 + 1

    last_day = calendar.monthrange(new_year, new_month)[1]
    new_day = min(start.day, last_day)

    return date(new_year, new_month, new_day)


def parse(s: str, today: date | None = None) -> date:
    if today is None:
        today = date.today()

    s = s.strip().lower()

    if s == "":
        return today

    if s == "today":
        return today

    if s == "tomorrow":
        return today + timedelta(days=1)

    if s == "yesterday":
        return today - timedelta(days=1)

    # "in 3 days", "in two days", "in a day"
    match = re.fullmatch(r"in (\w+) days?", s)
    if match:
        n = word_or_number_to_int(match.group(1))
        return today + timedelta(days=n)

    # "in a week", "in two weeks", "in 3 weeks"
    match = re.fullmatch(r"in (\w+) weeks?", s)
    if match:
        n = word_or_number_to_int(match.group(1))
        return today + timedelta(weeks=n)

    # "in two months", "in 2 months", "in a month"
    match = re.fullmatch(r"in (\w+) months?", s)
    if match:
        n = word_or_number_to_int(match.group(1))
        return add_months(today, n)

    # "next tuesday"
    match = re.fullmatch(r"next (\w+)", s)
    if match:
        weekday_name = match.group(1).capitalize()

        weekdays = {
            day: i
            for i, day in enumerate(calendar.day_name)
        }

        if weekday_name not in weekdays:
            raise ValueError("Invalid weekday")

        target = weekdays[weekday_name]
        days_ahead = (target - today.weekday()) % 7

        if days_ahead == 0:
            days_ahead = 7

        return today + timedelta(days=days_ahead)

    # "5 days before December 1st, 2025"
    # "5 days after December 1st, 2025"
    match = re.fullmatch(
        r"(\d+) days? (before|after) ([a-zA-Z]+) (\d+)(st|nd|rd|th), (\d{4})",
        s,
    )

    if match:
        n = int(match.group(1))
        direction = match.group(2)
        month_name = match.group(3).lower()
        day = int(match.group(4))
        year = int(match.group(6))

        months = {
            month.lower(): i
            for i, month in enumerate(calendar.month_name)
            if month
        }

        if month_name not in months:
            raise ValueError("Invalid month")

        target_date = date(year, months[month_name], day)

        if direction == "before":
            return target_date - timedelta(days=n)
        else:
            return target_date + timedelta(days=n)

    raise ValueError(f"Could not parse date string: {s}")