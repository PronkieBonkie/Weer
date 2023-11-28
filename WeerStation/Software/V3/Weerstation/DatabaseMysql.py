import mysql.connector
from mysql.connector import errorcode
import time

class WeatherDataDatabaseMySQL:
    def __init__(self):
        self.try_mysql_connection()
        self.create_table()

    def try_mysql_connection(self):
            
        self.connection = mysql.connector.connect(
            host='172.20.20.2',
            user='gebruiker',
            password='1',
            database='sensor_data'
        )


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
            print("Data naar MySQL-database ingevoegd")