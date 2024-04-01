import custom_calendar
import datetime

custom_calendar.setfirstweekday(datetime.date(2024, 3, 1).weekday())
first_weekday = custom_calendar.firstweekday()

print(first_weekday)