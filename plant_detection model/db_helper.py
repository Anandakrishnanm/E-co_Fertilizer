import sqlite3

# Define database path
DB_PATH = "plant_treatment.db"

def get_treatment_recommendation(disease_name):
    """Fetch treatment recommendation for a given disease from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Query to fetch treatment details
    cursor.execute("""
        SELECT symptoms, causes, recommended_medicine, dosage_duration, 
               preventive_measures, recommended_pesticides, pesticide_usage_measures
        FROM treatments
        WHERE disease_name = ?
    """, (disease_name,))

    result = cursor.fetchone()
    conn.close()

    if result:
        return {
            "Symptoms": result[0],
            "Causes": result[1],
            "Recommended Medicine": result[2],
            "Dosage & Duration": result[3],
            "Preventive Measures": result[4],
            "Recommended Pesticides": result[5],
            "Pesticide Usage Measures": result[6]
        }
    else:
        return {"Error": "No data found for the specified disease."}
