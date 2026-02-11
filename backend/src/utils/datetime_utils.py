from datetime import datetime, timedelta, timezone

def get_utc_now() -> datetime:
    """
    Returns the current UTC datetime with timezone information.
    """
    return datetime.now(timezone.utc)

def is_future_datetime(dt: datetime) -> bool:
    """
    Checks if a given datetime is in the future relative to now (UTC).
    """
    if dt.tzinfo is None:
        # Assume UTC if no timezone info, or convert to aware if needed
        return dt > get_utc_now().replace(tzinfo=None) # Compare naive to naive for simplicity, assuming input is UTC
    return dt > get_utc_now()

def calculate_next_occurrence(
    current_occurrence: datetime,
    recurrence_type: str,
    recurrence_interval: int
) -> datetime:
    """
    Calculates the next occurrence of a recurring task.
    Assumes current_occurrence is timezone-aware UTC.
    """
    if recurrence_type == "daily":
        return current_occurrence + timedelta(days=recurrence_interval)
    elif recurrence_type == "weekly":
        return current_occurrence + timedelta(weeks=recurrence_interval)
    elif recurrence_type == "monthly":
        # This is a simplified monthly calculation that adds months directly.
        # A more robust solution might consider day of month, end of month, etc.
        # For simplicity, we'll just add days equivalent to 30*interval
        return current_occurrence + timedelta(days=30 * recurrence_interval)
    else:
        raise ValueError(f"Unsupported recurrence type: {recurrence_type}")

def get_time_until(target_dt: datetime) -> timedelta:
    """
    Returns the timedelta until a target datetime from now (UTC).
    """
    return target_dt - get_utc_now()
