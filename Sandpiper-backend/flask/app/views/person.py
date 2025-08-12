from flask_restx import Namespace, Resource
from flask import request
from app.helpers.response import get_success_response, get_failure_response, parse_request_body, validate_required_fields
from app.helpers.decorators import login_required, token_required
from common.app_config import config
from common.services import PersonService

# Create the person blueprint
person_api = Namespace('person', description="Person-related APIs")


@person_api.route('/me')
class Me(Resource):
    
    @login_required()
    def get(self, person):
        return get_success_response(person=person)
    
    @token_required
    @person_api.doc(security='Bearer')
    def put(self):
        """
        Update the current user's profile
        """
        parsed_body = parse_request_body(request, ['first_name', 'last_name'])
        validate_required_fields(parsed_body, ['first_name', 'last_name'])
        
        person_service = PersonService(config)
        person = person_service.get_person_by_id(request.user_id)
        
        if not person:
            return get_failure_response(message="Person not found.")
        
        person.first_name = parsed_body['first_name']
        person.last_name = parsed_body['last_name']
        
        updated_person = person_service.save_person(person)
        
        return get_success_response(
            person=updated_person.as_dict(),
            message="Profile updated successfully."
        )
