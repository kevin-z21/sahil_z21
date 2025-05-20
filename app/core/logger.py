import logging
# import watchtower
# import boto3
# from config.config import Config

class Logger:
    _instance = None
    _initialized = False
    _loggingEnabled = True

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not Logger._initialized:
            # self.config = Config()
            self.logger = logging.getLogger('algo_trading_logger')
            self.logger.setLevel(logging.DEBUG)
            
            # Clear existing handlers
            self.logger.handlers.clear()

            # Console handler
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)

            # CloudWatch handler
            # try:
            #     if not any(isinstance(h, watchtower.CloudWatchLogHandler) for h in self.logger.handlers):
            #         cloudwatch_handler = watchtower.CloudWatchLogHandler(
            #             log_group="/ecs/z21-algo-trading",
            #             stream_name="ecs-application-logs",
            #             boto3_client=boto3.client(
            #                 'logs',
            #                 region_name='ap-south-1'
            #             ),
            #             create_log_group=True
            #         )
            #         cloudwatch_handler.setFormatter(console_formatter)
            #         self.logger.addHandler(cloudwatch_handler)
            # except Exception as e:
            #     self.logger.error(f"Failed to initialize CloudWatch logging: {str(e)}")
            
            Logger._initialized = True

    def info(self, message):
        if self._loggingEnabled:
            self.logger.info(message)

    def error(self, message):
        if self._loggingEnabled:
            self.logger.error(message)

    def debug(self, message):
        if self._loggingEnabled:
            self.logger.debug(message)