data = {"time": "2019-03-14T15:00:00Z", "feels": 7.0, "gust": 40.0, "humid": 56.0, "temp": 11.0, "visib": "VG", "winddir": "WNW",
        "windspd": 22.0, "uv": 1.0,  "type": "3", "prob": "1"}


print('\n')
print("data: ", data.items(), '\n', type(data.items()))
print('\n')
print("data: ", data)
print('\n')

name_map = dict({"time": "WeatherTime", "feels": "FeelsLikeTemperature", "gust": "WindGust", "humid": "Humidity", "temp": "Temperature", "visib": "Visibility", "winddir": "WindDirection",
            "windspd": "WindSpeed", "uv": "MaxUVIndex", "type": "WeatherType", "prob": "PrecipitationProbability"})

print('name_map', name_map)


new_data = dict((name_map[name], val) for name, val in data.items())


print("new data: ", new_data)

# for name, val in data.items():
#     d = dict(name_map[name], val)
#     print(d)


d = {}
print("\n",d, hex(id(d)))
d['data'] = 'download'
print('\n')
print(d, hex(id(d)))

# d = next(item for item in name_map if item['WeatherType'] == '3')
# d['3'] == "cloudy"
# h = 'WeatherType'
# for key, val in name_map:
#     if key = h:
#         if val = "3"
#             val = 'Partly cloudy (day)'
# print(name_map)




current_dict = {'corse': 378, 'cielo': 209, 'mute': 16}
# {'corse': 'Definition of "corse"', 'cielo': 209, 'mute': 16}

# If you find it is taking too long to loop through your dictionary try a generator function:

# current_dict = {}
# l = [{'user': 'user6', 'match_sum': 8},
#      {'user': 'user7', 'match_sum': 4},
#      {'user': 'user9', 'match_sum': 7},
#      {'user': 'user8', 'match_sum': 2}]
#
# d = next(item for item in l if item['user'] == 'user7')
# d['match_sum'] += 3
# print(l)


# def gen_replace_value_with_definition(key_to_find, definition):
#     for key in current_dict.keys():
#         if key == key_to_find:
#             current_dict[key] = definition
#             yield True
#     yield False
#
#
# found = False
# while not found:
#     found = next(gen_replace_value_with_definition('corse', 'Definition of "corse" via generator'), ('cielo', 'Definition of "cielo" via generator'))
# print(current_dict)


# for word in data:
#     data[word] = find_definition(word)