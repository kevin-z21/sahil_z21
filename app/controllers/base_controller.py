from flask import jsonify

class BaseController:
    def success_response(self, data=None, message="Success", status_code=200):
        response = {
            "success": True,
            "message": message
        }
        if data is not None:
            response["data"] = data
        return jsonify(response), status_code

    def error_response(self, message="Error", status_code=400):
        return jsonify({
            "success": False,
            "message": message
        }), status_code
    
    def send_unauthorized_response(self, message="Unauthorized access"):
        return self.error_response(message, 401)

    def send_forbidden_response(self, message="Forbidden"):
        return self.error_response(message, 403)

    def send_not_found_response(self, message="Resource not found"):
        return self.error_response(message, 404)

    def send_server_error_response(self, message="Internal server error"):
        return self.error_response(message, 500)

    def send_validation_error_response(self, message="Validation failed"):
        return self.error_response(message, 422)

    def send_bad_request_response(self, message="Bad request"):
        return self.error_response(message, 400)
    
    def send_credentials_not_found_response(self, message="API credentials not found"):
        return self.error_response(message, 409) # Conflict status code