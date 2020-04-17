from datetime import datetime, timezone
from typing import Optional

import pytz

from app.core.config import TIMEZONE


def convert_from_utc(datetime_obj: datetime, tz: Optional[str] = None) -> datetime:
    if tz is None:
        return datetime_obj.replace(tzinfo=timezone.utc).astimezone(TIMEZONE)
    else:
        return datetime_obj.replace(tzinfo=timezone.utc).astimezone(pytz.timezone(tz))
