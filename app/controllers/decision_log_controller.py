from flask import jsonify
from controllers.base_controller import BaseController
from services.decision_log_service import DecisionLogService
from auth.token_handler import token_required

class DecisionLogController(BaseController):
    def __init__(self):
        self.decision_log_service = DecisionLogService()
    
    @token_required
    def get_decision_logs_by_user_id(self, current_user):
        user_id = current_user["user_id"]
        # Validate user_id presence
        if not user_id:
            return self.error_response("User ID is required")
        
        try:
            decision_logs = self.decision_log_service.get_decision_logs_by_user_id(user_id)
            return jsonify({
                "status": "success", 
                "message": "Decision log fetched successfully",
                "data": decision_logs
            }), 201
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
