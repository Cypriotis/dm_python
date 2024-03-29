from db_connect import DatabaseConnector


# MySQL database connection details
host = 'localhost'
username = 'root'
password = ''
database = 'DeMa'
port = '3308'


class database_init():
    def execute():
        # Create an instance of the DatabaseConnector
        db_connector = DatabaseConnector(
            host, username, password, database, port)
        db_connector.connect()

        # debug action
        db_connector.execute_query('''DROP TABLE IF EXISTS Users''')

        db_connector.execute_query('''DROP TABLE IF EXISTS Artists''')

        db_connector.execute_query('''DROP TABLE IF EXISTS Albums''')

        db_connector.execute_query('''DROP TABLE IF EXISTS UsersFavInfo''')

        db_connector.execute_query('''DROP TABLE IF EXISTS UsersSongs''')

        db_connector.execute_query('''DROP TABLE IF EXISTS Recommends''')

        db_connector.execute_query('''DROP TABLE IF EXISTS LatLon''')
        # creating tables if not exists
        db_connector.execute_query(
            '''CREATE TABLE IF NOT EXISTS LatLon (name VARCHAR(254),lat FLOAT,lon FLOAT,song1 VARCHAR(254),song1_lat FLOAT,song1_lon FLOAT,song2 VARCHAR(254),song2_lat FLOAT,song2_lon FLOAT,song3 VARCHAR(254),song3_lat FLOAT,song3_lon FLOAT)''')
        
        db_connector.execute_query(
            '''CREATE TABLE IF NOT EXISTS Users (user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, username VARCHAR(254), country VARCHAR(254), favorite_artist VARCHAR(254), playcount INT)''')

        db_connector.execute_query(
            '''CREATE TABLE IF NOT EXISTS Artists (artists_name VARCHAR(254),mbid VARCHAR(254),artist_url VARCHAR(254))''')

        db_connector.execute_query(
            '''CREATE TABLE IF NOT EXISTS Albums(artists_name VARCHAR(254),album_name VARCHAR(254))''')

        db_connector.execute_query(
            '''CREATE TABLE IF NOT EXISTS UsersFavInfo (user_name VARCHAR(254),artists_name VARCHAR(254),album_name VARCHAR(254))''')

        db_connector.execute_query(
            '''CREATE TABLE IF NOT EXISTS UserSongs (user_name VARCHAR(254), song_name VARCHAR(254),song_name2 VARCHAR(254),song_name3 VARCHAR(254))''')

        db_connector.execute_query(
            '''CREATE TABLE IF NOT EXISTS RandomUsers (name VARCHAR(254))''')

        db_connector.execute_query(
            '''CREATE TABLE IF NOT EXISTS Filtered (name TEXT)''')

        db_connector.execute_query(
            '''CREATE TABLE IF NOT EXISTS Recommends (name VARCHAR(254),song VARCHAR(254), recommend_from_user VARCHAR(254))''')

        db_connector.commit_changes()
