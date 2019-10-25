description = ["SAP Equipment History", "Master Data Change", "FSW Version", "BoM as built set", "Technical Document"]


dictOfWords = {"Description": i for i in description}

print(dictOfWords)

description = ["SAP Master Data Set", "SAP Equipment History", "Equipment History", "BOM as Built"]
des_list = []
des_dict = {}
for data in description:
    des_dict["Description"] = data
    des_list.append(des_dict)
    print(des_list)
