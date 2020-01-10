from matplotlib import pyplot
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error

dataset = pd.read_excel("C:\Futures\Futures.xls")
dataset['CO Last'] = dataset['CO Last'].str.rstrip('s')
dataset['Contracts'] = dataset['Contracts'].str.rstrip('(E)')
dataset['Contracts'] = pd.to_datetime(dataset['Contracts'])
dataset = dataset.set_index('Contracts')

X = dataset[['NG High', 'NG Low', 'NG Last', 'NG Volumes']]
y = dataset['NG Open']

gbrt = GradientBoostingRegressor()
kfold = KFold(n_splits=10, random_state=7, shuffle=True)
results = cross_val_score(gbrt, X, y, cv=kfold)
print("Accuracy: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))


gbrt.fit(X_train, y_train)
y_pred = gbrt.predict(X_test)


lin_mse = mean_squared_error(y_pred, y_test)
lin_rmse = np.sqrt(lin_mse)
print('Liner Regression RMSE: %.4f' % lin_rmse)
