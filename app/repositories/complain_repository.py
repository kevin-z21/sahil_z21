from core.logger import Logger
import json
import os


class ComplainRepository:
    def __init__(self):
        self.logger = Logger()
        self.file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "complains.json")

    def generate_complain_id(self, today_date):
        try:
            # Load existing complaints
            if os.path.exists(self.file_path):
                with open(self.file_path, "r", encoding="utf-8") as file:
                    try:
                        existing_complaints = json.load(file)
                        if not isinstance(existing_complaints, list):
                            existing_complaints = []  # Ensure it's a list
                    except json.JSONDecodeError:
                        existing_complaints = []
            else:
                existing_complaints = []

            # Count complaints for today
            daily_count = sum(1 for c in existing_complaints if c.get("complainId", "").startswith(f"C{today_date}")) + 1

            # Generate new complainId
            return f"C{today_date}{daily_count:06d}"  # Ensures 6-digit count (e.g., 000001, 000002)

        except Exception as e:
            raise Exception(f"Error generating complainId: {str(e)}")

    def save_complain(self, data):
        try:
            # Load existing complaints
            if os.path.exists(self.file_path):
                with open(self.file_path, "r", encoding="utf-8") as file:
                    try:
                        existing_data = json.load(file)
                        if not isinstance(existing_data, list):
                            existing_data = []
                    except json.JSONDecodeError:
                        existing_data = []
            else:
                existing_data = []

            # Append new complaint
            existing_data.append(data)

            # Save updated data
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(existing_data, file, indent=4, ensure_ascii=False)

            return {"status": "success", "message": "Complaint saved successfully", "data": data}

        except Exception as e:
            return {"status": "error", "message": f"Error saving complaint: {str(e)}", "data": None}

    def get_all_complains(self):
        try:
            # Get the absolute path of the data folder
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(base_dir, "data", "complains.json")

            # Load existing data if file exists
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as file:
                    try:
                        existing_data = json.load(file)
                        if not isinstance(existing_data, list):
                            existing_data = []  # Ensure it's a list
                    except json.JSONDecodeError:
                        existing_data = []
            else:
                existing_data = []

            # Sort the data by a field in descending order (e.g., by 'date' or 'id')
            # Change the key (e.g., 'date') to whatever field you want to sort by
            sorted_data = sorted(existing_data, key=lambda x: x.get("date", ""), reverse=True)

            return {"status": "success", "message": "Data fetched successfully", "data": sorted_data}
        
        except Exception as e:
            self.logger.error(f"Error fetching complaints: {str(e)}")
            raise Exception(f"Failed to fetch complaints: {str(e)}")

    def get_complain_by_id(self, complain_id):
        try:
            # Get the absolute path of the data folder
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(base_dir, "data", "complains.json")

            # Load existing data if file exists
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as file:
                    try:
                        existing_data = json.load(file)
                        if not isinstance(existing_data, list):
                            existing_data = []  # Ensure it's a list
                    except json.JSONDecodeError:
                        existing_data = []
            else:
                existing_data = []

            # Find complaint by ID
            complain = next((c for c in existing_data if c.get("complainId") == complain_id), None)

            if complain:
                return {"status": "success", "message": "Complaint fetched successfully", "data": complain}
            else:
                return {"status": "error", "message": "Complaint not found", "data": None}
        
        except Exception as e:
            self.logger.error(f"Error fetching complaint: {str(e)}")
            raise Exception(f"Failed to fetch complaint: {str(e)}")
        
    def get_uploaded_file(self, complain_id, filename):
        try:
            # Get the absolute path of the data folder
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(base_dir, "data", "complains.json")

            # Load existing data if file exists
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as file:
                    try:
                        existing_data = json.load(file)
                        if not isinstance(existing_data, list):
                            existing_data = []  # Ensure it's a list
                    except json.JSONDecodeError:
                        existing_data = []
            else:
                existing_data = []
        
            # Find complaint by ID
            complain = next((c for c in existing_data if c.get("complainId") == complain_id), None)

            if complain:
                # Get file path
                file_path = os.path.join(base_dir, "uploads", complain_id, filename)
                return file_path
            else:
                return None
        
        except Exception as e:
            self.logger.error(f"Error fetching uploaded file: {str(e)}")
            raise Exception(f"Failed to fetch uploaded file: {str(e)}")