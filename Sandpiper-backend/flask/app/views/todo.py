from datetime import datetime
from flask_restx import Namespace, Resource, fields
from flask import request, g

from app.helpers.decorators import token_required
from app.helpers.response import get_success_response, get_failure_response, parse_request_body, validate_required_fields
from common.app_config import config
from common.services import TodoService

# Create the todo namespace
todo_api = Namespace('todo', description="Todo related APIs")

# Define models for request/response validation
todo_model = todo_api.model('Todo', {
    'entity_id': fields.String(description='Todo ID'),
    'title': fields.String(required=True, description='Todo title'),
    'description': fields.String(description='Todo description'),
    'is_completed': fields.Boolean(description='Completion status'),
    'due_date': fields.DateTime(description='Due date'),
    'changed_on': fields.DateTime(description='Last updated date')
})

todo_create_model = todo_api.model('TodoCreate', {
    'title': fields.String(required=True, description='Todo title'),
    'description': fields.String(description='Todo description'),
    'due_date': fields.DateTime(description='Due date')
})

todo_update_model = todo_api.model('TodoUpdate', {
    'title': fields.String(description='Todo title'),
    'description': fields.String(description='Todo description'),
    'is_completed': fields.Boolean(description='Completion status'),
    'due_date': fields.DateTime(description='Due date')
})


@todo_api.route('/')
class TodoList(Resource):
    @token_required
    @todo_api.doc(security='Bearer')
    @todo_api.doc(params={'status': 'Filter by completion status (completed, active, all)'})
    def get(self):
        """
        Get all todos for the current user
        """
        status = request.args.get('status', 'all')
        
        todo_service = TodoService(config)
        
        try:
            if status == 'completed':
                todos = todo_service.get_todos_by_person_id_and_status(g.current_user_id, True)
            elif status == 'active':
                todos = todo_service.get_todos_by_person_id_and_status(g.current_user_id, False)
            else:
                todos = todo_service.get_todos_by_person_id(g.current_user_id)
            
            # Filter out any todos with missing data
            valid_todos = []
            for todo in todos:
                if todo.person_id and todo.title:  # Only include valid todos
                    valid_todos.append(todo)
            
            return get_success_response(todos=[todo.as_dict() for todo in valid_todos])
        except Exception as e:
            from common.app_logger import logger
            logger.error(f"Error fetching todos: {str(e)}")
            return get_failure_response(message="Failed to fetch todos")

    @token_required
    @todo_api.doc(security='Bearer')
    @todo_api.expect(todo_create_model)
    def post(self):
        """
        Create a new todo
        """
        try:
            parsed_body = parse_request_body(request, ['title', 'description', 'due_date'])
            validate_required_fields(parsed_body, ['title'])
            
            todo_service = TodoService(config)
            
            # Parse due_date if provided
            due_date = None
            if parsed_body.get('due_date'):
                try:
                    due_date = datetime.fromisoformat(parsed_body['due_date'])
                except (ValueError, TypeError):
                    return get_failure_response(message="Invalid due date format. Use ISO format (YYYY-MM-DDTHH:MM:SS).")
            
            todo = todo_service.create_todo(
                person_id=g.current_user_id,
                title=parsed_body['title'],
                description=parsed_body.get('description'),
                due_date=due_date
            )
            
            return get_success_response(todo=todo.as_dict(), message="Todo created successfully.")
        except ValueError as e:
            return get_failure_response(message=str(e))
        except Exception as e:
            from common.app_logger import logger
            logger.error(f"Error creating todo: {str(e)}")
            return get_failure_response(message="Failed to create todo")


