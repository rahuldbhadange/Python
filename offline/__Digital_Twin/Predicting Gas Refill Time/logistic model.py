from pprint import pprint

import pandas as pd

from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

# define the data/predictors as the pre-set feature names
Training_data = "Training.csv"
columns = ["Cycle", "Type", "Time", "Values"]
data = pd.read_csv(Training_data)
df = pd.DataFrame(data=data, columns=columns)
pprint(df.head())


# Put the target (housing value -- EndTime) in another DataFrame
target = pd.DataFrame(data=data, columns=["EndTime"])
pprint(target.head())



#
# create a base classifier used to evaluate a subset of attributes
model = LogisticRegression()

# create the RFE model and select 3 attributes
rfe = RFE(model, 4)
rfe = rfe.fit(data, target)

# summarize the selection of the attributes
print(rfe.support_)
print(rfe.ranking_)
