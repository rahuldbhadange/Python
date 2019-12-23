from pprint import pprint

data = {
      "d": {
            "results": [
                      {
                        "Equnr": "000000000200000465",
                        "Sernr": "1000015",
                        "Eqart": "SYS",
                        "Hequi": "2"
                      },

                      {
                        "Equnr": "000000000200000031",
                        "Sernr": "4711-0006",
                        "Eqart": "ENG",
                        "Hequi": "000000000200000465"
                      },
                    {
                        "Equnr": "000000000200000465555555555555555555555555555555555",
                        "Sernr": "1000016",
                        "Eqart": "SYS",
                        "Hequi": "25"
                    },

                    {
                        "Equnr": "00000000020000003111111111111111111111111111111111111",
                        "Sernr": "4711-0007",
                        "Eqart": "ENG",
                        "Hequi": "000000000200000465"
                    },
                    {
                        "Equnr": "000000000200000465666666666666666666666666666666666666666666666",
                        "Sernr": "1000015",
                        "Eqart": "SYS",
                        "Hequi": ""
                    },

                    {
                        "Equnr": "00000000020000003111111111111111111111111111111111111",
                        "Sernr": "4711-00066666666666666666666666666666666666666666",
                        "Eqart": "ENG",
                        "Hequi": "000000000200000465666666666666666666666666666666666666666666666"
                    }
                ]
          }
        }

aggregate_equipment_number = None
engine_serial = None

results = data['d']['results']
pprint(results)
print("\n")
for d in results:
# while results["Hequi"] == "":
    if d['Hequi'] == "":
        aggregate_equipment_number = d['Equnr']
for d in results:
    if d["Hequi"] == aggregate_equipment_number and d["Eqart"] == "ENG":
        engine_serial = d["Sernr"]
# else:
#     aggregate_equipment_number = data['d']['results'][1]['Equnr']
print("\n")
print(aggregate_equipment_number)
print("\n")
print(engine_serial)


# master_data = data['d']['results'][0]
