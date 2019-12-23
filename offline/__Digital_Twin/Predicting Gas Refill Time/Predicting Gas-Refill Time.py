from pprint import pprint

import pandas as pd
from sklearn import linear_model

# Recursive Feature Elimination
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

Training_data = "Training.csv"
Testing_data = "Testing.csv"


Training = pd.read_csv(Training_data)

X_Training = Training[:-20]
pprint(X_Training.head())
X_Testing = Training[-20:]
pprint(X_Testing.head())


Testing = pd.read_csv(Testing_data)
Y_Training = Testing[:-20]
pprint(Y_Training.head())
Y_Testing = Testing[-20:]
pprint(Y_Testing.head())

# Create linear regression object
regression = linear_model.LinearRegression()
regression.fit(X_Training, Y_Training)


# create a base classifier used to evaluate a subset of attributes
model = LogisticRegression()


# create the RFE model and select 3 attributes
rfe = RFE(model, 3)
rfe = rfe.fit(Training_data.data, Training_data.target)

# summarize the selection of the attributes
# print(rfe.support_)
# print(rfe.ranking_)
