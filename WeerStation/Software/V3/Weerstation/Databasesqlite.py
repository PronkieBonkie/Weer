import sqlite3
import time

DATABASE_FILE = 'weather_data.db'

class WeatherDataDatabase:
    def __init__(self):
        self.connection = sqlite3.connect(DATABASE_FILE)
        self.create_table()

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                temperature REAL,
                pressure REAL,
                wind_speed REAL,
                wind_direction REAL,
                rain REAL,
                timestamp INTEGER
            )
        ''')
        self.connection.commit()

    def insert_data(self, sensor_data):
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO weather_data (
                temperature, pressure, wind_speed, wind_direction, rain, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            sensor_data.temperature,
            sensor_data.pressure,
            sensor_data.wind_speed,
            sensor_data.wind_direction,
            sensor_data.rain,
            int(time.time())
        ))
        self.connection.commit()
        print("data naar sqlite")