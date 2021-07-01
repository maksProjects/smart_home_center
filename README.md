Smart home center is a project that is built to run on a Raspberry PI micro computer and to display on chosen screen. 
In its current form it allows to check the current time and date, or something more interesting such as weather forecast.
Weather forecast is displayed in two diffrent ways:
  first, user can check heavily described, actual weather, synchronized with server once per 10 minutes
  second, user can check forecast for next 24 hours. Its mainly temeprature and for greater readibility an icon visually describing the weather.
As a great addition I implemented graph showing temperature changes across incomming 24 hours.
Last thing in current build is intercom screen. It's not functional yet, the idea is to display view from web camera outside the house, preferably front door.
As a substitute It shows the view from built in camera of a laptop.


How to launch the program:
1. ensure you have python3 on your device
2. add pygame library
3. add requests library
4. run smartHomeCenter.py
