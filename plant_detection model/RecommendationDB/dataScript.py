import sqlite3
import pandas as pd
import os

# Ensure the correct file path
csv_file_path = r"C:\000000000000000\Demo\Model\plant_detection model\RecommendationDB\plant_disease_expert_dataset_filled.csv"

# Verify if the file exists
if not os.path.exists(csv_file_path):
    print(f"Error: File not found -> {csv_file_path}")
else:
    print("File found! Proceeding with database creation.")

    # Try reading the file with different encodings
    try:
        df = pd.read_csv(csv_file_path, encoding="utf-8")
    except UnicodeDecodeError:
        print("UTF-8 decoding failed. Trying ISO-8859-1...")
        df = pd.read_csv(csv_file_path, encoding="ISO-8859-1")

    # Define the SQLite database file name
    db_path = "plant_treatment.db"

    # Create a new SQLite database and a table
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS treatments (
        disease_name TEXT PRIMARY KEY,
        symptoms TEXT,
        causes TEXT,
        recommended_medicine TEXT,
        dosage_duration TEXT,
        preventive_measures TEXT,
        recommended_pesticides TEXT,
        pesticide_usage_measures TEXT
    )
    """)

    # Insert data from CSV into the database
    for _, row in df.iterrows():
        cursor.execute("""
        INSERT OR REPLACE INTO treatments (
            disease_name, symptoms, causes, recommended_medicine, dosage_duration, 
            preventive_measures, recommended_pesticides, pesticide_usage_measures
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, tuple(row))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    print(f"Database created successfully: {db_path}")
