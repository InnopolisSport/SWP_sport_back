from datetime import datetime, timezone

from app.core.config import TIMEZONE


def convert_from_utc(datetime_obj: datetime) -> datetime:
    return datetime_obj.replace(tzinfo=timezone.utc).astimezone(TIMEZONE)
