import json
import os
from datetime import datetime
from services.base_service import BaseService
from repositories.complain_repository import ComplainRepository

class ComplainService(BaseService):

    def __init__(self):
        self.complain_repo = ComplainRepository()

    def save_complain(self, data):
        try:
            # Generate complainId
            today_date = datetime.today().strftime("%Y%m%d")
            complain_id = self.complain_repo.generate_complain_id(today_date)

            # Create directory for storing files
            upload_dir = os.path.join("uploads", complain_id)
            os.makedirs(upload_dir, exist_ok=True)

            # Save uploaded files
            uploaded_files_paths = []
            for file in data["uploadedFiles"]:
                file_path = os.path.join(upload_dir, file.filename)
                file.save(file_path)
                uploaded_files_paths.append(file_path)

            # Save audio file
            audio_file_path = None
            if data["audioFile"]:
                audio_file_path = os.path.join(upload_dir, data["audioFile"].filename)
                data["audioFile"].save(audio_file_path)

            # Prepare complaint data
            complain_data = {
                "complainId": complain_id,
                "description": data["description"],
                "predictedCategory": data["predictedCategory"],
                "predictedSubcategory": data["predictedSubcategory"],
                "manualCategory": data["manualCategory"],
                "manualSubcategory": data["manualSubcategory"],
                "state": data["state"],
                "pincode": data["pincode"],
                "mobileNo": data["mobileNo"],
                "uploadedFiles": uploaded_files_paths,
                "audioFile": audio_file_path,
                "predictedAudioCategory": data.get("predictedAudioCategory", None),
                "predictedImageCategory": data.get("predictedImageCategory", None),
                "predictedAudioSubcategory": data.get("predictedAudioSubcategory", None),
                "predictedImageSubcategory": data.get("predictedImageSubcategory", None),
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            # Save complaint to repository
            result = self.complain_repo.save_complain(complain_data)
            return result

        except Exception as e:
            return {
                "status": "error",
                "message": f"Error saving complaint: {str(e)}",
                "data": None
            }
        
    def get_all_complains(self):
        try:
            complains = self.complain_repo.get_all_complains()
            return complains
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error retrieving complains: {str(e)}",
                "data": None
            }   
        
    def get_complain_by_id(self, complain_id):
        try:
            complain = self.complain_repo.get_complain_by_id(complain_id)
            return complain
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error retrieving complain: {str(e)}",
                "data": None
            }
        
    def get_uploaded_file(self, complain_id, filename):
        try:
            file_path = self.complain_repo.get_uploaded_file(complain_id, filename)
            return file_path
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error retrieving file: {str(e)}",
                "data": None
            }