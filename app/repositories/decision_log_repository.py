from core.database import Database

class DecisionLogRepository:
    def __init__(self):
        self.db = Database()

    def find_by_user_id(self, user_id):
        return self.db.fetch_one(
            "SELECT * FROM decision_algo_log WHERE user_id = %s", 
            (user_id,)
        )

    def get_decision_logs_by_user_id(self, user_id):
        return self.db.fetch_all(
            "SELECT * FROM decision_algo_log WHERE user_id = %s ORDER BY createdat DESC;", (user_id,)
        )
