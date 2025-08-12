from typing import List, Optional
import psycopg2
from datetime import datetime

from common.models import Todo
from common.repositories.base import BaseRepository
from common.app_config import get_config


class TodoRepository(BaseRepository):
    """
    Repository for Todo model with direct database queries to fix Rococo versioning issues.
    """
    MODEL = Todo

    def _get_db_connection(self):
        """Get direct database connection"""
        config = get_config()
        return psycopg2.connect(
            host=config.POSTGRES_HOST,
            port=config.POSTGRES_PORT,
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASSWORD,
            database=config.POSTGRES_DB
        )

    def _row_to_todo(self, row) -> Todo:
        """Convert database row to Todo object"""
        if not row:
            return None
        
        return Todo(
            entity_id=row[0],
            version=row[1],
            previous_version=row[2],
            active=row[3],
            changed_by_id=row[4],
            changed_on=row[5],
            person_id=row[6],
            title=row[7],
            description=row[8],
            is_completed=row[9],
            due_date=row[10]
        )

    def get_todos_by_person_id(self, person_id: str) -> List[Todo]:
        """
        Get all todos for a specific person.
        """
        if not person_id:
            return []
        
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT entity_id, version, previous_version, active, changed_by_id, changed_on,
                       person_id, title, description, is_completed, due_date
                FROM todo 
                WHERE person_id = %s AND active = true
                ORDER BY changed_on DESC
            """, (person_id,))
            
            rows = cursor.fetchall()
            todos = [self._row_to_todo(row) for row in rows]
            return [todo for todo in todos if todo]  # Filter out None values
            
        finally:
            cursor.close()
            conn.close()

    def get_todos_by_person_id_and_status(self, person_id: str, is_completed: bool) -> List[Todo]:
        """
        Get todos for a specific person filtered by completion status.
        """
        if not person_id:
            return []
        
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT entity_id, version, previous_version, active, changed_by_id, changed_on,
                       person_id, title, description, is_completed, due_date
                FROM todo 
                WHERE person_id = %s AND active = true AND is_completed = %s
                ORDER BY changed_on DESC
            """, (person_id, is_completed))
            
            rows = cursor.fetchall()
            todos = [self._row_to_todo(row) for row in rows]
            return [todo for todo in todos if todo]  # Filter out None values
            
        finally:
            cursor.close()
            conn.close()

    def get_todo_by_id(self, entity_id: str) -> Optional[Todo]:
        """
        Get a todo by its ID.
        """
        if not entity_id:
            return None
        
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT entity_id, version, previous_version, active, changed_by_id, changed_on,
                       person_id, title, description, is_completed, due_date
                FROM todo 
                WHERE entity_id = %s AND active = true
            """, (entity_id,))
            
            row = cursor.fetchone()
            return self._row_to_todo(row)
            
        finally:
            cursor.close()
            conn.close()

    def save_todo(self, todo: Todo) -> Todo:
        """
        Save a todo to the database.
        """
        if not todo:
            raise ValueError("Todo object is required")
            
        # Validate the todo before saving
        todo.validate()
        
        # For now, use the original Rococo save method for saving
        # The issue is only with retrieval, not with saving
        return self.save(todo)
