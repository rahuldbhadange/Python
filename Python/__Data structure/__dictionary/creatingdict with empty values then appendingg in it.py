p = {"UnitDim": "mm", "UnitOfWt": 123}


template = {
    "Length": None,
    "Width": "",
    "Height": "",
    "NetWeight": "",
    "GrossWeight": "",
    "LengthUnit": "",
    "WeightUnit": ""
}

template["Length"] = 90
template["Width"] = "Width"
template["Height"] = "Height"
template["NetWeight"] = "NetWeight"
template["GrossWeight"] = "GrossWt"
template["LengthUnit"] = p["UnitDim"]
template["WeightUnit"] = p["UnitOfWt"]
print(template)
