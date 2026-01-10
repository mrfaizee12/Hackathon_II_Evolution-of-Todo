"""Validation utilities for Phase I Advanced todo application.

This module provides validation functions for dates, times, recurrence rules, and templates.
"""

from datetime import datetime
from typing import Tuple
from ..models.enums import RecurrenceType


def validate_due_date(date_str: str) -> Tuple[bool, str, datetime]:
    """
    Validate and parse a due date string in YYYY-MM-DD HH:MM format.

    Args:
        date_str: Date string in YYYY-MM-DD HH:MM format

    Returns:
        Tuple of (is_valid: bool, message: str, parsed_datetime: datetime or None)
    """
    if not date_str or not date_str.strip():
        return False, "Date string cannot be empty", None

    try:
        # Parse the date string using fromisoformat which handles YYYY-MM-DD HH:MM
        dt = datetime.fromisoformat(date_str.replace(" ", "T"))

        # Check if the date is in the past
        if dt < datetime.now():
            return False, "Due date cannot be in the past", None

        return True, "Date is valid", dt
    except ValueError as e:
        return False, f"Invalid date format: {str(e)}. Expected format: YYYY-MM-DD HH:MM", None


def validate_recurrence_rule(recurrence_type: RecurrenceType, interval_days: int = None) -> Tuple[bool, str]:
    """
    Validate a recurrence rule.

    Args:
        recurrence_type: Type of recurrence (NONE, DAILY, WEEKLY, CUSTOM)
        interval_days: Number of days for CUSTOM recurrence

    Returns:
        Tuple of (is_valid: bool, message: str)
    """
    if recurrence_type == RecurrenceType.CUSTOM:
        if interval_days is None:
            return False, "CUSTOM recurrence requires interval_days to be specified"
        if interval_days < 1:
            return False, "interval_days must be positive for CUSTOM recurrence"

    if recurrence_type != RecurrenceType.CUSTOM and interval_days is not None:
        return False, "interval_days should only be specified for CUSTOM recurrence"

    return True, "Recurrence rule is valid"


def validate_template_data(name: str, title: str, due_date_offset: str = None) -> Tuple[bool, str]:
    """
    Validate template data.

    Args:
        name: Template name
        title: Template title
        due_date_offset: Due date offset (today, tomorrow, next_week, next_month, None)

    Returns:
        Tuple of (is_valid: bool, message: str)
    """
    if not name or not name.strip():
        return False, "Template name cannot be empty"

    if not title or not title.strip():
        return False, "Template title cannot be empty"

    valid_offsets = [None, "today", "tomorrow", "next_week", "next_month"]
    if due_date_offset not in valid_offsets:
        return False, f"Invalid due_date_offset: {due_date_offset}. Valid values: {valid_offsets}"

    return True, "Template data is valid"