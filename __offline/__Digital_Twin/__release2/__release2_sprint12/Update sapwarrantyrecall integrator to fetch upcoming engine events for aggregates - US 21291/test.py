import re
from pprint import pprint

eng = {
    "d": {
        "results": [
            {
                "Pnguid": "AFBWiyhYHtiE5aq+SeSqiw==",
                "Pncnt": "00000001",
                "HPntext": "2018.02.16.0001",
                "Clmno": "000440000120",
                "Clmty": "YCIF",
                "Refdt": "\/Date(1514764800000)\/",
                "Refno": "2018.02.16.0001",
                "Sernr": "",
                "Equnr": "000000000200000081",
                "Parnr": "",
                "Astate": "YC20",
                "Abdes": "Active",
                "YywtyState": "",
                "YycifPrio": "M",
                "YycifPriotxt": "Modifikation",
                "Yyroopen": "0000-00-00",
                "Yyroclosed": "0000-00-00",
                "YydueDate": "2018-12-31",
                "Yysystfir": "",
                "Yyclmtype": "",
                "Yyclmtypetxt": "",
                "Yyrepcountry": "",
                "DocLink": "HTTP://WWW.PRORATA-NOW.COM"
            },
            {
                "Pnguid": "AFBWiyhYHtiE5aq+SeSqiw==",
                "Pncnt": "00000001",
                "HPntext": "2018.02.16.0001",
                "Clmno": "000440000120",
                "Clmty": "YCIF",
                "Refdt": "\/Date(1514764800000)\/",
                "Refno": "2018.02.16.0001",
                "Sernr": "",
                "Equnr": "000000000200000081",
                "Parnr": "",
                "Astate": "YC20",
                "Abdes": "Active",
                "YywtyState": "",
                "YycifPrio": "M",
                "YycifPriotxt": "Modifikation",
                "Yyroopen": "0000-00-00",
                "Yyroclosed": "0000-00-00",
                "YydueDate": "2018-12-31",
                "Yysystfir": "",
                "Yyclmtype": "",
                "Yyclmtypetxt": "",
                "Yyrepcountry": "",
                "DocLink": "HTTP://WWW.PRORATA-NOW.COM"
            }
        ]
    }
}

