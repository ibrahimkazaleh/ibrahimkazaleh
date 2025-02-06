from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import sqlite3
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

# تعريف التطبيق
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تعريف قاعدة البيانات وإنشائها
DB_PATH = "sensor_data.db"
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

# إنشاء جدول البيانات إذا لم يكن موجودًا
cursor.execute("""
    CREATE TABLE IF NOT EXISTS sensor_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        acc_x REAL,
        acc_y REAL,
        acc_z REAL,
        gyr_x REAL,
        gyr_y REAL,
        gyr_z REAL,
        time TEXT,
        timegyr TEXT
    )
""")

# إنشاء جدول لتخزين التنبؤات
cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time TEXT,
        timegyr TEXT,
        predicted_workout TEXT,
        acc_x REAL,
        acc_y REAL,
        acc_z REAL,
        gyr_x REAL,
        gyr_y REAL,
        gyr_z REAL
    )
""")
conn.commit()

# تعريف نموذج البيانات
class SensorData(BaseModel):
    acc_x: float
    acc_y: float
    acc_z: float
    gyr_x: float
    gyr_y: float
    gyr_z: float
    time: str
    timegyr: str

# تحميل النموذج عند بدء تشغيل التطبيق
model_path = "../../../data-science-template-main/models/NN_workout_prediction_model(0).pkl"
try:
    model = joblib.load(model_path)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Failed to load the model: {e}")
    raise

# نقطة النهاية لتلقي البيانات وتحليلها
@app.post("/predict")
async def receive_data(data: SensorData) -> Dict[str, str]:
    try:
        # إضافة البيانات الجديدة إلى جدول البيانات
        insert_query = """
        INSERT INTO sensor_data (acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z, time, timegyr)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(insert_query, (data.acc_x, data.acc_y, data.acc_z, data.gyr_x, data.gyr_y, data.gyr_z, data.time, data.timegyr))
        conn.commit()

        # تحويل البيانات إلى صيغة مصفوفة لتناسب النموذج
        input_features = np.array([[data.acc_x, data.acc_y, data.acc_z, data.gyr_x, data.gyr_y, data.gyr_z]])

        # استخدام النموذج للتنبؤ بالحركة
        prediction = model.predict(input_features)
        predicted_workout = str(prediction[0])

        # تخزين النتيجة في جدول التنبؤات
        insert_prediction_query = """
        INSERT INTO predictions (time, timegyr, predicted_workout, acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(insert_prediction_query, (data.time, data.timegyr, predicted_workout, data.acc_x, data.acc_y, data.acc_z, data.gyr_x, data.gyr_y, data.gyr_z))
        conn.commit()

        # إرسال الاستجابة
        return {
            "message": "Data processed successfully!",
            "exercise_name": predicted_workout
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing data: {e}")

# تشغيل التطبيق الرئيسي
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
