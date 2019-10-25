import pprint
import json
d = {
  "d": {
    "results": [
      {
        "BaseUom": "ST",
        "BaseUomIso": "PCE",
        "BasicMatl": "W1",
        "BasicMatlNew": "W1",
        "ChangedBy": "ETTRICH",
        "Code": "",
        "Container": "",
        "CreatedBy": "NGSO",
        "CreatedOn": "/Date(1297728000000)/",
        "Division": "50",
        "EanCat": "",
        "EanUpc": "",
        "Emptiesbom": "",
        "GrossWt": "1131.000",
        "Height": "17.000",
        "IndSector": "M",
        "LabDesign": "ALT",
        "LastChnge": "/Date(1540857600000)/",
        "Length": "12.000",
        "LogMsgNo": "",
        "LogNo": "",
        "ManuMat": "",
        "Material": "000000000020",
        "MatlCat": "",
        "MatlDesc": "SCHELLE",
        "MatlGroup": "W310020",
        "MatlType": "ZINV",
        "Message": "",
        "MessageV1": "",
        "MessageV2": "",
        "MessageV3": "",
        "MessageV4": "",
        "MfrNo": "",
        "NetWeight": "3130.000",
        "OldMatNo": "DAIMLER NUMMER",
        "Pageformat": "",
        "ProdHier": "650",
        "ProdMemo": "",
        "SizeDim": "",
        "StdDescr": "N288A",
        "StorConds": "",
        "TempConds": "01",
        "Type": "",
        "UnitDim": "MM",
        "UnitDimIso": "MMT",
        "UnitOfWt": "G",
        "UnitOfWtIso": "GRM",
        "Volume": "11.424",
        "Volumeunit": "CCM",
        "VolumeunitIso": "CMQ",
        "Width": "56.000",
        "__metadata": {
          "id": "https://sap-fes-i.org-intra.net/sap/opu/odata/sap/Y_DIGITAL_TWIN_SRV/MatMasSet('000000000020')",
          "type": "Y_DIGITAL_TWIN_SRV.MatMas",
          "uri": "https://sap-fes-i.org-intra.net/sap/opu/odata/sap/Y_DIGITAL_TWIN_SRV/MatMasSet('000000000020')"
        }
      }
    ]
  }
}


def format(data1):
    _data = []
    for p in data1:
        p.pop("__metadata", {})
        template = {
            "Length": "",
            "Width": "",
            "Height": "",
            "NetWeight": "",
            "GrossWeight": "",
            "LengthUnit": "",
            "WeightUnit": ""
        }
        template["Length"] = p["Length"]
        template["Width"] = p["Width"]
        template["Height"] = p["Height"]
        template["NetWeight"] = p["NetWeight"]
        template["GrossWeight"] = p["GrossWt"]
        template["LengthUnit"] = p["UnitDim"]
        template["WeightUnit"] = p["UnitOfWt"]
        _data.append(template)
    return _data


data1 = d['d']['results']

# pprint.pprint(format(data1))
data = format(data1)
print(data, type(data))
data = json.dumps(data)
print(data, type(data))
