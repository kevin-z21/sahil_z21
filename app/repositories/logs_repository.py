from core.logger import Logger
import json
import os


class LogsRepository:
    def __init__(self):
        self.logger = Logger()
        self.file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "logs.json")

    def get_all_logs(self):
        try:
            with open(self.file_path, "r") as f:
                logs = json.load(f)
             # Sort the logs by 'date' in descending order
            sorted_logs = sorted(logs, key=lambda x: x.get("timestamp", ""), reverse=True)
            
            return sorted_logs
        
        except Exception as e:
            self.logger.error(f"Error in get_all_logs: {str(e)}")
            return {"error": str(e)}
        
    def add_log(self, log):
        try:
            print("log :: ", log)
            logs = self.get_all_logs()
            logs.append(log)
            with open(self.file_path, "w") as f:
                json.dump(logs, f, indent=4)
            return {"message": "Log added successfully"}
        except Exception as e:
            self.logger.error(f"Error in add_log: {str(e)}")
            return {"error": str(e)}