from flask import jsonify, request, send_from_directory
from controllers.base_controller import BaseController
from services.complain_service import ComplainService
import os

class ComplainController(BaseController):
    def __init__(self):
        self.complain_service = ComplainService()

    def save_complain(self):
        try:
            # Extract form data
            description = request.form.get("description")
            predictedCategory = request.form.get("predictedCategory")
            predictedSubcategory = request.form.get("predictedSubcategory")
            manualCategory = request.form.get("manualCategory")
            manualSubcategory = request.form.get("manualSubcategory")
            pincode = request.form.get("pincode")
            state = request.form.get("state")
            mobile_no = request.form.get("mobileNo")
            predictedAudioCategory = request.form.get("predictedAudioCategory")
            predictedImageCategory = request.form.get("predictedImageCategory")
            predictedAudioSubcategory = request.form.get("predictedAudioSubcategory")
            predictedImageSubcategory = request.form.get("predictedImageSubcategory")

            uploaded_files = request.files.getlist("uploadedFiles")
            audio_file = request.files.get("audioFile")

            # Prepare data dictionary
            complain_data = {
                "description": description,
                "predictedCategory": predictedCategory,
                "predictedSubcategory": predictedSubcategory,
                "manualCategory": manualCategory,
                "manualSubcategory": manualSubcategory,
                "state": state,
                "pincode": pincode,
                "mobileNo": mobile_no,
                "uploadedFiles": uploaded_files,
                "audioFile": audio_file,
                "predictedAudioCategory" : predictedAudioCategory,
                "predictedImageCategory" : predictedImageCategory,
                "predictedAudioSubcategory" : predictedAudioSubcategory,
                "predictedImageSubcategory" : predictedImageSubcategory,
            }

            # Call service layer
            response = self.complain_service.save_complain(complain_data)
            return jsonify(response), 201 if response["status"] == "success" else 500

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    
    def get_all_complains(self):
        try:
            complains = self.complain_service.get_all_complains()
            return jsonify({
                "status": "success", 
                "message": "Complains fetched successfully",
                "data": complains
            }), 201
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
        
    def get_complain_by_id(self):
        try:
            complain_id = request.args.get("complain_id")
            if not complain_id:
                raise ValueError("complain_id parameter is required")
            complain = self.complain_service.get_complain_by_id(complain_id)
            return jsonify({
                "status": "success", 
                "message": "Complain fetched successfully",
                "data": complain
            }), 201
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
        
    # def get_uploaded_file(self):
    #     try:
    #         complain_id = request.args.get("complain_id")
    #         filename = request.args.get("filename")
    #         file_path = self.complain_service.get_uploaded_file(complain_id, filename)
    #         return file_path
    #     except Exception as e:
    #         return jsonify({"status": "error", "message": str(e)}), 500
    
    def get_uploaded_file(self):
        try:
            # complain_id = request.args.get("complain_id")
            filename = request.args.get("filename")
            # upload_folder = "uploads"
            directory, file_name = os.path.split(filename)
            return send_from_directory(directory, file_name)
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
        