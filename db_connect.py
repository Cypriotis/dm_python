import mysql.connector

class DatabaseConnector:
    def __init__(self, host, username, password, database ,port):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.username,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def execute_query(self, query):
        self.cursor.execute(query)

    def fetch_all_rows(self):
        return self.cursor.fetchall()

    def commit_changes(self):
        self.conn.commit()