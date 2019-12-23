__recent_weather_to_publish = {"time": "56464", "feels": "hot", "gust": "yono", "humid": "dfdgdsg", "temp": "gds",
                "visib": "gsd", "winddir": "dsgsdg", "windspd": "gds", "uv": "fh", "type": "ghd", "prob": "fhdf"}

print(__recent_weather_to_publish, type(__recent_weather_to_publish), id(__recent_weather_to_publish))
print(__recent_weather_to_publish.items())
for name, val in __recent_weather_to_publish.items():
    print(name, val)

print("\n")
name_map = {"time": "WeatherTime", "feels": "FeelsLikeTemperature", "gust": "WindGust", "humid": "Humidity",
            "temp": "Temperature", "visib": "Visibility", "winddir": "WindDirection",
            "windspd": "WindSpeed", "uv": "MaxUVIndex", "type": "WeatherType",
            "prob": "PrecipitationProbability"}
__recent_weather_to_publish = dict((name_map[name], val) for name, val in __recent_weather_to_publish.items())
print(__recent_weather_to_publish, type(__recent_weather_to_publish), id(__recent_weather_to_publish))


# example 2
print("\n")
dict1 = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
dict2 = {"a": 5, "b": 6, "c": 7, "d": 8}
# Put all keys of `dict1` in a list and returns the list
print(dict2.keys())
# Put all values saved in `dict1` in a list and returns the list
print(dict2.values())
print(dict2.items())
print(dict1.items())
dict_variable1 = dict((dict2[name], val) for name, val in dict1.items())    # option 1
dict_variable2 = {dict2[key]: value for (key, value) in dict1.items()}      # option 2
print(dict_variable1)
print(dict_variable2)
