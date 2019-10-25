location = {'lat': 52.427809, 'long': -0.327829, 'radius': {'radius1': 10.788889}}
location1 = {'lat': 52.427809, 'long': -0.327829, 'radius': 10.789}
location2 = {'lat': 52.427809, 'long': -0.327829, 'radius': 10.789}

for radius in range(5):
    print(location["radius"]["radius1"])
    for radius in location1:
        print('inner1')
        for radius in location2:
            print("inner2")
    # location["radius"] += 1