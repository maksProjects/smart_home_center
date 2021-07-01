import pygame
import time
import currentWeatherForecast
import hourlyWeatherForecast


class Screen(pygame.Surface):
    def __init__(self, screen_w, screen_h, font, fontcolor):
        pygame.Surface.__init__(self, (screen_w, screen_h))

        # variables for updating screen
        self.hours_passed = 0
        self.minutes_passed = 0
        self.current_weather_updated = False
        self.hourly_weather_updated = False
        self.date_updated = False
        self.week_updated = False

        # fonts
        screen_measurements = max(screen_w, screen_h)
        self.tiniestFont = pygame.font.Font(font, int(screen_measurements/87))
        self.verySmallFont = pygame.font.Font(font, int(screen_measurements/40))
        self.smallFont = pygame.font.Font(font, int(screen_measurements/25))
        self.normalFont = pygame.font.Font(font, int(screen_measurements/12))
        self.bigFont = pygame.font.Font(font, int(screen_measurements/10))
        self.fontcolor = fontcolor

        # fonts heights
        self.tiniestHeight = self.tiniestFont.get_height()
        self.verySmallHeight = self.verySmallFont.get_height()
        self.smallHeight = self.smallFont.get_height()
        self.normalHeight = self.normalFont.get_height()
        self.bigHeight = self.bigFont.get_height()

        # surfaces
        self.screen = pygame.Surface((screen_w-60, screen_h-60))
        self.dateScreen = pygame.Surface((self.screen.get_width()/2, self.smallHeight))
        self.timeScreen = pygame.Surface((self.screen.get_width()/2, self.normalHeight))
        self.weekScreen = pygame.Surface((self.screen.get_width()/2, self.verySmallHeight))
        self.currentWeatherScreen = pygame.Surface((self.screen.get_width() / 2, self.screen.get_height() / 1.78))
        self.hourlyWeatherScreen = pygame.Surface((self.screen.get_width(), self.screen.get_height() / 2.6))

        # starting height drawing point
        self.dateStartingHeight = 0
        self.timeStartingHeight = self.dateScreen.get_height()
        self.weekStartingHeight = self.timeStartingHeight + self.timeScreen.get_height()
        self.weatherStartingHeight = 0
        self.hourlyWeatherStartingHeight = self.currentWeatherScreen.get_height()

        # initial screens blit
        self.currentWeatherScreen.blit(currentWeatherForecast.update_weather(self.currentWeatherScreen.get_width(), self.currentWeatherScreen.get_height(), self.verySmallFont, self.fontcolor, self.verySmallHeight), (0, 0))
        self.hourlyWeatherScreen.blit(hourlyWeatherForecast.update_weather(self.hourlyWeatherScreen.get_width(), self.hourlyWeatherScreen.get_height(), self.tiniestFont, self.fontcolor, self.tiniestHeight), (0, 0))
        self.dateScreen.blit(self.update_date_screen(time.localtime()), (0, 0))
        self.weekScreen.blit(self.update_week_screen(time.localtime()), (0, 0))

    def update_time_screen(self, current_time):
        """returns current time in H:M:S format"""

        hours = str(current_time[3])
        minutes = str(current_time[4])
        seconds = str(current_time[5])

        self.hours_passed = int(hours)
        self.minutes_passed = int(minutes)

        if len(hours) == 1:
            hours = "0"+hours
        if len(minutes) == 1:
            minutes = "0"+minutes
        if len(seconds) == 1:
            seconds = "0"+seconds
        return self.normalFont.render(hours+":"+minutes+":"+seconds, True, self.fontcolor)

    def update_date_screen(self, current_time):
        """returns current date in string in 'D M Y' format"""

        print("date screen updated")
        month_name = {
            1: "Stycznia",
            2: "Lutego",
            3: "Marca",
            4: "Kwietnia",
            5: "Maja",
            6: "Czerwca",
            7: "Lipca",
            8: "Sierpnia",
            9: "Września",
            10: "Października",
            11: "Listopada",
            12: "Grudnia",
        }

        year = str(current_time[0])
        month = month_name[current_time[1]]
        day = str(current_time[2])
        return self.smallFont.render(day+" "+month+" "+year, True, self.fontcolor)

    def update_week_screen(self, current_time):
        """returns current week in year"""

        print("week screen updated")
        week = current_time[7]/7
        if week % 1 >= 0.5:
            week = str(int(week)+1)
        else:
            week = str(int(week))
        return self.verySmallFont.render(week+" tydzień roku", True, self.fontcolor)

    def draw(self):
        """Draws everything on itself, based on the info provided in class.
         After resolving this module, object is ready to blit on designated surface"""
        # CLEAR THE SCREENS
        self.fill((0, 0, 0))
        self.screen.fill((0, 0, 0))

        #self.fill((155, 0, 0))
        #self.screen.fill((0, 255, 0))
        # self.timeScreen.fill((100, 0, 100))
        # self.dateScreen.fill((0, 155, 0))
        # self.weekScreen.fill((0, 0, 200))

        # blit time screen
        self.timeScreen.fill((0, 0, 0))
        self.timeScreen.blit(self.update_time_screen(time.localtime()), (0, 0))

        # blit date screen
        if self.hours_passed == 0:
            if not self.date_updated:
                self.dateScreen.fill((0, 0, 0))
                self.dateScreen.blit(self.update_date_screen(time.localtime()), (0, 0))
                self.date_updated = True
        else:
            self.date_updated = False

        # blit week screen
        if self.hours_passed == 0:
            if not self.week_updated:
                self.weekScreen.fill((0, 0, 0))
                self.weekScreen.blit(self.update_week_screen(time.localtime()), (0, 0))
                self.week_updated = True
        else:
            self.date_updated = False

        # current weather screen
        if self.minutes_passed == 0 or self.minutes_passed == 10 or self.minutes_passed == 20 or self.minutes_passed == 30 or self.minutes_passed == 40 or self.minutes_passed == 50:
            if not self.current_weather_updated:
                self.currentWeatherScreen.blit(currentWeatherForecast.update_weather(self.currentWeatherScreen.get_width(), self.currentWeatherScreen.get_height(), self.verySmallFont, self.fontcolor, self.verySmallHeight), (0, 0))
                self.current_weather_updated = True
            else:
                pass
        else:
            self.current_weather_updated = False

        # hourly weather screen
        if self.minutes_passed == 0:
            if not self.hourly_weather_updated:
                self.hourlyWeatherScreen.blit(hourlyWeatherForecast.update_weather(self.hourlyWeatherScreen.get_width(), self.hourlyWeatherScreen.get_height(), self.tiniestFont, self.fontcolor, self.tiniestHeight), (0, 0))
                self.hourly_weather_updated = True
            else:
                pass
        else:
            self.hourly_weather_updated = False

        # BLIT EVERYTHING ONTO MAIN SCREEN
        self.screen.blit(self.dateScreen, (0, self.dateStartingHeight))
        self.screen.blit(self.timeScreen, (0, self.timeStartingHeight))
        self.screen.blit(self.weekScreen, (0, self.weekStartingHeight))
        self.screen.blit(self.currentWeatherScreen, (self.screen.get_width() / 2, self.weatherStartingHeight))
        self.screen.blit(self.hourlyWeatherScreen, (0, self.hourlyWeatherStartingHeight))
        self.blit(self.screen, (40, 30))
