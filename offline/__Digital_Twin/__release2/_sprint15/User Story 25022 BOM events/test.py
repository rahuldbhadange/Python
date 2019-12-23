# Copyright (c) 2019 Rolls-Royce Power Systems AG. All rights reserved.

import datetime
import math
from pprint import pprint

import pytz

from rrps.dt.events import SapBomAsIbaseChangesSet
from rrps.dt.follower.rest_follower.views import RiverOfNewsView, BasicDataView


def test_listing(app_client, data_access):
    event_time = datetime.datetime.utcnow().replace(microsecond=0) - datetime.timedelta(hours=25)
    start_timestamp = math.floor(event_time.timestamp())
    basic_data = BasicDataView(data_access)
    ron_view = RiverOfNewsView(data_access, basic_data)

    Crtim = "20180212085321"
    Uptim = "20180212085436"
    Valfr = "20180212085209"
    Valto = "20180212085427"
    _Valfr = int(Valfr)

    event = SapBomAsIbaseChangesSet("123", source="src", time=datetime.datetime.now(), data=[
             {'Crtim': int(datetime.datetime.timestamp
                           (pytz.utc.localize(datetime.datetime.strptime(Crtim, "%Y%m%d%H%M%S")))),
              'InRecno': '',
              'Maktx': 'DIESEL ENGINE',
              'Matnr': '12V4000G23',
              'Sernr': '000000000526104878',
              'Uptim': int(datetime.datetime.timestamp
                           (pytz.utc.localize(datetime.datetime.strptime(Uptim, "%Y%m%d%H%M%S")))),
              'Valfr': int(datetime.datetime.timestamp
                           (pytz.utc.localize(datetime.datetime.strptime(Valfr, "%Y%m%d%H%M%S")))),
              'Valto': int(datetime.datetime.timestamp
                           (pytz.utc.localize(datetime.datetime.strptime(Valto, "%Y%m%d%H%M%S"))))},
             {'Crtim': int(datetime.datetime.timestamp
                           (pytz.utc.localize(datetime.datetime.strptime(Crtim, "%Y%m%d%H%M%S")))),
              'InRecno': '051MYoXO7kM{}}PXdttEkG',
              'Maktx': 'OIL PUMP',
              'Matnr': 'XS526180.00006',
              'Sernr': '000000000526104875',
              'Uptim': None,
              'Valfr': int(datetime.datetime.timestamp
                           (pytz.utc.localize(datetime.datetime.strptime(Valfr, "%Y%m%d%H%M%S")))),
              'Valto': None}
        ]
    )

    # dt = datetime.datetime.strptime(timestring, "%Y%m%d%H%M%S")
