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
    total_months = start.month - 1 + months
    new_year = start.year + total_months // 12
    new_month = total_months % 12 + 1

    last_day = calendar.monthrange(new_year, new_month)[1]
    new_day = min(start.day, last_day)

    return date(new_year, new_month, new_day)


def add_years(start: date, years: int) -> date:
    new_year = start.year + years
    last_day = calendar.monthrange(new_year, start.month)[1]
    new_day = min(start.day, last_day)

    return date(new_year, start.month, new_day)


def make_month_dict() -> dict[str, int]:
    full_months = {
        month.lower(): i for i, month in enumerate(calendar.month_name) if month
    }

    short_months = {
        month.lower(): i for i, month in enumerate(calendar.month_abbr) if month
    }

    short_months_with_period = {
        f"{month}.": number for month, number in short_months.items()
    }

    return full_months | short_months | short_months_with_period


def parse_date_text(s: str, all_months: dict[str, int]) -> date | None:
    s = s.strip().lower()

    match = re.fullmatch(r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})", s)
    if match:
        return date(
            int(match.group(1)),
            int(match.group(2)),
            int(match.group(3)),
        )

    match = re.fullmatch(r"(\d{1,2})[-/](\d{1,2})[-/](\d{4})", s)
    if match:
        return date(
            int(match.group(3)),
            int(match.group(1)),
            int(match.group(2)),
        )

    match = re.fullmatch(
        r"([a-zA-Z]+\.?) (\d+)(st|nd|rd|th)?, (\d{4})",
        s,
    )
    if match:
        month_name = match.group(1).lower()
        day = int(match.group(2))
        year = int(match.group(4))

        if month_name not in all_months:
            raise ValueError("Invalid month")

        return date(year, all_months[month_name], day)

    return None


def move_date(start: date, n: int, unit: str) -> date:
    if unit.startswith("day"):
        return start + timedelta(days=n)

    if unit.startswith("week"):
        return start + timedelta(weeks=n)

    if unit.startswith("month"):
        return add_months(start, n)

    if unit.startswith("year"):
        return add_years(start, n)

    raise ValueError(f"Invalid unit: {unit}")


def apply_parts(start: date, parts: list[tuple[int, str]], sign: int) -> date:
    result = start

    for n, unit in parts:
        result = move_date(result, sign * n, unit)

    return result


def parse_parts(s: str) -> list[tuple[int, str]]:
    s = s.replace(", and ", ", ")
    s = s.replace(" and ", ", ")

    parts = []

    for part in s.split(","):
        part = part.strip()

        match = re.fullmatch(
            r"(\w+) (days?|weeks?|months?|years?)",
            part,
        )

        if not match:
            raise ValueError(f"Invalid date part: {part}")

        n = word_or_number_to_int(match.group(1))
        unit = match.group(2)

        parts.append((n, unit))

    return parts


def parse_base_date(s: str, today: date, all_months: dict[str, int]) -> date | None:
    s = s.strip().lower()

    parsed_date = parse_date_text(s, all_months)
    if parsed_date is not None:
        return parsed_date

    if s == "today":
        return today

    if s == "tomorrow":
        return today + timedelta(days=1)

    if s == "yesterday":
        return today - timedelta(days=1)

    if s == "the day after tomorrow":
        return today + timedelta(days=2)

    if s == "the day before yesterday":
        return today - timedelta(days=2)

    weekdays = {day.lower(): i for i, day in enumerate(calendar.day_name)}

    match = re.fullmatch(r"last (\w+)", s)
    if match:
        weekday_name = match.group(1)

        if weekday_name not in weekdays:
            raise ValueError("Invalid weekday")

        target = weekdays[weekday_name]
        days_back = (today.weekday() - target) % 7

        if days_back == 0:
            days_back = 7

        return today - timedelta(days=days_back)

    match = re.fullmatch(r"next (\w+)", s)
    if match:
        weekday_name = match.group(1)

        if weekday_name not in weekdays:
            raise ValueError("Invalid weekday")

        target = weekdays[weekday_name]
        days_ahead = (target - today.weekday()) % 7

        if days_ahead == 0:
            days_ahead = 7

        return today + timedelta(days=days_ahead)

    return None


def parse(s: str, today: date | None = None) -> date:
    if today is None:
        today = date.today()

    s = s.strip().lower()

    all_months = make_month_dict()

    parsed_date = parse_date_text(s, all_months)
    if parsed_date is not None:
        return parsed_date

    if s == "":
        return today

    base_date = parse_base_date(s, today, all_months)
    if base_date is not None:
        return base_date

    match = re.fullmatch(r"in (\w+) (days?|weeks?|months?|years?)", s)
    if match:
        n = word_or_number_to_int(match.group(1))
        unit = match.group(2)
        return move_date(today, n, unit)

    match = re.fullmatch(r"(\w+) (days?|weeks?|months?|years?) from now", s)
    if match:
        n = word_or_number_to_int(match.group(1))
        unit = match.group(2)
        return move_date(today, n, unit)

    match = re.fullmatch(r"(\w+) (days?|weeks?|months?|years?) (ago|before)", s)
    if match:
        n = word_or_number_to_int(match.group(1))
        unit = match.group(2)
        return move_date(today, -n, unit)

    match = re.fullmatch(r"(.+) (before|after) (.+)", s)
    if match:
        parts_text = match.group(1)
        direction = match.group(2)
        base_text = match.group(3)

        base_date = parse_base_date(base_text, today, all_months)

        if base_date is None:
            raise ValueError(f"Invalid date: {base_text}")

        parts = parse_parts(parts_text)

        sign = 1
        if direction == "before":
            sign = -1

        return apply_parts(base_date, parts, sign)

    raise ValueError(f"Could not parse date string: {s}")
