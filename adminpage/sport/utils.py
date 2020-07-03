from datetime import date


def get_study_year_from_date(in_date: date) -> int:
    new_semester_start = date.today().replace(month=8, day=20)
    delta_year = -1 if in_date < new_semester_start else 0
    return in_date.year + delta_year


def get_current_study_year() -> int:
    return get_study_year_from_date(date.today())
