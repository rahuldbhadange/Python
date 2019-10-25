import pandas as pd
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt


# define the data/predictors as the pre-set feature names
Training_data = "Training.csv"
Target_data = "Target.csv"
Testing_data = "Testing.csv"

columns = ["Time", "Values"]   # "Cycle", "Type", "Time", "Values"

Training_data = pd.read_csv(Training_data)
Target_data = pd.read_csv(Target_data)
Testing_data = pd.read_csv(Testing_data)


X = pd.DataFrame(data=Training_data, columns=columns)
print(X.head())

# Put the target (housing value -- EndTime) in another DataFrame
Y = pd.DataFrame(data=Target_data, columns=["EndTime"])
# print(Y.head())

X_ = pd.DataFrame(data=Testing_data[:-99], columns=columns)
print(X_.head())
lm = LinearRegression()
# lm = Lasso()
lm_model = lm.fit(X, Y)


predictions = lm.predict(X_)


print('\nCoefficient of determination (R-Square) :', lm.score(X, Y))
print('\nSlope:', lm_model.coef_)
print('\nIntercept:', lm_model.intercept_)
print("\nPredictions:\n", predictions)


# The mean squared error
# print("Mean squared error: %.2f"
#       % mean_squared_error(X, predictions))
# # Explained variance score: 1 is perfect prediction
# print('Variance score: %.2f' % r2_score(X, X_))

# Coefficient of determination (R-Square) (Variation) (0-1) : should be maximum


# Plot outputs
# plt.scatter(X_, Y,  color='black')
# plt.plot(X_, X, color='blue', linewidth=3)

# plt.xticks(())
# plt.yticks(())
#
# plt.scatter(X, Y)
# plt.show()
















































# Calculate the mean value of a list of numbers
def mean(values):
	return sum(values) / float(len(values))


# Calculate the variance of a list of numbers
def variance(values, mean):
	return sum([(x-mean)**2 for x in values])

# variance = sum( (x - mean(x))^2 )

# Calculate the mean value of a list of numbers
def mean(values):
    return sum(values) / float(len(values))

# Calculate the variance of a list of numbers
def variance(values, mean):
    return sum([(x-mean)**2 for x in values])


# calculate mean and variance
# dataset = [[1, 1], [2, 3], [4, 3], [3, 2], [5, 5]]
Cycle = [row[0] for row in Training_data]
Type = [row[1] for row in Training_data]
Time = [row[0] for row in Training_data]
Values = [row[0] for row in Training_data]

# mean_Cycle, mean_Type = mean(Cycle), mean(Type)
mean_Time = mean(Time)
mean_Values = mean(Values)
# var_Cycle, var_Type = variance(Cycle, mean_Cycle), variance(Type, mean_Type)
var_Time = variance(Time, mean_Time)
var_Values = variance(Values, mean_Values)
# print('x stats: mean=%.3f variance=%.3f' % (mean_Cycle, var_Cycle))
# print('y stats: mean=%.3f variance=%.3f' % (mean_Cycle, var_Type))
print('Time stats: mean=%.3f variance=%.3f' % (mean_Time, var_Time))
print('Values stats: mean=%.3f variance=%.3f' % (mean_Values, var_Values))


"""import pyplotlib.pyplot as py
py.scatter(x_axis_value,y_axis_value,color=’black’)
py.show()"""