from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import sqlite3
import joblib
import numpy as np
from datetime import datetime, timedelta
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
cursor = conn.cursor()

# إنشاء جدول البيانات
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
        set_id INTEGER
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time TEXT,
        predicted_workout TEXT,
        acc_x REAL,
        acc_y REAL,
        acc_z REAL,
        gyr_x REAL,
        gyr_y REAL,
        gyr_z REAL,
        set_id INTEGER
    )
""")
conn.commit()

class SensorData(BaseModel):
    acc_x: float
    acc_y: float
    acc_z: float
    gyr_x: float
    gyr_y: float
    gyr_z: float
    time: str

model_path = "../../../data-science-template-main/models/NN_workout_prediction_model(0).pkl"
try:
    model = joblib.load(model_path)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Failed to load the model: {e}")
    raise

def get_last_time():
    cursor.execute("SELECT time, set_id FROM sensor_data ORDER BY id DESC LIMIT 1")
    last_entry = cursor.fetchone()
    if last_entry:
        return datetime.fromisoformat(last_entry[0]), last_entry[1]
    return None, None

buffered_data = []  # قائمة لتخزين البيانات قبل التنبؤ

@app.post("/predict")
async def receive_data(data: SensorData) -> Dict[str, str]:
    print(data)
    try:
        new_time = datetime.fromisoformat(data.time)
        last_time, last_set_id = get_last_time()

        if last_time and (new_time - last_time) < timedelta(minutes=1):
            set_id = last_set_id
        else:
            set_id = (last_set_id + 1) if last_set_id is not None else 1

        insert_query = """
        INSERT INTO sensor_data (acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z, time, set_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(insert_query, (data.acc_x, data.acc_y, data.acc_z, data.gyr_x, data.gyr_y, data.gyr_z, data.time, set_id))
        conn.commit()

        # تخزين البيانات في القائمة المؤقتة
        buffered_data.append([data.acc_x, data.acc_y, data.acc_z, data.gyr_x, data.gyr_y, data.gyr_z])

        if len(buffered_data) < 3:
            return {"message": "Data received, waiting for more readings..."}

        # تحويل البيانات وإجراء التنبؤ
        input_features = np.array(buffered_data)
        prediction = model.predict(input_features)
        predicted_workout = str(prediction[-1])  # أخذ آخر تنبؤ

        insert_prediction_query = """
        INSERT INTO predictions (time, predicted_workout, acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z, set_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(insert_prediction_query, (data.time, predicted_workout, data.acc_x, data.acc_y, data.acc_z, data.gyr_x, data.gyr_y, data.gyr_z, set_id))
        conn.commit()

        # تفريغ القائمة بعد التنبؤ
        buffered_data.clear()

        return {
            "message": "Exercise detected!",
            "exercise_name": predicted_workout,
            "set_id": str(set_id)
        }

        print(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing data: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
