from datetime import datetime
from typing import Optional

from rococo.models.versioned_model import VersionedModel


class Todo(VersionedModel):
    """
    Todo model for storing task information.
    """
    def __init__(
        self,
        entity_id: Optional[str] = None,
        version: Optional[str] = None,
        previous_version: Optional[str] = None,
        active: bool = True,
        changed_by_id: Optional[str] = None,
        changed_on: Optional[datetime] = None,
        person_id: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        is_completed: bool = False,
        due_date: Optional[datetime] = None,
    ):
        super().__init__(
            entity_id=entity_id,
            version=version,
            previous_version=previous_version,
            active=active,
            changed_by_id=changed_by_id,
            changed_on=changed_on,
        )
        self.person_id = person_id
        self.title = title
        self.description = description
        self.is_completed = is_completed
        self.due_date = due_date

    def validate(self):
        """Validate the todo model before saving"""
        if not self.person_id:
            raise ValueError("person_id is required")
        if not self.title:
            raise ValueError("title is required")
        return True

    def as_dict(self, convert_datetime_to_iso_string=True, convert_uuids=False, export_properties=None):
        """
        Convert the Todo object to a dictionary.
        
        Args:
            convert_datetime_to_iso_string: Whether to convert datetime fields to ISO strings
            convert_uuids: Whether to convert UUID fields to strings
            export_properties: Additional properties to export (ignored for now)
        """
        base_dict = super().as_dict(
            convert_datetime_to_iso_string=convert_datetime_to_iso_string,
            convert_uuids=convert_uuids
        )
        
        todo_dict = {
            "person_id": self.person_id,
            "title": self.title or "",  # Ensure title is never null
            "description": self.description or "",  # Ensure description is never null
            "is_completed": self.is_completed,
        }
        
        # Handle due_date based on the convert_datetime_to_iso_string parameter
        if self.due_date:
            if convert_datetime_to_iso_string:
                todo_dict["due_date"] = self.due_date.isoformat()
            else:
                todo_dict["due_date"] = self.due_date
        else:
            todo_dict["due_date"] = None
            
        return {**base_dict, **todo_dict}