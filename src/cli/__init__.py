"""CLI input and output handlers."""

from src.cli.input_handler import (
    get_task_title,
    get_task_description,
    get_menu_choice,
    get_task_id,
    get_status_choice,
    get_optional_input,
    get_priority_choice,
    get_tags_input
)
from src.cli.output_formatter import format_task_list
from src.cli.style import heading, separator, success, error, info

__all__ = [
    "get_task_title",
    "get_task_description",
    "get_menu_choice",
    "get_task_id",
    "get_status_choice",
    "get_optional_input",
    "get_priority_choice",
    "get_tags_input",
    "format_task_list",
    "heading",
    "separator",
    "success",
    "error",
    "info"
]
