from pprint import pprint

import datetime as datetime


data = {
  "d" : {
    "results" : [
      {
        "__metadata" : {
                          "id" : "https://sap-fes-i.org-intra.net/sap/opu/odata/sap/Y_DIGITAL_TWIN_SRV/EQUI01Set('000000000200000082')",
                          "uri" : "https://sap-fes-i.org-intra.net/sap/opu/odata/sap/Y_DIGITAL_TWIN_SRV/EQUI01Set('000000000200000082')",
                          "type" : "Y_DIGITAL_TWIN_SRV.EQUI01"
                        },
        "Equnr" : "000000000200000082",
        "Matnr" : "R16V4000G83",
        "Maktx" : "R16V4000G83 REMAN ENGINE",
        "Sernr" : "4711-001",
        "Kunde" : "0022111236",
        "Name1" : "Land Badenwürtenberg",
        "Datab" : "2017-09-08",
        "Datbi" : "2017-09-08",
        "Yybau" : "030",
        "Yyerz" : "10V1600A50",
        "Vkbur" : "0101",
        "Eqart" : "SYS",
        "EquiPartSet" : {
                          "__deferred" : {
                                            "uri" : "https://sap-fes-i.org-intra.net/sap/opu/odata/sap/Y_DIGITAL_TWIN_SRV/EQUI01Set('000000000200000082')/EquiPartSet"
                                          }
                            }
      }
    ]
  }
}


event_data = data['d']['results'][0]
print(event_data['Datab'])
print(event_data['Datbi'])

print("\n\n\n\n")
event_data['Datab'] = datetime.datetime.strptime(event_data['Datab'], '%Y-%m-%d').timestamp() * 1000

event_data['Datbi'] = datetime.datetime.strptime(event_data['Datbi'], '%Y-%m-%d').timestamp() * 1000
event_data['EqunrAgg'] = event_data['Equnr']
event_data['MaktxAgg'] = event_data['Maktx']
event_data['MatnrAgg'] = event_data['Matnr']
event_data['SernrAgg'] = event_data['Sernr']


print(type(event_data))
pprint(event_data)
# for d in event_data:
for field in ('Equnr', 'Maktx', 'Matnr', 'Sernr'):
    del event_data[field]
#
print("\n\n\n\n")
pprint(event_data)

print("\n\n\n\n")
event_time = event_data['Datab']
event_time = datetime.datetime.utcfromtimestamp(event_time // 1000)
print(event_data['Datab'])
print(event_time)