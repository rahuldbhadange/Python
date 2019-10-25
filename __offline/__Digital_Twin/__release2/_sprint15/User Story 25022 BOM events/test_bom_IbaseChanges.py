# Copyright (c) 2019 Rolls-Royce Power Systems AG. All rights reserved.

import datetime
import math
import pytz

from rrps.dt.events import SapBomAsIbaseChangesSet
from rrps.dt.follower.rest_follower.views import RiverOfNewsView, BasicDataView


def test_listing(app_client, data_access):
    event_time = datetime.datetime.utcnow().replace(microsecond=0) - datetime.timedelta(hours=25)
    start_timestamp = math.floor(event_time.timestamp())
    basic_data = BasicDataView(data_access)
    ron_view = RiverOfNewsView(data_access, basic_data)

    event = SapBomAsIbaseChangesSet("123", source="src", time=datetime.datetime.now(), data=[
             {'Crtim': 1518425601,
              'InRecno': '',
              'Maktx': 'DIESEL ENGINE',
              'Matnr': '12V4000G23',
              'Sernr': '000000000526104878',
              'Uptim': 1518425676,
              'Valfr': 1518425529,
              'Valto': 1518425667}#,
             # {'Crtim': 1519910569,
             #  'InRecno': '051MYoXO7jY7gdH2GU5gYm',
             #  'Maktx': 'DIESEL ENGINE',
             #  'Matnr': '12V4000G23',
             #  'Sernr': '000000000526104875',
             #  'Uptim': 1519910586,
             #  'Valfr': 1519910555,
             #  'Valto': 1519910583},
             # {'Crtim': 1519910586,
             #  'InRecno': '051MYoXO7jY7gdLWN1DgYm',
             #  'Maktx': '',
             #  'Matnr': '',
             #  'Sernr': '000000000526104875',
             #  'Uptim': 1519991558,
             #  'Valfr': 1519910583,
             #  'Valto': 1519991553},
             # {'Crtim': 1459951135,
             #  'InRecno': '051MYoXO7kM{}}HruQqEkG',
             #  'Maktx': '',
             #  'Matnr': '',
             #  'Sernr': '000000000526104875',
             #  'Uptim': 1518425601,
             #  'Valfr': 1459951086,
             #  'Valto': 1518425529},
             # {'Crtim': 1459951135,
             #  'InRecno': '051MYoXO7kM{}}PXdttEkG',
             #  'Maktx': 'OIL PUMP',
             #  'Matnr': 'XS526180.00006',
             #  'Sernr': '000000000526104875',
             #  'Uptim': None,
             #  'Valfr': 1459951086,
             #  'Valto': None},
             # {'Crtim': 1459862064,
             #  'InRecno': '051MYqhc7kM{vWd52ZNfc0',
             #  'Maktx': 'PLATE',
             #  'Matnr': '000.00899',
             #  'Sernr': '000000000526104875',
             #  'Uptim': 1460020345,
             #  'Valfr': 1454425731,
             #  'Valto': 1460020312},
             # {'Crtim': 1460020656,
             #  'InRecno': '051MYqhc7kM}b36CFGR9c0',
             #  'Maktx': 'PLATE',
             #  'Matnr': '000.00899',
             #  'Sernr': '000000000526104875',
             #  'Uptim': None,
             #  'Valfr': 1460020641,
             #  'Valto': None},
             # {'Crtim': 1519991558,
             #  'InRecno': '051MYqhc7kY7mWN{RScwMm',
             #  'Maktx': 'DIESEL ENGINE',
             #  'Matnr': '12V4000G23',
             #  'Sernr': '000000000526104875',
             #  'Uptim': 1519991581,
             #  'Valfr': 1519991553,
             #  'Valto': 1519991577},
             # {'Crtim': 1519991581,
             #  'InRecno': '051MYqhc7kY7mWUSOt4wMm',
             #  'Maktx': '',
             #  'Matnr': '',
             #  'Sernr': '000000000526104875',
             #  'Uptim': None,
             #  'Valfr': 1519991577,
             #  'Valto': None},
             # {'Crtim': 1559917459,
             #  'InRecno': '051Ma4RC7jcYfVq4dD}H5m',
             #  'Maktx': 'FLUIDS/LUBRICANTS    FOR ENGINE',
             #  'Matnr': 'A001061/33E',
             #  'Sernr': '000000000526104875',
             #  'Uptim': None,
             #  'Valfr': 1559917420,
             #  'Valto': None
             #  }
        ]
    )

    ron_view.on_event(event)

    IbaseChanges = app_client.open("/engine-bom-as-maintained/1234").json
    # assert len(IbaseChanges) == 1
    assert IbaseChanges["Source"] == "SapBoM"
    assert IbaseChanges["Type"] == "SapBomIBaseChanges"
    assert IbaseChanges["Description"] == "BoM event: Removal"
    assert IbaseChanges["Attachments"] == []

    # assert len(IbaseChanges["Details"]) == 1

    assert IbaseChanges["Details"]["DateofInstallation"] == pytz.utc.localize(
        datetime.datetime.fromtimestamp(start_timestamp + 3660)).isoformat()
    assert IbaseChanges["Details"]["IBaseRecord"] == "051MYoXO7jY7gUfL1tlgYm"
    assert IbaseChanges["Details"]["MaterialNumber"] == "12V4000G23"
    assert IbaseChanges["Details"]["Description"] == "DIESEL ENGINE"



    IbaseChanges = app_client.open("/engine-bom-as-maintained/1234").json

    assert len(IbaseChanges) == 1
    assert IbaseChanges["Source"] == "SapBoM"
    assert IbaseChanges["Type"] == "SapBomIBaseChanges"
    assert IbaseChanges["Description"] == "BoM event: Installation"
    assert IbaseChanges["Attachments"] == []

    assert len(IbaseChanges["Details"]) == 1

    assert IbaseChanges["Details"][0]["DateofInstallation"] == pytz.utc.localize(
        datetime.datetime.fromtimestamp(start_timestamp + 3660)).isoformat()
    assert IbaseChanges["Details"][0]["IBaseRecord"] == "051MYoXO7kM{}}PXdttEkG"
    assert IbaseChanges["Details"][0]["MaterialNumber"] == "XS526180.00006"
    assert IbaseChanges["Details"][0]["Description"] == "OIL PUMP"

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
