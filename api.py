import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import pandas as pd
import pickle
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import mlflow

mlflow.set_tracking_uri("http://localhost:5001")

logged_model = 'runs:/84796d3763414a3da8039c556f22c549/model'
loaded_model = mlflow.pyfunc.load_model(logged_model)

app = FastAPI()
class Data(BaseModel):
    type: str
    district: str
    
@app.get("/estimateduration")
async def read_item(data: Data):
    
    return predict(data.type,data.district)

if __name__ == "__main__":
    uvicorn.run('api:app', host='0.0.0.0', port=8000, reload=True)


def predict(int_type,int_distric):
    feature_list = ["type_[\'PM2.5\']", "type_[\'การเดินทาง\']","type_[\'กีดขวาง\']", 'type_[\'คนจรจัด\']', 'type_[\'คลอง\']','type_[\'ความปลอดภัย\']', 'type_[\'ความสะอาด\']', 'type_[\'จราจร\']','type_[\'ต้นไม้\']', 'type_[\'ถนน\']', 'type_[\'ทางเท้า\']','type_[\'ท่อระบายน้ำ\']', 'type_[\'น้ำท่วม\']', 'type_[\'ป้าย\']','type_[\'ป้ายจราจร\']', 'type_[\'ร้องเรียน\']', 'type_[\'สอบถาม\']','type_[\'สะพาน\']', 'type_[\'สัตว์จรจัด\']', 'type_[\'สายไฟ\']','type_[\'ห้องน้ำ\']', 'type_[\'เสนอแนะ\']', 'type_[\'เสียงรบกวน\']','type_[\'แสงสว่าง\']', 'district_คลองสาน', 'district_คลองสามวา','district_คลองเตย', 'district_คันนายาว', 'district_จตุจักร','district_จอมทอง', 'district_ดอนเมือง', 'district_ดินแดง','district_ดุสิต', 'district_ตลิ่งชัน', 'district_ทวีวัฒนา','district_ทุ่งครุ', 'district_ธนบุรี', 'district_บางกอกน้อย','district_บางกอกใหญ่', 'district_บางกะปิ', 'district_บางขุนเทียน','district_บางคอแหลม', 'district_บางซื่อ', 'district_บางนา','district_บางบอน', 'district_บางพลัด', 'district_บางรัก','district_บางเขน', 'district_บางแค', 'district_บึงกุ่ม','district_ปทุมวัน', 'district_ประเวศ', 'district_ป้อมปราบศัตรูพ่าย','district_พญาไท', 'district_พระนคร', 'district_พระโขนง','district_ภาษีเจริญ', 'district_มีนบุรี', 'district_ยานนาวา','district_ราชเทวี', 'district_ราษฎร์บูรณะ', 'district_ลาดกระบัง','district_ลาดพร้าว', 'district_วังทองหลาง', 'district_วัฒนา','district_สวนหลวง', 'district_สะพานสูง', 'district_สัมพันธวงศ์','district_สาทร', 'district_สายไหม', 'district_หนองจอก','district_หนองแขม', 'district_หลักสี่', 'district_ห้วยขวาง']
    int_type="type_['" + int_type + "']"
    int_distric = "district_"+int_distric

    if int_distric not in feature_list:
        return "District not exist, please try again"
    if int_type not in feature_list:
        return "Type not exist, please try again"
    
    predict_data = pd.DataFrame(0, index=np.arange(1), columns=feature_list)
    predict_data[int_distric] = 1
    predict_data[int_type] = 1
    
    prediction = loaded_model.predict(predict_data)
    prediction/=24

    return str(prediction[0])+" days"
