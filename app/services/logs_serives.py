from datetime import datetime
from services.base_service import BaseService
from repositories.logs_repository import LogsRepository

class LogsService(BaseService):

    def __init__(self):
        self.logs_repo = LogsRepository()

    def get_all_logs(self):
        logs = self.logs_repo.get_all_logs()
        return logs

    def add_log(self, log):
        # If the log contains an array of logs, add timestamp to each entry
        if "logs" in log:
            logs_list = log["logs"]
            current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Add timestamp to each log entry and remove the outer timestamp
            for entry in logs_list:
                entry["timestamp"] = current_timestamp
                # Now pass each log entry to the repository one by one
                response = self.logs_repo.add_log(entry)  # Pass single log entry here
                # You can collect responses if needed, e.g., append to a list
            # Remove the outer timestamp property, if it exists.
            log.pop("timestamp", None)
        else:
            # If the log is a single log entry, just pass it directly to the repository
            response = self.logs_repo.add_log(log)
        
        return response