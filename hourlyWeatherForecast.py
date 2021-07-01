import requests
import pygame
import io
from deviceSetup import setupFile
from datetime import datetime
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
    screen = pygame.Surface((screen_w, screen_h))
    plot_screen = pygame.Surface((screen_w, screen_h))
    screen.fill((0, 0, 0))
    plot_screen.fill((0, 0, 0))

    BASE_URL = "https://api.openweathermap.org/data/2.5/onecall?"
    URL = BASE_URL + "lat=" + LAT + "&lon=" + LON + "&exclude=currently,minutely,daily,alerts" + "&units=" + UNITS + "&appid=" + API_KEY + "&lang=" + LANG
    response = requests.get(URL)

    # checking the status code of the request
    if response.status_code == 200:
        data = response.json()
        main = data['hourly']

        # hourly plot for 24h
        y_hourlyTemp = []
        x_hours = []
        step = (screen_w) / 24
        hours = ""
        icons = []
        for i in range(24):
            # hourly plot
            temp = main[i]["temp"]
            y = screen_h - (temp ** 1.6)
            x = 22 + (i * step)
            x_hours.append(x)
            y_hourlyTemp.append(y)

            # blit hours onto screen
            screen.blit(font.render(str(datetime.fromtimestamp(main[i]["dt"]).hour) + ":00", True, fontcolor), (x-13, int(screen_h/1.1)))

            # blit temperature onto screen
            if type(temp) == float:
                if int(str(temp-int(temp))[2:3]) >= 5:
                    temp += 1
            str_temp = str(temp)[:2] + "°C"
            plot_screen.blit(font.render(str_temp, True, fontcolor), (x-10, y-25))

            # hourly image
            img_id = main[i]["weather"][0]["icon"]
            img_url = "http://openweathermap.org/img/wn/" + str(img_id) + "@2x.png"
            img_str = urlopen(img_url).read()
            img_file = io.BytesIO(img_str)
            img = pygame.image.load(img_file)
            img = pygame.transform.scale(img, (int(screen_w / 20), int(screen_w / 20)))
            icons.append(img)

        # points -> [x, y], for lines drawing
        fucking_list_of_points = []
        for i in range(24):
            fucking_list_of_points.append([x_hours[i], y_hourlyTemp[i]])

        # DRAW everything onto screen
        pygame.draw.lines(plot_screen, (0, 0, 255), False, fucking_list_of_points, 4)
        screen.blit(plot_screen, (0, -int(screen_h / 7)))

        y_icons = int(screen_h/1.3)
        for i in range(24):
            screen.blit(icons[i], (x_hours[i]-22, y_icons))

    else:
        print("Error in the HTTP request")

    print("hourly weather screen updated")
    return screen
