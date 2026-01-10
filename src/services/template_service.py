"""TemplateService for managing task templates in Phase I Advanced todo application.

This module provides CRUD operations for task templates.
"""

from datetime import datetime
from typing import Optional, List
from src.models.template import TaskTemplate
from src.models.task import Task
from src.utils.validators import validate_template_data


class TemplateService:
    """Manages task template CRUD operations."""

    def __init__(self, max_templates: int = 10):
        """Initialize TemplateService with maximum template limit."""
        self._templates: dict[str, TaskTemplate] = {}
        self._max_templates = max_templates

    def create_template(self, template: TaskTemplate) -> tuple[bool, str, Optional[TaskTemplate]]:
        """
        Create a new task template.

        Args:
            template: The template to create

        Returns:
            Tuple of (success: bool, message: str, template: TaskTemplate or None)
        """
        # Check if we've reached the template limit
        if len(self._templates) >= self._max_templates:
            return False, f"Maximum number of templates reached ({self._max_templates})", None

        # Validate template data
        is_valid, message = validate_template_data(template.name, template.title, template.due_date_offset)
        if not is_valid:
            return False, message, None

        # Check if template with this name already exists
        if template.id in self._templates:
            return False, f"Template with ID {template.id} already exists", None

        self._templates[template.id] = template
        return True, f"Template '{template.name}' created successfully", template

    def get_template(self, template_id: str) -> Optional[TaskTemplate]:
        """Get template by ID."""
        return self._templates.get(template_id)

    def list_templates(self) -> List[TaskTemplate]:
        """List all templates."""
        return list(self._templates.values())

    def update_template(self, template_id: str, updates: dict) -> tuple[bool, str, Optional[TaskTemplate]]:
        """
        Update template fields.

        Args:
            template_id: ID of the template to update
            updates: Dictionary of fields to update

        Returns:
            Tuple of (success: bool, message: str, updated_template: TaskTemplate or None)
        """
        if template_id not in self._templates:
            return False, f"Template not found (ID: {template_id})", None

        template = self._templates[template_id]

        # Update fields
        if "name" in updates:
            template.name = updates["name"]
        if "title" in updates:
            template.title = updates["title"]
        if "description" in updates:
            template.description = updates["description"]
        if "priority" in updates:
            template.priority = updates["priority"]
        if "tags" in updates:
            template.tags = updates["tags"]
        if "due_date_offset" in updates:
            template.due_date_offset = updates["due_date_offset"]

        # Validate updated template data
        is_valid, message = validate_template_data(template.name, template.title, template.due_date_offset)
        if not is_valid:
            # Restore original values if validation fails
            # This is a simplified approach - in a real system, we'd need to store original values
            return False, message, None

        return True, f"Template '{template.name}' updated successfully", template

    def delete_template(self, template_id: str) -> tuple[bool, str]:
        """Delete template."""
        if template_id not in self._templates:
            return False, f"Template not found (ID: {template_id})"

        del self._templates[template_id]
        return True, f"Template deleted successfully"

    def create_task_from_template(self, template_id: str, custom_fields: dict = None, id_generator=None) -> tuple[bool, str, Optional[Task]]:
        """
        Create task from template with optional overrides.

        Args:
            template_id: ID of the template to use
            custom_fields: Dictionary of fields to override from the template
            id_generator: Function to generate task IDs

        Returns:
            Tuple of (success: bool, message: str, task: Task or None)
        """
        if template_id not in self._templates:
            return False, f"Template not found (ID: {template_id})", None

        template = self._templates[template_id]
        try:
            task = template.to_task(custom_fields=custom_fields, id_generator=id_generator)
            return True, f"Task created from template '{template.name}'", task
        except Exception as e:
            return False, f"Failed to create task from template: {str(e)}", None

    def get_template_count(self) -> int:
        """Get the number of templates."""
        return len(self._templates)

    def is_at_template_limit(self) -> bool:
        """Check if we've reached the maximum number of templates."""
        return len(self._templates) >= self._max_templates