import pickle
import sqlite3
import time
from fastapi import FastAPI, HTTPException
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

db_name = "exercise_data.db"
pkl_file = "data.pkl"
model_file = "model.pkl"
BUFFER_SIZE = 20  # عدد القيم المطلوبة قبل التنبؤ

def init_db():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            acc_x REAL,
            acc_y REAL,
            acc_z REAL,
            gyr_x REAL,
            gyr_y REAL,
            gyr_z REAL,
            epic TEXT,
            exercise_name TEXT
        )
    ''')
    conn.commit()
    conn.close()

def load_pkl(file_path):
    with open(file_path, "rb") as f:
        return pickle.load(f)

def save_to_db(player_id, data, exercise_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    for entry in data:
        cursor.execute('''
            INSERT INTO exercises (player_id, acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z, epic, exercise_name)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (player_id, entry["acc_x"], entry["acc_y"], entry["acc_z"], entry["gyr_x"], entry["gyr_y"], entry["gyr_z"], entry["epic"], exercise_name))
    conn.commit()
    conn.close()

def predict_exercise(data):
    model = load_pkl(model_file)
    input_data = np.array([[d["acc_x"], d["acc_y"], d["acc_z"], d["gyr_x"], d["gyr_y"], d["gyr_z"]] for d in data])
    prediction = model.predict([input_data.flatten()])
    return prediction[0]

@app.post("/process/{player_id}")
def process_data(player_id: int, signal: int):
    if signal != 1:
        raise HTTPException(status_code=400, detail="Signal must be 1 to start processing")
    
    data = load_pkl(pkl_file)
    if len(data) < BUFFER_SIZE:
        raise HTTPException(status_code=400, detail="Not enough data to process")
    
    selected_data = data[:BUFFER_SIZE]  # أخذ أول 20 عينة
    exercise_name = predict_exercise(selected_data)
    save_to_db(player_id, selected_data, exercise_name)
    
    return {"exercise_name": exercise_name}

init_db()
