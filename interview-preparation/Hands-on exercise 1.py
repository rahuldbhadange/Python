import pandas as pd
from pandas import DataFrame as df

_file_path = "./height-weight.csv"

data_frame = pd.read_csv(_file_path, sep="\t")

print(data_frame.head())

data_frame["Height"] = data_frame["HEIGHT(INCHES)"].map(lambda inches: round(inches * 0.083333, 2))
print(data_frame.head())

data_frame["Weight"] = data_frame["WEIGHT(POUNDS)"].map(lambda pounds: round(pounds * 0.4535, 2))
print(data_frame.head())

df = data_frame[["Height"]["Weight"]]
print(df.head())
print(len(df.index))
