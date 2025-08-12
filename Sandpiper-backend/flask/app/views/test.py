from flask_restx import Namespace, Resource, fields
from flask import request
from app.helpers.response import get_success_response, get_failure_response, parse_request_body, validate_required_fields
from common.app_config import config
from common.services import AuthService, PersonService
from common.models import Person, Email, LoginMethod, Organization, PersonOrganizationRole
from common.models.login_method import LoginMethodType
from common.services import EmailService, LoginMethodService, OrganizationService, PersonOrganizationRoleService

# Create the test namespace - only available in non-production environments
test_api = Namespace('test', description="Test helper APIs (non-production only)")

@test_api.route('/create_user')
class CreateTestUser(Resource):
    @test_api.expect({
        'type': 'object',
        'properties': {
            'first_name': {'type': 'string'},
            'last_name': {'type': 'string'},
            'email_address': {'type': 'string'},
            'password': {'type': 'string'}
        }
    })
    def post(self):
        """
        Create a test user with a custom password (non-production only)
        
        This endpoint bypasses the email verification flow for testing purposes.
        """
        # Only allow in non-production environments
        if config.APP_ENV == "production":
            return get_failure_response(message="Test endpoints not available in production", status_code=404)
        
        try:
            parsed_body = parse_request_body(request, ['first_name', 'last_name', 'email_address', 'password'])
            validate_required_fields(parsed_body)

            person_service = PersonService(config)
            email_service = EmailService(config)
            login_method_service = LoginMethodService(config)
            organization_service = OrganizationService(config)
            person_organization_role_service = PersonOrganizationRoleService(config)

            # Check if email already exists
            existing_email = email_service.get_email_by_email_address(parsed_body['email_address'])
            if existing_email:
                return get_failure_response(message="Email address already registered")

            # Create person
            person = Person(
                first_name=parsed_body['first_name'], 
                last_name=parsed_body['last_name']
            )
            person = person_service.save_person(person)

            # Create email
            email = Email(person_id=person.entity_id, email=parsed_body['email_address'])
            email = email_service.save_email(email)

            # Create organization
            organization = Organization(
                name=f"{parsed_body['first_name']}'s Test Organization"
            )
            organization = organization_service.save_organization(organization)

            # Create login method with custom password
            login_method = LoginMethod(
                method_type=LoginMethodType.EMAIL_PASSWORD,
                raw_password=parsed_body['password'],
                person_id=person.entity_id,
                email_id=email.entity_id
            )
            login_method = login_method_service.save_login_method(login_method)

            # Create person-organization role
            person_organization_role = PersonOrganizationRole(
                person_id=person.entity_id,
                organization_id=organization.entity_id,
                role="admin"
            )
            person_organization_role_service.save_person_organization_role(person_organization_role)

            return get_success_response(
                message="Test user created successfully",
                user_id=person.entity_id,
                email=email.email
            )

        except Exception as e:
            from common.app_logger import logger
            logger.error(f"Error creating test user: {str(e)}")
            return get_failure_response(message=f"Failed to create test user: {str(e)}")


@test_api.route('/debug_todos')
class DebugTodos(Resource):
    def get(self):
        """
        Debug endpoint to check todos in database
        """
        if config.APP_ENV == "production":
            return get_failure_response(message="Test endpoints not available in production", status_code=404)
        
        try:
            from common.services import TodoService
            from common.repositories.factory import RepositoryFactory, RepoType
            import psycopg2
            
            # Get database connection info
            db_config = config
            
            # Connect directly to PostgreSQL
            conn = psycopg2.connect(
                host=db_config.POSTGRES_HOST,
                port=db_config.POSTGRES_PORT,
                user=db_config.POSTGRES_USER,
                password=db_config.POSTGRES_PASSWORD,
                database=db_config.POSTGRES_DB
            )
            
            cursor = conn.cursor()
            
            # Check what tables exist
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_name LIKE '%todo%'")
            tables = cursor.fetchall()
            
            # Execute raw SQL to see what's in the database
            cursor.execute("SELECT entity_id, person_id, title, active, is_completed, changed_on, version FROM todo ORDER BY changed_on DESC LIMIT 10")
            todo_rows = cursor.fetchall()
            
            # Also check the audit table
            cursor.execute("SELECT entity_id, person_id, title, active, is_completed, changed_on, version FROM todo_audit ORDER BY changed_on DESC LIMIT 10")
            audit_rows = cursor.fetchall()
            
            # Convert to list of dicts
            result = []
            for row in todo_rows:
                result.append({
                    "entity_id": row[0],
                    "person_id": row[1], 
                    "title": row[2],
                    "active": row[3],
                    "is_completed": row[4],
                    "changed_on": str(row[5]),
                    "version": row[6]
                })
            
            audit_result = []
            for row in audit_rows:
                audit_result.append({
                    "entity_id": row[0],
                    "person_id": row[1], 
                    "title": row[2],
                    "active": row[3],
                    "is_completed": row[4],
                    "changed_on": str(row[5]),
                    "version": row[6]
                })
            
            cursor.close()
            conn.close()
            
            return get_success_response(
                message="Debug data retrieved",
                tables=tables,
                todos_in_main_table=result,
                todos_in_audit_table=audit_result
            )
            
        except Exception as e:
            return get_failure_response(message=f"Debug failed: {str(e)}")


@test_api.route('/health')
class TestHealth(Resource):
    def get(self):
        """
        Test endpoint health check
        """
        if config.APP_ENV == "production":
            return get_failure_response(message="Test endpoints not available in production", status_code=404)
        
        return get_success_response(
            message="Test endpoints are available",
            environment=config.APP_ENV
        )
