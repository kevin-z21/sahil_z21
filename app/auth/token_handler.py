from functools import wraps
from flask import request, jsonify
import jwt
import datetime
from core.database import Database
from core.logger import Logger
from config.config import Config

def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            logger = Logger()
            token = request.headers.get("x-access-token")
            # logger.info(f"Token from request {token}")
            if not token:
                logger.error("Token is missing")
                return jsonify({"status": "error", "message": "Token is missing!"}), 401

            try:
                db = Database()
                config = Config()
                data = jwt.decode(
                    token, 
                    config.SECRET_KEY, 
                    algorithms=["HS256"]
                )
                current_user = db.fetch_one(
                    "SELECT * FROM users WHERE user_id = %s", 
                    (data["user_id"],)
                )
                # print("current_user from db", current_user)
                if not current_user:
                    raise ValueError("User not found")

                return f(args[0], current_user, *args[1:], **kwargs)
                
            except jwt.ExpiredSignatureError:
                logger.error("Token has expired")
                return jsonify({"status": "error", "message": "Token has expired!"}), 401
            except jwt.InvalidTokenError:
                logger.error("Invalid token")
                return jsonify({"status": "error", "message": "Token is invalid!"}), 401
            except Exception as e:
                logger.error(f"Token validation error: {str(e)}")
                return jsonify({"status": "error", "message": "Token validation failed!"}), 401

        return decorated

class TokenHandler:
    def __init__(self):
        self.db = Database()
        self.logger = Logger()
        self.config = Config()

    

    def generate_tokens(self, user_id):
        try:
            # Generate access token
            # print("user_id in token handler", user_id)
            self.logger.info(f"Generating token for user {user_id}")
            access_token = jwt.encode(
                {
                    "user_id": user_id,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
                },
                self.config.SECRET_KEY,
                algorithm="HS256"
            )

            # Generate refresh token
            refresh_token = jwt.encode(
                {
                    "user_id": user_id,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
                    
                },
                self.config.SECRET_KEY,
                algorithm="HS256"
            )

            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_in": 24 * 60 * 60  # 24 hours in seconds
                
            }

        except Exception as e:
            self.logger.error(f"Token generation failed: {str(e)}")
            raise
