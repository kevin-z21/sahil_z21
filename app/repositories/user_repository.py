from core.database import Database

class UserRepository:
    def __init__(self):
        self.db = Database()

    def get_user_by_email(self, email):
        query = """
            SELECT *
            FROM users
            WHERE email = %s;
        """
        return self.db.fetch_one(query, (email,))
  