import pandas as pd
from flask import Flask
from flask_cors import CORS
from controllers.complain_controller import ComplainController
from controllers.logs_controller import LogsController

def create_app():
    app = Flask(__name__)
    CORS(app, 
         supports_credentials=True, 
         resources={
             r"/api/*": {
                 "origins": [
                     "http://localhost:3000", # for User panel
                     "http://192.168.1.16:3000", # for User panel
                     "http://localhost:8000", # for Admin panel
                     "http://192.168.1.16:8000", # for Admin panel
                     "http://127.0.0.1:3000",
                 ]
             }
         })
    # Initialize controllers
    complain_controller = ComplainController()
    logs_controller = LogsController()

    # Complain routes
    app.add_url_rule('/api/complains/get_all_complains', 'get_all_complains', complain_controller.get_all_complains, methods=['GET'])
    app.add_url_rule('/api/complains/get_complain_by_id', 'get_complain_by_id', complain_controller.get_complain_by_id, methods=['GET'])
    app.add_url_rule('/api/complains/get_uploaded_file', 'get_uploaded_file', complain_controller.get_uploaded_file, methods=['GET'])
    app.add_url_rule('/api/complains/save_complain', 'save_complain', complain_controller.save_complain, methods=['POST'])

    # Logs routes
    app.add_url_rule('/api/logs/get_all_logs', 'get_all_logs', logs_controller.get_all_logs, methods=['GET'])
    app.add_url_rule('/api/logs/add_log', 'add_log', logs_controller.add_log, methods=['POST'])

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, use_reloader=False, port=5005)