from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn import metrics
import pickle
import joblib

def model():

    path = "./data_cleaned.csv"
    data = pd.read_csv(path)
    path_saved_model = 'model.sav'

    nominal_columns = ["type","district"]

    dummy_df = pd.get_dummies(data[nominal_columns], drop_first=False) 
    data_df = pd.concat([data, dummy_df], axis=1)
    data_df = data_df.drop(nominal_columns, axis=1)

    y = data_df.pop('duration_hour')
    X = data_df.drop("timestamp",axis = 1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2020)

    model_RF = RandomForestRegressor(bootstrap = False, max_depth = 40, max_features = 10, min_samples_leaf = 3, min_samples_split = 36, n_estimators = 120)

    model_RF.fit(X_train, y_train)

    predictions = model_RF.predict(X_test)

    print('MAE:', metrics.mean_absolute_error(y_test, predictions))
    print('MSE:', metrics.mean_squared_error(y_test, predictions))
    print('RMSE:', np.sqrt(metrics.mean_squared_error(y_test, predictions)))

    pickle.dump(model_RF, open(path_saved_model, 'wb'))

    return path_saved_model

print( "path of model = ",model())





