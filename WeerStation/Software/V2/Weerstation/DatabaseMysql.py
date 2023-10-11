import mysql.connector
from mysql.connector import errorcode
import time

class WeatherDataDatabaseMySQL:
    def __init__(self):
        self.connection = self.connect_to_database()
        self.create_table()

    def connect_to_database(self):
        try:
            connection = mysql.connector.connect(
                host='172.20.20.2',
                user='gebruiker',
                password='1',
                database='sensor_data'
            )
            return connection
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Error: Wrong MySQL username or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Error: Database does not exist")
            else:
                print("Error:", err)

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Jeroen (
                id INT AUTO_INCREMENT PRIMARY KEY,
                temperature FLOAT,
                pressure FLOAT,
                wind_speed FLOAT,
                wind_direction FLOAT,
                rain FLOAT,
                timestamp INT
            )
        ''')
        self.connection.commit()

    def insert_data(self, sensor_data):
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO Jeroen (
                temperature, pressure, wind_speed, wind_direction, rain, timestamp
            ) VALUES (%s, %s, %s, %s, %s, %s)
        ''', (
            sensor_data.temperature,
            sensor_data.pressure,
            sensor_data.wind_speed,
            sensor_data.wind_direction,
            sensor_data.rain,
            int(time.time())
        ))
        self.connection.commit()