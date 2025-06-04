from flask import Flask
from flask_cors import CORS
from controllers.user_controller import UserController
from controllers.decision_log_controller import DecisionLogController

def create_app():
    app = Flask(__name__)
    CORS(app, 
         supports_credentials=True, 
         resources={
             r"/api/*": {
                 "origins": [
                     "http://localhost:3000", # for User panel
                     "http://192.168.1.5:3000", # for User panel
                     "http://localhost:8000", # for Admin panel
                     "http://192.168.1.5:8000", # for Admin panel
                     "http://127.0.0.1:3000"
                 ]
             }
         })
    # Initialize controllers
    user_controller = UserController()
    decision_log_controller = DecisionLogController()

    # User routes
    app.add_url_rule('/api/users/register', 'user_register', user_controller.register, methods=['POST'])

    # Decision Log routes
    app.add_url_rule('/api/decisionLog/get_decision_logs_by_user_id', 'get_decision_logs_by_user_id', decision_log_controller.get_decision_logs_by_user_id, methods=['GET'])

    return app

if __name__ == "__main__":
    app = create_app()
    # app.run(host='0.0.0.0', port= 5000)
    app.run(debug=True, use_reloader=False, port= 5003)