# import logging
# import watchtower
# import boto3
# from config.config import Config

# class Logger:
#     _instance = None
#     _initialized = False
#     _loggingEnabled = True

#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super(Logger, cls).__new__(cls)
#         return cls._instance

#     def __init__(self):
#         if not Logger._initialized:
#             self.config = Config()
#             self.logger = logging.getLogger('algo_trading_logger')
#             self.logger.setLevel(logging.DEBUG)
            
#             # Clear existing handlers
#             self.logger.handlers.clear()

#             # Console handler
#             console_handler = logging.StreamHandler()
#             console_formatter = logging.Formatter(
#                 '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#             )
#             console_handler.setFormatter(console_formatter)
#             self.logger.addHandler(console_handler)

#             # CloudWatch handler
#             try:
#                 if not any(isinstance(h, watchtower.CloudWatchLogHandler) for h in self.logger.handlers):
#                     cloudwatch_handler = watchtower.CloudWatchLogHandler(
#                         log_group="/ecs/z21-algo-trading",
#                         stream_name="ecs-application-logs",
#                         boto3_client=boto3.client(
#                             'logs',
#                             region_name='ap-south-1'
#                         ),
#                         create_log_group=True
#                     )
#                     cloudwatch_handler.setFormatter(console_formatter)
#                     self.logger.addHandler(cloudwatch_handler)
#             except Exception as e:
#                 self.logger.error(f"Failed to initialize CloudWatch logging: {str(e)}")
            
#             Logger._initialized = True

#     def info(self, message):
#         if self._loggingEnabled:
#             self.logger.info(message)

#     def error(self, message):
#         if self._loggingEnabled:
#             self.logger.error(message)

#     def debug(self, message):
#         if self._loggingEnabled:
#             self.logger.debug(message)


import logging
from config.settings import Settings

class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.logger = logging.getLogger('algo_trading_logger')
            self.logger.setLevel(Settings.LOG_LEVEL)
            
            # File handler
            file_handler = logging.FileHandler(Settings.LOG_FILE)
            file_handler.setLevel(Settings.LOG_LEVEL)
            
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(Settings.LOG_LEVEL)
            
            # Formatter
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            # Add handlers
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
            
            self.initialized = True

    def debug(self, message, *args, **kwargs):
        self.logger.debug(message, *args, **kwargs)
        
    def info(self, message, *args, **kwargs):
        self.logger.info(message, *args, **kwargs)
        
    def warning(self, message, *args, **kwargs):
        self.logger.warning(message, *args, **kwargs)
        
    def error(self, message, *args, **kwargs):
        self.logger.error(message, *args, **kwargs)
        
    def critical(self, message, *args, **kwargs):
        self.logger.critical(message, *args, **kwargs)