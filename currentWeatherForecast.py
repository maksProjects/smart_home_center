import requests
import pygame
import io
from deviceSetup import setupFile

try:
    # Python2
    from urllib2 import urlopen
except ImportError:
    # Python3
    from urllib.request import urlopen

CITY = setupFile["weather_forecast"][0]["city"]
LAT = setupFile["weather_forecast"][0]["lat"]
LON = setupFile["weather_forecast"][0]["lon"]
LANG = setupFile["main_settings"][0]["lang"]
UNITS = setupFile["weather_forecast"][0]["units"]
API_KEY = setupFile["weather_forecast"][0]["api_key"]


def update_weather(screen_w, screen_h, font, fontcolor, font_height):
    screen = pygame.Surface((screen_w+100, screen_h))
    screen.fill((0, 0, 0))
    weatherScreen = pygame.Surface((screen_w+100, int(screen_h)))
    weatherScreen.fill((0, 0, 0))

    BASE_URL = "https://api.openweathermap.org/data/2.5/onecall?"
    URL = BASE_URL + "lat=" + LAT + "&lon=" + LON + "&exclude=hourly,minutely,daily,alerts" + "&units=" + UNITS + "&appid=" + API_KEY + "&lang=" + LANG
    response = requests.get(URL)

    # checking the status code of the request
    if response.status_code == 200:
        data = response.json()

        main = data["current"]

        # WEATHER IMAGE
        img_id = data['current']['weather'][0]["icon"]
        img_url = "http://openweathermap.org/img/wn/" + str(img_id) + "@2x.png"
        img_str = urlopen(img_url).read()
        img_file = io.BytesIO(img_str)
        img = pygame.image.load(img_file)
        img = pygame.transform.scale(img, (int(screen_h / 2.7), int(screen_h / 2.7)))
        # img = img.convert()
        screen.blit(img, (screen_w/2, -screen_h/12))

        # CURRENT WEATHER
        description = font.render(main["weather"][0]["description"], True, fontcolor)
        temperature = font.render(f"temperatura: {main['temp']} °C", True, fontcolor)
        feels_like = font.render(f"odczuwalna: {main['feels_like']} °C", True, fontcolor)
        humidity = font.render(f"wilgotność: {main['humidity']}%", True, fontcolor)
        pressure = font.render(f"ciśnienie: {main['pressure']} hPa", True, fontcolor)
        visibility = font.render(f"widoczność: {main['visibility'] / 1000} km", True, fontcolor)
        try:
            wind_speed = main['wind_speed']*3.6
            wind = font.render("wiatr: %.2f km/h" % wind_speed, True, fontcolor)
        except:
            pass
        try:
            rain = font.render(f"opady deszczu: {main['rain']['1h']} mm", True, fontcolor)
        except:
            pass
        try:
            snow = font.render(f"opady śniegu: {main['snow']['1h']} mm", True, fontcolor)
        except:
            pass

        # blit on weather screen
        from_left_border = screen_w/3
        weatherScreen.blit(description, (from_left_border, 0))
        weatherScreen.blit(temperature, (from_left_border, font_height))
        weatherScreen.blit(feels_like, (from_left_border, 2 * font_height))
        weatherScreen.blit(humidity, (from_left_border, 3 * font_height))
        weatherScreen.blit(pressure, (from_left_border, 4 * font_height))
        weatherScreen.blit(visibility, (from_left_border, 5 * font_height))
        i = 6
        try:
            weatherScreen.blit(wind, (from_left_border, i * font_height))
            i += 1
        except:
            pass
        try:
            weatherScreen.blit(rain, (from_left_border, i * font_height))
            i += 1
        except:
            pass
        try:
            weatherScreen.blit(snow, (from_left_border, i * font_height))
            i += 1
        except:
            pass
        screen.blit(weatherScreen, (0, int(screen_h / 5)))
    else:
        print("Error in the HTTP request")

    print("current weather screen updated")
    return screen
