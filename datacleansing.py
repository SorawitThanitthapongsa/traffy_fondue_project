import pandas as pd
import pyspark
import matplotlib
from datetime import datetime, timezone
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import classification_report,confusion_matrix


path = "./bangkok_traffy.csv"
df = pd.read_csv(path)


df_type = df[df["state"] == "เสร็จสิ้น"]
bangkok = ["กรุงเทพมหานคร","จังหวัดกรุงเทพมหานคร","จังหวัดจังหวัด กรุงเทพมหานคร","จังหวัดBangkok","จังหวัดจังหวัดกรุงเทพมหานคร"]
df_type_pro = df_type[df_type["province"].isin(bangkok)]

print(df_type_pro.province.value_counts())

df_type_pro["timestamp"]=pd.to_datetime(df_type_pro["timestamp"])

print(df_type_pro["timestamp"])


df_type_pro["last_activity"] = pd.to_datetime(df_type_pro["last_activity"])
df_type_pro["duration"] = df_type_pro["last_activity"]-df_type_pro["timestamp"]

print(df_type_pro)

# df_type_pro = df_type_pro[df_type_pro["district"].isnull() == False]
# df_type_pro = df_type_pro[df_type_pro["type"].isnull() == False]
# df_type_pro = df_type_pro[df_type_pro["type"] != "{}"]

# df_type_pro_dpro = df_type_pro.drop(columns=["province","state","photo","photo_after"])
# df_type_pro_dpro['type'] = [x[1:-1] for x in df_type_pro_dpro['type']]
# df_type_pro_dpro['type']= df_type_pro_dpro['type'].str.split(",", n = 1, expand = False)
# type_df = df_type_pro_dpro[df_type_pro_dpro.type.apply(lambda x: len(x)) == 1]
# type_df.style

# df_feature = df_type_pro_dpro[['type', 'district','timestamp','duration']]


# model = GridSearchCV(estimator=RandomForestRegressor(),param_grid=dict(criterion=['gini','entropy'],max_depth=[2,3,6],min_samples_leaf=[2,5,10],
#     n_estimators=[100,200], random_state=[2020]),scoring='f1_weighted',cv=5,n_jobs=-1
# ) 

