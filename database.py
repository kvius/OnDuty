import mysql.connector

class DatabaseManager:
    def __init__(self, host, user, password, db_name):
        self.connection = None
        self.host = host
        self.user = user
        self.port = 3306
        self.password = password
        self.db_name = db_name

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.db_name
        )

    def load_data(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()  # Добавляем коммит изменений
            print(f"Query executed successfully: {query}")
        except mysql.connector.Error as e:
            print(f"MySQL Error: {e}")
        finally:
            cursor.close()

    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        try:
            results = cursor.fetchall()
            cursor.close()
            return results
        except mysql.connector.Error as e:
            print(f"MySQL Error: {e}")
            cursor.close()
            return None

    def get_cur_date(self):
        """Retrieves the current date from the MySQL database."""

        self.connect()  # Ensure a database connection exists
        query = "SELECT CURDATE()"
        cursor = self.connection.cursor()

        try:
            cursor.execute(query)
            result = cursor.fetchone()  # Fetch the date as a tuple
            cursor.close()
            return result[0]  # Return the date object (datetime.date)
        except mysql.connector.Error as e:
            print(f"MySQL Error: {e}")
            cursor.close()
            return None

    def check_credentials(self, username, password):
        self.connect()
        query = "SELECT role,`group` FROM admins WHERE login = %s AND password = %s"
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            cursor.close()
            if result:
                print(result)
                return {"role": result[0],"group":str(result[1])}
            else:
                return None
        except mysql.connector.Error as e:
            print(f"MySQL Error: {e}")
            cursor.close()
            return None

    # def decorator(self, func):
    #     def inner(*args, **kwargs):
    #         try:
    #             connection = pymysql.connect(
    #                 host=self.host,
    #                 port=self.port,
    #                 user=self.user,
    #                 password=self.password,
    #                 database=self.db_name)
    #
    #             with connection.cursor() as cursor:
    #                 result = func(*args, cursor)
    #                 return result
    #         except Exception as e:
    #             print(e)
    #         finally:
    #             if connection:
    #                 connection.close()
    #
    #     return inner
    #

    def close(self):
        if self.connection:
            self.connection.close()
