from pprint import pprint

import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn import linear_model


# define the data/predictors as the pre-set feature names
Training_data = "Training.csv"
data = pd.read_csv(Training_data)
df = pd.DataFrame(data=data, columns=['Time', 'Values'])
pprint(df.head())

# Put the target (housing value -- MEDV) in another DataFrame
target = pd.DataFrame(data=data, columns=["EndTime"])
pprint(target.head())

# Note the difference in argument order
ols_model = sm.OLS(target, df).fit()
predictions = ols_model.predict(df)  # make the predictions by the model

# Print out the statistics
# pprint(model.summary())


lm = linear_model.LinearRegression()
lm_model = lm.fit(target, df)
# Print out the statistics
pprint(lm_model.summary())
# predictions = lm.predict(X)
# print(predictions)[0:5]