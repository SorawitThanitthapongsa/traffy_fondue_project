
model = GridSearchCV(estimator=RandomForestRegressor(),param_grid=dict(criterion=['gini','entropy'],max_depth=[2,3,6],min_samples_leaf=[2,5,10],
    n_estimators=[100,200], random_state=[2020]),scoring='f1_weighted',cv=5,n_jobs=-1
) 