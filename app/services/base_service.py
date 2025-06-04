from core.database import Database

class BaseService:
    def __init__(self):
        self.db = Database()