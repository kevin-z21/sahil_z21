from flask import jsonify, request, send_from_directory
from controllers.base_controller import BaseController
from services.logs_serives import LogsService

class LogsController(BaseController):
    def __init__(self):
        self.logs_service = LogsService()

    def get_all_logs(self):
        try:
            logs = self.logs_service.get_all_logs()
            return jsonify(logs)
        except Exception as e:
            return jsonify({"error": str(e)})
        
    def add_log(self):
        try:
            log = request.json
            response = self.logs_service.add_log(log)
            return jsonify(response)
        except Exception as e:
            return jsonify({"error": str(e)})