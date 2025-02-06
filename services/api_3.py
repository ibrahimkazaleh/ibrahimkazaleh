from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import joblib  # تحميل النموذج
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "sensor_data.db"
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
exercise_names="rest"
cursor = conn.cursor()
value=False
# ✅ تعديل قاعدة البيانات لإضافة عمود exercise_name
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
        person TEXT,
        set_id INTEGER,
        exercise_name TEXT  -- ✅ إضافة عمود التمرين
    )
""")
conn.commit()

# ✅ تحميل نموذج الذكاء الاصطناعي
model_path = "NN_workout_prediction_model.pkl"  # تأكد من المسار الصحيح للنموذج
if value:
    try:
        model = joblib.load(model_path)
        print("✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Failed to load the model: {e}")
        raise

# ✅ نموذج البيانات المستقبلة
class SensorData(BaseModel):
    acc_x: float
    acc_y: float
    acc_z: float
    gyr_x: float
    gyr_y: float
    gyr_z: float
    flag: int  # 1 لبدء التنبؤ، 0 لإيقافه
    time: str
    person: str
    set_id: int

@app.post("/predict")
async def receive_data(data: SensorData):
    if value:
        
        input_features = np.array([[data.acc_x, data.acc_y, data.acc_z, data.gyr_x, data.gyr_y, data.gyr_z]])
        

        prediction = model.predict(input_features)
        exercise_name = str(prediction[0]) 

    cursor.execute(
        """
        INSERT INTO sensor_data (acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z, time, person, set_id, exercise_name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (data.acc_x, data.acc_y, data.acc_z, data.gyr_x, data.gyr_y, data.gyr_z, data.time, data.person, data.set_id, "ohp")
    )
    conn.commit()
        
        # ✅ إرجاع التمرين المتوقع
    return {
        "message": "Data received successfully!",
        "exercise_name": exercise_names  # اسم التمرين من النموذج
    }
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


