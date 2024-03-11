import sqlite3


class Database:
    def __init__(self, path_to_db="database.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            id INTEGER UNIQUE,
            user_id INTEGER NOT NULL UNIQUE,
            Name varchar(255) NOT NULL,
            voice TEXT,
            PRIMARY KEY (id AUTOINCREMENT)
            );
"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def stat(self):
        return self.execute(f"SELECT COUNT(*) FROM Users;", fetchone=True)

    def add_user(self, user_id: int, name: str, voice: str):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO Users(user_id, Name, voice) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=(user_id, name, voice), commit=True)

    def select_all_users(self):
        sql = """
         SELECT * FROM Users
         """
        return self.execute(sql, fetchall=True)

    def update_user_voice(self, voice, user_id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE users SET voice = ? WHERE user_id = ?
        """
        return self.execute(sql, parameters=(voice, user_id), commit=True)

    def is_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchall=True)


def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
