thing_data_label = "Weather Forecast for: EYE (PETERBOROUGH), ENGLAND"
label = thing_data_label.strip("Weather Forecast for: ")
recent_weather_to_publish = label
print(recent_weather_to_publish)


# Python code to illustrate the working of strip()
string = '@@@@Geeks for Geeks@@@@@'

# Strip all '@' from begining and ending
print(string.strip('@'))

string = 'www.Geeksforgeeks.org'

# '.grow' removes 'www' and 'org' and '.'
print(string.strip('.grow'))
