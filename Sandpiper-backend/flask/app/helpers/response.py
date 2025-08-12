from flask import current_app as app
from common.helpers.exceptions import InputValidationError


def parse_request_body(request, keys, default_value=None):
    try:
        request_body = request.get_json(force=True)
        return {key: request_body.get(key, default_value) for key in keys}
    except Exception as e:
        raise InputValidationError(f"Error parsing request body: {str(e)}")


def validate_required_fields(data, required_fields=None):
    """
    Validate that required fields exist and are not empty.
    
    Args:
        data: Dictionary containing the data to validate
        required_fields: List of field names that are required (optional)
    """
    if required_fields:
        # Validate specific required fields
        for field in required_fields:
            if field not in data:
                raise InputValidationError(f"'{field}' is required.")
            if not data[field] or not str(data[field]).strip():
                raise InputValidationError(f"'{field}' is required and cannot be empty.")
    else:
        # Validate all fields in the data (backward compatibility)
        for field, value in data.items():
            if not value or not str(value).strip():
                raise InputValidationError(f"'{field}' is required and cannot be empty.")


def _get_response(data, status_code=200):
    response = app.response_class(
        response=app.json.dumps(data),
        status=status_code,
        mimetype=app.config['MIME_TYPE']
    )
    return response


def get_failure_response(message, status_code=200):
    response = _get_response(dict(success=False, message=message), status_code)
    return response


def get_success_response(status_code=200, **data):
    response = _get_response(dict(success=True, **data), status_code)
    return response
