location = {'lat': 52.427809, 'long': -0.327829, 'radius': 10.789}
location1 = {'lat': 52.427809, 'long': -0.327829, 'radius': 10.789}
location2 = {'lat': 52.427809, 'long': -0.327829, 'radius': 10.789}

for radius in range(10):
    print(location["radius"])
    # for radius in location1:
    location["radius"] += 1
    print(location["radius"])
    #     for radius in location2:
    #         location["radius"] += 1
    #         print(location["radius"])
