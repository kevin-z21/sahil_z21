from services.base_service import BaseService
from repositories.decision_log_repository import DecisionLogRepository

class DecisionLogService(BaseService):

    def __init__(self):
        self.decision_log_repo = DecisionLogRepository()

    def get_decision_logs_by_user_id(self, user_id):
        try:
            # Check if user exists
            existing_user = self.decision_log_repo.find_by_user_id(user_id)
            if not existing_user:
                return {
                    "status": "error",
                    "message": f"User with ID {user_id} not found",
                    "data": None
                }

            # Get decision logs
            try:
                decision_logs = self.decision_log_repo.get_decision_logs_by_user_id(user_id)
                return  decision_logs
            except Exception as e:
                return {
                    "status": "error",
                    "message": f"Error retrieving decision logs: {str(e)}",
                    "data": None
                }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Error checking user existence: {str(e)}",
                "data": None
            }
 