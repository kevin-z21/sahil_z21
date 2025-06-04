from contextlib import contextmanager
import psycopg2
from psycopg2.extras import RealDictCursor 
from config.config import Config
from core.logger import Logger
from psycopg2.extras import execute_values

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.logger = Logger()
        if not hasattr(self, 'conn'):
            self.config = Config()
            self.connect()

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                database=self.config.DB_NAME,
                user=self.config.DB_USER,
                password=self.config.DB_PASS,
                host=self.config.DB_HOST,
            )
            self.conn.autocommit = False
        except Exception as e:
            self.logger.error(f"Database connection failed: {str(e)}")
            raise

    @contextmanager
    def transaction(self):
        try:
            yield
            self.commit()
        except Exception as e:
            self.rollback()
            raise
        finally:
            self.ensure_connection()

    def ensure_connection(self):
        if self.conn.closed or self.conn.status != psycopg2.extensions.STATUS_READY:
            self.connect()

    def execute(self, query, params=None):
        try:
            with self.transaction():
                cursor = self.conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute(query, params or ())
                return cursor
        except Exception as e:
            self.logger.error(f"Query execution failed: {str(e)}")
            raise
    
    def bulk_insert(self, query, values):
        try:
            with self.transaction():
                cursor = self.conn.cursor(cursor_factory=RealDictCursor)
                # Convert list of tuples to list of value strings
                values_str = [
                    cursor.mogrify("(%s,%s,%s)", x).decode('utf-8') 
                    for x in values
                ]
                # Join all values into single query
                cursor.execute(
                    query + ",".join(values_str)
                )
                if 'RETURNING' in query:
                    return cursor.fetchall()
                return True
        except Exception as e:
            self.logger.error(f"Bulk insert failed: {str(e)}")
            raise 

    def bulk_insert_dynamic(self, query, values):
        try:
            with self.transaction():
                cursor = self.conn.cursor(cursor_factory=RealDictCursor)
                
                # Ensure values are a list of tuples
                if not values or not isinstance(values[0], (list, tuple)):
                    raise ValueError("Values must be a list of tuples/lists")

                # Create correct number of placeholders dynamically
                placeholders = "(" + ",".join(["%s"] * len(values[0])) + ")"

                # Convert list of tuples into a list of mogrified strings
                values_str = [
                    cursor.mogrify(placeholders, x).decode('utf-8')
                    for x in values
                ]
                
                # Join all values into a single query and execute
                final_query = query + ",".join(values_str)
                cursor.execute(final_query)

                if 'RETURNING' in query:
                    return cursor.fetchall()
                return True
        except Exception as e:
            self.logger.error(f"Bulk insert failed: {str(e)}")
            raise

        
    def fetch_one(self, query, params=None):
        with self.transaction():
            cursor = self.execute(query, params)
            return cursor.fetchone()

    def fetch_all(self, query, params=None):
        with self.transaction():
            cursor = self.execute(query, params)
            return cursor.fetchall()

    def insert(self, table, data):
        try:
            with self.transaction():
                columns = ', '.join(data.keys())
                values = ', '.join(['%s'] * len(data))
                query = f"INSERT INTO {table} ({columns}) VALUES ({values}) RETURNING id"
                params = tuple(data.values())
                
                self.logger.debug(f"Executing insert query: {query} with params: {params}")
                cursor = self.execute(query, params)
                
                result = cursor.fetchone()
                return result['id'] if result else None
                
        except Exception as e:
            self.logger.error(f"Insert failed for table {table}: {str(e)}")
            raise Exception(f"Database insert error: {str(e)}")
        
    ## Temporary Create for order by Kevin ##
    def insert_order(self, table, data):
        try:
            with self.transaction():
                columns = ', '.join(data.keys())
                values = ', '.join(['%s'] * len(data))
                query = f"INSERT INTO {table} ({columns}) VALUES ({values}) RETURNING order_id"
                params = tuple(data.values())
                
                self.logger.debug(f"Executing insert query for ORDER: {query} with params: {params}")
                cursor = self.execute(query, params)
                
                result = cursor.fetchone()
                return result['order_id'] if result else None
                
        except Exception as e:
            self.logger.error(f"Insert failed for table {table}: {str(e)}")
            raise Exception(f"Database insert error: {str(e)}")

    def update(self, table, data, condition):
        try:
            with self.transaction():
                set_values = ', '.join([f"{k} = %s" for k in data.keys()])
                where_clause = ' AND '.join([f"{k} = %s" for k in condition.keys()])
                query = f"UPDATE {table} SET {set_values} WHERE {where_clause} RETURNING id"
                params = tuple(data.values()) + tuple(condition.values())
                cursor = self.execute(query, params)
                return cursor.fetchone()['id']
        except Exception as e:
            self.logger.error(f"Update failed for table {table}: {str(e)}")
            raise Exception(f"Database update error: {str(e)}")
    
    ## Temporary Create for order by Kevin ##
    def update_order(self, table, data, condition):
        with self.transaction():
            set_values = ', '.join([f"{k} = %s" for k in data.keys()])
            where_clause = ' AND '.join([f"{k} = %s" for k in condition.keys()])
            query = f"UPDATE {table} SET {set_values} WHERE {where_clause} RETURNING order_id"
            params = tuple(data.values()) + tuple(condition.values())
            cursor = self.execute(query, params)
            return cursor.fetchone()['order_id']
        
    def delete(self, table, condition):
        """
        Delete rows from the database.

        Parameters:
        table (str): The name of the table to delete from.
        condition (dict): A dictionary representing the condition for the WHERE clause.

        Example:
        condition = {"user_id": 1}
        database.delete("table_name", condition)
        """
        try:
            with self.transaction():
                where_clause = ' AND '.join([f"{k} = %s" for k in condition.keys()])
                query = f"DELETE FROM {table} WHERE {where_clause} RETURNING id"
                params = tuple(condition.values())
                cursor = self.execute(query, params)
                result = cursor.fetchall()
                return [row['id'] for row in result] if result else None
        except Exception as e:
            self.logger.error(f"Delete failed for table {table}: {str(e)}")
            raise Exception(f"Database delete error: {str(e)}")

    def bulk_upsert(self, query, values):
        try:
            with self.transaction():
                cursor = self.conn.cursor()
                execute_values(cursor, query, values)
        except Exception as e:
            self.logger.error(f"Bulk upsert failed: {str(e)}")
            raise
        
    def rollback(self):
        try:
            self.conn.rollback()
        except:
            self.connect()

    def commit(self):
        try:
            self.conn.commit()
        except:
            self.rollback()
            raise