@todo_api.route('/<string:todo_id>')
class TodoItem(Resource):
    @token_required
    @todo_api.doc(security='Bearer')
    def get(self, todo_id):
        """
        Get a specific todo by ID
        """
        from common.app_logger import logger
        
        try:
            todo_service = TodoService(config)
            todo = todo_service.get_todo_by_id(todo_id)
            
            if not todo:
                return get_failure_response(message="Todo not found.")
            
            # Debug logging
            logger.info(f"Todo person_id: {todo.person_id}, current_user_id: {g.current_user_id}")
            logger.info(f"Todo data: {todo.as_dict()}")
                
            if not todo.person_id:
                return get_failure_response(message="Todo data is corrupted (missing person_id).")
                
            if todo.person_id != g.current_user_id:
                return get_failure_response(message="You don't have permission to access this todo.")
                
            return get_success_response(todo=todo.as_dict())
        except Exception as e:
            logger.error(f"Error fetching todo: {str(e)}")
            return get_failure_response(message="Failed to fetch todo")

    @token_required
    @todo_api.doc(security='Bearer')
    @todo_api.expect(todo_update_model)
    def put(self, todo_id):
        """
        Update a specific todo
        """
        try:
            todo_service = TodoService(config)
            todo = todo_service.get_todo_by_id(todo_id)
            
            if not todo:
                return get_failure_response(message="Todo not found.")
                
            if not todo.person_id:
                return get_failure_response(message="Todo data is corrupted (missing person_id).")
                
            if todo.person_id != g.current_user_id:
                return get_failure_response(message="You don't have permission to update this todo.")
            
            parsed_body = parse_request_body(request, ['title', 'description', 'is_completed', 'due_date'])
            
            # Parse due_date if provided
            due_date = None
            if parsed_body.get('due_date'):
                try:
                    due_date = datetime.fromisoformat(parsed_body['due_date'])
                except (ValueError, TypeError):
                    return get_failure_response(message="Invalid due date format. Use ISO format (YYYY-MM-DDTHH:MM:SS).")
            
            updated_todo = todo_service.update_todo(
                todo_id=todo_id,
                title=parsed_body.get('title'),
                description=parsed_body.get('description'),
                is_completed=parsed_body.get('is_completed'),
                due_date=due_date
            )
            
            return get_success_response(todo=updated_todo.as_dict(), message="Todo updated successfully.")
        except ValueError as e:
            return get_failure_response(message=str(e))
        except Exception as e:
            from common.app_logger import logger
            logger.error(f"Error updating todo: {str(e)}")
            return get_failure_response(message="Failed to update todo")

    @token_required
    @todo_api.doc(security='Bearer')
    def delete(self, todo_id):
        """
        Delete a specific todo
        """
        try:
            todo_service = TodoService(config)
            todo = todo_service.get_todo_by_id(todo_id)
            
            if not todo:
                return get_failure_response(message="Todo not found.")
                
            if not todo.person_id:
                return get_failure_response(message="Todo data is corrupted (missing person_id).")
                
            if todo.person_id != g.current_user_id:
                return get_failure_response(message="You don't have permission to delete this todo.")
            
            success = todo_service.delete_todo(todo_id)
            
            if success:
                return get_success_response(message="Todo deleted successfully.")
            else:
                return get_failure_response(message="Failed to delete todo.")
        except ValueError as e:
            return get_failure_response(message=str(e))
        except Exception as e:
            from common.app_logger import logger
            logger.error(f"Error deleting todo: {str(e)}")
            return get_failure_response(message="Failed to delete todo")


@todo_api.route('/<string:todo_id>/toggle')
class TodoToggle(Resource):
    @token_required
    @todo_api.doc(security='Bearer')
    def put(self, todo_id):
        """
        Toggle the completion status of a todo
        """
        try:
            todo_service = TodoService(config)
            todo = todo_service.get_todo_by_id(todo_id)
            
            if not todo:
                return get_failure_response(message="Todo not found.")
                
            if not todo.person_id:
                return get_failure_response(message="Todo data is corrupted (missing person_id).")
                
            if todo.person_id != g.current_user_id:
                return get_failure_response(message="You don't have permission to update this todo.")
            
            updated_todo = todo_service.toggle_todo_completion(todo_id)
            
            return get_success_response(
                todo=updated_todo.as_dict(), 
                message=f"Todo marked as {'completed' if updated_todo.is_completed else 'active'}."
            )
        except ValueError as e:
            return get_failure_response(message=str(e))
        except Exception as e:
            from common.app_logger import logger
            logger.error(f"Error toggling todo: {str(e)}")
            return get_failure_response(message="Failed to toggle todo")
