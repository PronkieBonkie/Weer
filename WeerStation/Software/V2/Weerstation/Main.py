import time
import ST7789
from PIL import Image, ImageDraw
import weatherhat
from PIL import ImageFont
from colorsys import hsv_to_rgb
from Databasesqlite import WeatherDataDatabase
from DatabaseMysql import WeatherDataDatabaseMySQL

sproeiMinuten = 10
timer_duration = 10
FPS = 1

DISPLAY_WIDTH = 240
DISPLAY_HEIGHT = 240
SPI_SPEED_MHZ = 80

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)

OFFSET = -7.5

font_size = 20

class WeatherStationApp:
    def __init__(self):
        self.start_time = time.time()
        
        self.custom_font = ImageFont.truetype("MinecraftTen-VGORe.ttf", font_size)
        self.display = ST7789.ST7789(
            rotation=90,
            port=0,
            cs=1,
            dc=9,
            backlight=12,
            spi_speed_hz=SPI_SPEED_MHZ * 1000 * 1000,
            width=DISPLAY_WIDTH,
            height=DISPLAY_HEIGHT
        )
        self.image = Image.new("RGBA", (DISPLAY_WIDTH, DISPLAY_HEIGHT), color=(255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)
        self.sensor_data = self.initialize_sensor_data()
        self.db = WeatherDataDatabase()
        self.db = WeatherDataDatabaseMySQL()

    def initialize_sensor_data(self):
        sensor = weatherhat.WeatherHAT()
        sensor.temperature_offset = OFFSET
        return sensor

    def update_sensor_data(self):
        self.sensor_data.update(interval=1.0)
        
    def render_display(self):
        self.draw.rectangle((0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT), fill=COLOR_BLACK)
        self.rainbow_colors = [hsv_to_rgb(i / 50, 1, 1) for i in range(50)]
        rainbow_color_index = int((time.time() * 50) % 50)
        rainbow_color = tuple(int(c * 255) for c in self.rainbow_colors[rainbow_color_index])
        temperature = round(self.sensor_data.temperature, 1)
        pressure = round(self.sensor_data.pressure, 1)
        wind_speed = round(self.sensor_data.wind_speed, 1)
        wind_direction = self.sensor_data.wind_direction
        rain = round(self.sensor_data.rain, 1)

        wind_direction_text = ""
        if 22.5 <= wind_direction < 67.5:
            wind_direction_text = "Noord-Oost"
        elif 67.5 <= wind_direction < 112.5:
            wind_direction_text = "Oost"
        elif 112.5 <= wind_direction < 157.5:
            wind_direction_text = "Zuid-Oost"
        elif 157.5 <= wind_direction < 202.5:
            wind_direction_text = "Zuid"
        elif 202.5 <= wind_direction < 247.5:
            wind_direction_text = "Zuid-West"
        elif 247.5 <= wind_direction < 292.5:
            wind_direction_text = "West"
        elif 292.5 <= wind_direction < 337.5:
            wind_direction_text = "Noord-West"
        else:
            wind_direction_text = "Noord"

        self.draw.text((10, 10), "WEERSTATION", font=self.custom_font, fill=rainbow_color)
        self.draw.text((10, 40), f"Temperatuur: {temperature}°C", font=self.custom_font, fill=COLOR_WHITE)
        self.draw.text((10, 70), f"Luchtdruk: {pressure} hPa", font=self.custom_font, fill=COLOR_WHITE)
        self.draw.text((10, 100), f"Wind snelheid: {wind_speed} m/s", font=self.custom_font, fill=COLOR_WHITE)
        self.draw.text((10, 130), f"Wind Richting: {wind_direction_text}", font=self.custom_font, fill=COLOR_WHITE)
        self.draw.text((10, 160), f"Regen: {rain} mm", font=self.custom_font, fill=COLOR_WHITE)

    def run(self):
        sproeiTijdStart = 0
        sproeierAan = False
        
        while True:
            self.db.insert_data(self.sensor_data)
            self.update_sensor_data()
            self.render_display()
            self.display.display(self.image)
            rain = self.sensor_data.rain
            if rain < 15 and time.time() - self.start_time >= timer_duration and not sproeierAan:
                print("Sproeien gestart")
                sproeiTijdStart = time.time()
                sproeierAan = True 

            elif time.time() - sproeiTijdStart >= sproeiMinuten and sproeierAan:
                print("Stop sproeien")
                self.start_time = time.time()
                sproeiTijdStart = 0
                sproeierAan = False

            elif rain >= 15:
                print("Genoeg regen gevallen")
                self.start_time = time.time()

            time.sleep(1.0 / FPS)

if __name__ == "__main__":
    app = WeatherStationApp()
    app.run()