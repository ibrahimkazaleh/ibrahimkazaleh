from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import pandas as pd
import sqlite3  # لإدارة قاعدة البيانات
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
import algorathem

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
        processed BOOLEAN DEFAULT 0
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

# تحميل النموذج عند بدء تشغيل التطبيق
model_path = "../../../models/NN_workout_prediction_model(0).pkl"
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
        # إضافة البيانات الجديدة إلى قاعدة البيانات
        insert_query = f"""
        INSERT INTO sensor_data (acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z, time, processed)
        VALUES ({data.acc_x}, {data.acc_y}, {data.acc_z}, {data.gyr_x}, {data.gyr_y}, {data.gyr_z}, '{data.time}', 0)
        """
        cursor.execute(insert_query)
        conn.commit()

        # استرجاع البيانات غير المعالجة من قاعدة البيانات
        select_query = "SELECT acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z, time FROM sensor_data WHERE processed = 0"
        cursor.execute(select_query)
        db_data = cursor.fetchall()

        # تحويل البيانات المسترجعة إلى DataFrame
        columns = ["acc_x", "acc_y", "acc_z", "gyr_x", "gyr_y", "gyr_z", "time"]
        db_df = pd.DataFrame(db_data, columns=columns)

        # التحقق من طول البيانات
        if len(db_df) < 18:
            return {"message": "Data stored. Waiting for more data."}

        # معالجة البيانات إذا كان طولها أكبر من 18
        processed_data = db_df.head(18)  # أخذ أول 18 صفًا
        try:
            transformed_data = algorathem.build_features(processed_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error in data transformation: {e}")

        # تحويل البيانات إلى مصفوفة إذا لزم الأمر
        input_features = np.array(transformed_data).reshape(1, -1)

        # استخدام النموذج للتنبؤ
        prediction = model.predict(input_features)
        predicted_workout = prediction[0]

        # تحديث البيانات كمعالجة في قاعدة البيانات
        update_query = "UPDATE sensor_data SET processed = 1 WHERE processed = 0"
        cursor.execute(update_query)
        conn.commit()

        # إرسال الاستجابة
        return {"exercise_name": predicted_workout}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing data: {e}")