agg = {
    "d": {
        "results": [
            {
                "__metadata": {
                    "id": "https://sap-fes-i.org-intra.net:443/sap/opu/odata/sap/Y_DIGITAL_TWIN_SRV/WTYRCLSet(Pnguid=binary'0050568B28581ED884E5AABE49E4AA8B',Pncnt='00000001')",
                    "uri": "https://sap-fes-i.org-intra.net:443/sap/opu/odata/sap/Y_DIGITAL_TWIN_SRV/WTYRCLSet(Pnguid=binary'0050568B28581ED884E5AABE49E4AA8B',Pncnt='00000001')",
                    "type": "Y_DIGITAL_TWIN_SRV.WTYRCL"
                },
                "Pnguid": "AFBWiyhYHtiE5aq+SeSqiw==",
                "Pncnt": "00000001",
                "HPntext": "2018.02.16.0001",
                "Clmno": "000440000120",
                "Clmty": "YCIF",
                "Refdt": "\/Date(1514764800000)\/",
                "Refno": "2018.02.16.0001",
                "Sernr": "",
                "Equnr": "000000000010000018",
                "Parnr": "",
                "Astate": "YC20",
                "Abdes": "Active",
                "YywtyState": "",
                "YycifPrio": "M",
                "YycifPriotxt": "Modifikation",
                "Yyroopen": "2018-12-31",
                "Yyroclosed": "2018-12-31",
                "YydueDate": "2018-12-31",
                "Yysystfir": "",
                "Yyclmtype": "",
                "Yyclmtypetxt": "",
                "Yyrepcountry": "",
                "DocLink": "HTTP://WWW.PRORATA-NOW.COM"
            },
            {
                "__metadata": {
                    "id": "https://sap-fes-i.org-intra.net:443/sap/opu/odata/sap/Y_DIGITAL_TWIN_SRV/WTYRCLSet(Pnguid=binary'0050568B28581ED884E627BD57172A8B',Pncnt='00000001')",
                    "uri": "https://sap-fes-i.org-intra.net:443/sap/opu/odata/sap/Y_DIGITAL_TWIN_SRV/WTYRCLSet(Pnguid=binary'0050568B28581ED884E627BD57172A8B',Pncnt='00000001')",
                    "type": "Y_DIGITAL_TWIN_SRV.WTYRCL"
                },
                "Pnguid": "AFBWiyhYHtiE5ie9Vxcqiw==",
                "Pncnt": "00000001",
                "HPntext": "2018.02.16.0002",
                "Clmno": "000440000121",
                "Clmty": "YCIF",
                "Refdt": "\/Date(1514764800000)\/",
                "Refno": "2018.02.16.0002",
                "Sernr": "",
                "Equnr": "000000000010000018",
                "Parnr": "",
                "Astate": "YC20",
                "Abdes": "Active",
                "YywtyState": "",
                "YycifPrio": "M",
                "YycifPriotxt": "Modifikation",
                "Yyroopen": "0000-00-00",
                "Yyroclosed": "0000-00-00",
                "YydueDate": "2018-12-31",
                "Yysystfir": "",
                "Yyclmtype": "",
                "Yyclmtypetxt": "",
                "Yyrepcountry": "",
                "DocLink": "http://www.google.de"
            },
            {
                "__metadata": {
                    "id": "https://sap-fes-i.org-intra.net:443/sap/opu/odata/sap/Y_DIGITAL_TWIN_SRV/WTYRCLSet(Pnguid=binary'0050568B28581ED88690195AE1176A8B',Pncnt='00000001')",
                    "uri": "https://sap-fes-i.org-intra.net:443/sap/opu/odata/sap/Y_DIGITAL_TWIN_SRV/WTYRCLSet(Pnguid=binary'0050568B28581ED88690195AE1176A8B',Pncnt='00000001')",
                    "type": "Y_DIGITAL_TWIN_SRV.WTYRCL"
                },
                "Pnguid": "AFBWiyhYHtiGkBla4Rdqiw==",
                "Pncnt": "00000001",
                "HPntext": "Text",
                "Clmno": "000440000122",
                "Clmty": "YCIF",
                "Refdt": "\/Date(1514764800000)\/",
                "Refno": "2018.02.16.0004",
                "Sernr": "",
                "Equnr": "000000000010000018",
                "Parnr": "",
                "Astate": "YC20",
                "Abdes": "Active",
                "YywtyState": "",
                "YycifPrio": "M",
                "YycifPriotxt": "Modifikation",
                "Yyroopen": "0000-00-00",
                "Yyroclosed": "0000-00-00",
                "YydueDate": "2018-12-31",
                "Yysystfir": "",
                "Yyclmtype": "",
                "Yyclmtypetxt": "",
                "Yyrepcountry": "",
                "DocLink": ""
            },
            {
                "__metadata": {
                    "id": "https://sap-fes-i.org-intra.net:443/sap/opu/odata/sap/Y_DIGITAL_TWIN_SRV/WTYRCLSet(Pnguid=binary'0050568B28581EE88895A72B310C232F',Pncnt='00000001')",
                    "uri": "https://sap-fes-i.org-intra.net:443/sap/opu/odata/sap/Y_DIGITAL_TWIN_SRV/WTYRCLSet(Pnguid=binary'0050568B28581EE88895A72B310C232F',Pncnt='00000001')",
                    "type": "Y_DIGITAL_TWIN_SRV.WTYRCL"
                },
                "Pnguid": "AFBWiyhYHuiIlacrMQwjLw==",
                "Pncnt": "00000001",
                "HPntext": "Pro rata classic",
                "Clmno": "000440000130",
                "Clmty": "YCIF",
                "Refdt": "\/Date(1514764800000)\/",
                "Refno": "2018.02.16.0099",
                "Sernr": "",
                "Equnr": "000000000010000018",
                "Parnr": "",
                "Astate": "YC20",
                "Abdes": "Active",
                "YywtyState": "",
                "YycifPrio": "M",
                "YycifPriotxt": "Modifikation",
                "Yyroopen": "0000-00-00",
                "Yyroclosed": "0000-00-00",
                "YydueDate": "2018-12-31",
                "Yysystfir": "",
                "Yyclmtype": "",
                "Yyclmtypetxt": "",
                "Yyrepcountry": "",
                "DocLink": ""
            },
            {
                "__metadata": {
                    "id": "https://sap-fes-i.org-intra.net:443/sap/opu/odata/sap/Y_DIGITAL_TWIN_SRV/WTYRCLSet(Pnguid=binary'0050568B4AE61EE885C714AE8D99FA5B',Pncnt='00000001')",
                    "uri": "https://sap-fes-i.org-intra.net:443/sap/opu/odata/sap/Y_DIGITAL_TWIN_SRV/WTYRCLSet(Pnguid=binary'0050568B4AE61EE885C714AE8D99FA5B',Pncnt='00000001')",
                    "type": "Y_DIGITAL_TWIN_SRV.WTYRCL"
                },
                "Pnguid": "AFBWi0rmHuiFxxSujZn6Ww==",
                "Pncnt": "00000001",
                "HPntext": "PRO-RATATATA",
                "Clmno": "000440000111",
                "Clmty": "YCIF",
                "Refdt": "\/Date(1514764800000)\/",
                "Refno": "2018.02.16.0003",
                "Sernr": "",
                "Equnr": "000000000010000018",
                "Parnr": "",
                "Astate": "YC20",
                "Abdes": "Active",
                "YywtyState": "",
                "YycifPrio": "M",
                "YycifPriotxt": "Modifikation",
                "Yyroopen": "0000-00-00",
                "Yyroclosed": "0000-00-00",
                "YydueDate": "2018-12-31",
                "Yysystfir": "",
                "Yyclmtype": "",
                "Yyclmtypetxt": "",
                "Yyrepcountry": "",
                "DocLink": "http://www.dsc-eishockey.de/"
            },
            {
                "__metadata": {
                    "id": "https://sap-fes-i.org-intra.net:443/sap/opu/odata/sap/Y_DIGITAL_TWIN_SRV/WTYRCLSet(Pnguid=binary'0050568B4AE61EE887BFBA0B88ACBA5B',Pncnt='00000001')",
                    "uri": "https://sap-fes-i.org-intra.net:443/sap/opu/odata/sap/Y_DIGITAL_TWIN_SRV/WTYRCLSet(Pnguid=binary'0050568B4AE61EE887BFBA0B88ACBA5B',Pncnt='00000001')",
                    "type": "Y_DIGITAL_TWIN_SRV.WTYRCL"
                },
                "Pnguid": "AFBWi0rmHuiHv7oLiKy6Ww==",
                "Pncnt": "00000001",
                "HPntext": "german info",
                "Clmno": "000440000112",
                "Clmty": "YCIF",
                "Refdt": "\/Date(1514764800000)\/",
                "Refno": "2018.02.16.0005",
                "Sernr": "",
                "Equnr": "000000000010000018",
                "Parnr": "",
                "Astate": "YC20",
                "Abdes": "Active",
                "YywtyState": "",
                "YycifPrio": "M",
                "YycifPriotxt": "Modifikation",
                "Yyroopen": "0000-00-00",
                "Yyroclosed": "0000-00-00",
                "YydueDate": "2018-12-31",
                "Yysystfir": "",
                "Yyclmtype": "",
                "Yyclmtypetxt": "",
                "Yyrepcountry": "",
                "DocLink": ""
            }
        ]
    }
}

# pprint(agg)
# pprint(eng)

_agg = agg["d"]["results"]
_eng = eng["d"]["results"]

events = []
# pprint(events)

for item in _agg:
    item['AssetType'] = 'SYS'
    # item['Refdt'] = int(re.findall(r'\d+', item['Refdt'])[0])
    # item['Refdt'] = re.find...

    events.append(item)

# pprint(events)

for item in _eng:
    # item['Refdt'] = re.find...
    item['AssetType'] = 'ENG'
    events.append(item)
pprint(events)
