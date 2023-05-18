from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn import metrics
from urllib.parse import urlparse
import pickle
import joblib
import mlflow
import time

path = "airflow/dags/data/cleaned_data.csv"

data = pd.read_csv(path)
path_saved_model = 'model.sav'

nominal_columns = ["type","district"]

dummy_df = pd.get_dummies(data[nominal_columns], drop_first=False) 
data_df = pd.concat([data, dummy_df], axis=1)
data_df = data_df.drop(nominal_columns, axis=1)

y = data_df.pop('duration_hour')
X = data_df.drop("timestamp",axis = 1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2020)


mlflow.set_tracking_uri("http://localhost:5001")
with mlflow.start_run():
    model_RF = RandomForestRegressor(bootstrap = False, max_depth = 40, max_features = 10, min_samples_leaf = 3, min_samples_split = 36, n_estimators = 120)

    model_RF.fit(X_train, y_train)

    predictions = model_RF.predict(X_test)
    mae = metrics.mean_absolute_error(y_test, predictions)
    mse = metrics.mean_squared_error(y_test, predictions)
    rmse = np.sqrt(metrics.mean_squared_error(y_test, predictions))
    
    print('MAE:', mae)
    print('MSE:', mse)
    print('RMSE:', rmse)
    
    mlflow.log_metric("mse", mse)
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("mae", mae)
    
    pickle.dump(model_RF, open(path_saved_model, 'wb'))
    mlflow.set_tag("mlflow.runName", "model-"+time.strftime("%Y%m%d-%H:%M:%S"))
    tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
    print(tracking_url_type_store)
    if tracking_url_type_store != "file":
        mlflow.sklearn.log_model(model_RF, "model", registered_model_name="RandomForestRegressor")
    else:
        mlflow.sklearn.log_model(model_RF, "model")