# int(datetime.datetime.timestamp(pytz.utc.localize(datetime.datetime.strptime(timestring, "%Y%m%d%H%M%S"))))



    # "Sernr": "000000000526104875",
    # "Ibase": "000000000000001130",
    # "Crnam": "NO",
    # "Crtim": "20180212085321",
    # "Upnam": "NO",
    # "Uptim": "20180212085436",
    # "InRecno": "",
    # "Matnr": "12V4000G23",
    # "Maktx": "DIESEL ENGINE",
    # "Valfr": "20180212085209",
    # "Valto": "20180212085427",
    # "Sortf": "077/05"


    ron_view.on_event(event)

    # IbaseChanges = app_client.open("/ron/123").json
    # # pprint(IbaseChanges)
    #
    # assert IbaseChanges["Source"] == "SapBoM"
    # assert IbaseChanges["Type"] == "SapBomIBaseChanges"
    # assert IbaseChanges["Description"] == "BoM event: Removal"
    # assert IbaseChanges["Attachments"] == []
    #
    # assert IbaseChanges["Details"]["DateofInstallation"] == pytz.utc.localize(
    #     datetime.datetime.fromtimestamp(start_timestamp + 3660)).isoformat()
    # assert IbaseChanges["Details"]["IBaseRecord"] == "051MYoXO7jY7gUfL1tlgYm"
    # assert IbaseChanges["Details"]["MaterialNumber"] == "12V4000G23"
    # assert IbaseChanges["Details"]["Description"] == "DIESEL ENGINE"

    IbaseChanges = app_client.open("/ron/123").json

    pprint(IbaseChanges)

    assert len(IbaseChanges) == 2

    assert IbaseChanges[0]["Source"] == "src"
    assert IbaseChanges[0]["Type"] == "SapBomIBaseChanges"
    assert IbaseChanges[0]["Description"] == "BoM event: Removal"
    assert IbaseChanges[0]["Attachments"] == []

    assert len(IbaseChanges[0]["Details"]) == 1

    assert IbaseChanges[0]["Details"][0]["DateofRemoval"] == datetime.datetime.utcfromtimestamp(int(datetime.datetime.timestamp
                           (pytz.utc.localize(datetime.datetime.strptime(Valfr, "%Y%m%d%H%M%S"))))).strftime("%Y-%m-%d") # '2018-02-12'
    assert IbaseChanges[0]["Details"][0]["Description"] == "DIESEL ENGINE"
    assert IbaseChanges[0]["Details"][0]["IBaseRecord"] == ""
    assert IbaseChanges[0]["Details"][0]["MaterialNumber"] == "12V4000G23"

    assert IbaseChanges[1]["Source"] == "src"
    assert IbaseChanges[1]["Type"] == "SapBomIBaseChanges"
    assert IbaseChanges[1]["Description"] == "BoM event: Installation"
    assert IbaseChanges[1]["Attachments"] == []

    assert len(IbaseChanges[1]["Details"]) == 1

    assert IbaseChanges[1]["Details"][0]["DateofInstallation"] == datetime.datetime.utcfromtimestamp(int(datetime.datetime.timestamp
                           (pytz.utc.localize(datetime.datetime.strptime(Valfr, "%Y%m%d%H%M%S"))))).strftime("%Y-%m-%d") # '2016-04-06'
    assert IbaseChanges[1]["Details"][0]["Description"] == "OIL PUMP"
    assert IbaseChanges[1]["Details"][0]["IBaseRecord"] == "051MYoXO7kM{}}PXdttEkG"
    assert IbaseChanges[1]["Details"][0]["MaterialNumber"] == "XS526180.00006"


#     valto = datetime.datetime.utcfromtimestamp(Valfr)
#
#
# data_to_add = {}
#
# if valto:
#     date_of_removal = datetime.datetime.utcfromtimestamp(Valfr).strftime("%Y-%m-%d")
#


    # [{'Attachments': [],
    #   'Description': 'BoM event: Removal',
    #   'Details': [{'DateofRemoval': '2018-02-12',
    #                'Description': 'DIESEL ENGINE',
    #                'IBaseRecord': '',
    #                'MaterialNumber': '12V4000G23'}],
    #   'Seq': -1,
    #   'Source': 'src',
    #   'Ts': '2019-08-07T15:57:41.854271+00:00',
    #   'Type': 'SapBomIBaseChanges'},
    #  {'Attachments': [],
    #   'Description': 'BoM event: Installation',
    #   'Details': [{'DateofInstallation': '2016-04-06',
    #                'Description': 'OIL PUMP',
    #                'IBaseRecord': '051MYoXO7kM{}}PXdttEkG',
    #                'MaterialNumber': 'XS526180.00006'}],
    #   'Seq': -1,
    #   'Source': 'src',
    #   'Ts': '2019-08-07T15:57:41.854271+00:00',
    #   'Type': 'SapBomIBaseChanges'}]






    # {'Attachments': [],
    #  'Description': 'BoM event: Installation',
    #  'Details': [{'DateofInstallation': '2016-04-06',
    #               'Description': 'OIL PUMP',
    #               'IBaseRecord': '051MYoXO7kM{}}PXdttEkG',
    #               'MaterialNumber': 'XS526180.00006'}],
    #  'Seq': 4084,
    #  'Source': 'SapBoM',
    #  'Ts': '2016-04-06T13:58:55+00:00',
    #  'Type': 'SapBomIBaseChanges',
    #  'asset_id': '1000015'}

    # {'Attachments': [],
    #  'Description': 'BoM event: Removal',
    #  'Details': [{'DateofRemoval': '2016-02-02',
    #               'Description': 'OIL PUMP',
    #               'IBaseRecord': '051MYqhc7kM{vWd52Pl9c0',
    #               'MaterialNumber': 'XS526180.00006'}],
    #  'Seq': 4085,
    #  'Source': 'SapBoM',
    #  'Ts': '2016-04-06T13:58:55+00:00',
    #  'Type': 'SapBomIBaseChanges',
    #  'asset_id': '1000015'}
