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

    def fetchall(self):
        return self.cursor.fetchall()
    
    def fetch_one(self):
        result = self.cursor.fetchone()
        return result

    def execute_query(self, query):
        self.cursor.execute(query)

    def fetch_all_rows(self):
        return self.cursor.fetchall()

    def commit_changes(self):
        self.conn.commit()

    def get_column_names(self, table_name):
        query = f"SELECT * FROM {table_name} LIMIT 1"
        self.execute_query(query)
        column_names = [desc[0] for desc in self.cursor.description]
        return column_names
    
    def execute_query_with_dataframe(self, query, dataframe):
        for row in dataframe.itertuples(index=False):
            self.execute_query(query, row)
        self.commit_changes()