from datetime import datetime
from typing import List, Optional

from common.models import Todo
from common.repositories.factory import RepositoryFactory, RepoType


class TodoService:
    """
    Service for managing Todo operations.
    """
    def __init__(self, config):
        self.config = config
        self.repo_factory = RepositoryFactory(config)

    def get_todos_by_person_id(self, person_id: str) -> List[Todo]:
        """
        Get all todos for a specific person.
        """
        repo = self.repo_factory.get_repository(RepoType.TODO)
        todos = repo.get_todos_by_person_id(person_id)
        
        # Filter out todos with missing person_id (data integrity check)
        valid_todos = [todo for todo in todos if todo.person_id]
        return valid_todos

    def get_todos_by_person_id_and_status(self, person_id: str, is_completed: bool) -> List[Todo]:
        """
        Get todos for a specific person filtered by completion status.
        """
        repo = self.repo_factory.get_repository(RepoType.TODO)
        todos = repo.get_todos_by_person_id_and_status(person_id, is_completed)
        
        # Filter out todos with missing person_id (data integrity check)
        valid_todos = [todo for todo in todos if todo.person_id]
        return valid_todos

    def get_todo_by_id(self, todo_id: str) -> Optional[Todo]:
        """
        Get a todo by its ID.
        """
        repo = self.repo_factory.get_repository(RepoType.TODO)
        todo = repo.get_todo_by_id(todo_id)
        
        # Ensure the todo has a valid person_id
        if todo and not todo.person_id:
            # This todo has corrupted data, return None
            return None
            
        return todo

    def create_todo(self, person_id: str, title: str, description: Optional[str] = None, 
                   due_date: Optional[datetime] = None) -> Todo:
        """
        Create a new todo.
        """
        if not person_id:
            raise ValueError("person_id is required")
        if not title:
            raise ValueError("title is required")
            
        todo = Todo(
            person_id=person_id,
            title=title,
            description=description,
            is_completed=False,
            due_date=due_date
        )
        
        # Validate before saving
        todo.validate()
        
        repo = self.repo_factory.get_repository(RepoType.TODO)
        return repo.save_todo(todo)

    def update_todo(self, todo_id: str, title: Optional[str] = None, 
                   description: Optional[str] = None, is_completed: Optional[bool] = None,
                   due_date: Optional[datetime] = None) -> Optional[Todo]:
        """
        Update an existing todo.
        """
        repo = self.repo_factory.get_repository(RepoType.TODO)
        todo = repo.get_todo_by_id(todo_id)
        
        if not todo:
            return None
            
        # Ensure the todo has a valid person_id
        if not todo.person_id:
            raise ValueError("Cannot update todo with missing person_id")
            
        if title is not None:
            todo.title = title
            
        if description is not None:
            todo.description = description
            
        if is_completed is not None:
            todo.is_completed = is_completed
            
        if due_date is not None:
            todo.due_date = due_date
            
        # Validate before saving
        todo.validate()
        
        return repo.save_todo(todo)

    def delete_todo(self, todo_id: str) -> bool:
        """
        Delete a todo (mark as inactive).
        """
        repo = self.repo_factory.get_repository(RepoType.TODO)
        todo = repo.get_todo_by_id(todo_id)
        
        if not todo:
            return False
            
        # Ensure the todo has a valid person_id
        if not todo.person_id:
            raise ValueError("Cannot delete todo with missing person_id")
            
        todo.active = False
        repo.save_todo(todo)
        return True

    def toggle_todo_completion(self, todo_id: str) -> Optional[Todo]:
        """
        Toggle the completion status of a todo.
        """
        repo = self.repo_factory.get_repository(RepoType.TODO)
        todo = repo.get_todo_by_id(todo_id)
        
        if not todo:
            return None
            
        # Ensure the todo has a valid person_id
        if not todo.person_id:
            raise ValueError("Cannot toggle todo with missing person_id")
            
        todo.is_completed = not todo.is_completed
        return repo.save_todo(todo)
