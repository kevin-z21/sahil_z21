from core.logger import Logger
import json
import os


class ReportsRepository:
    def __init__(self):
        self.logger = Logger()
        self.file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "reports.json")

    def get_all_reports(self):
        try:
            with open(self.file_path, "r") as f:
                reports = json.load(f)
            return reports
        except Exception as e:
            self.logger.error(f"Error in get_all_reports: {str(e)}")
            return {"error": str(e)}
