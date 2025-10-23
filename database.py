# database.py
import sqlite3
from sqlite3 import Error
import csv
import datetime

DATABASE_NAME = "fitness_tracker.db"

def create_connection():
    """ Create a database connection to the SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
    except Error as e:
        print(e)
    return conn

def update_workout(workout_id, sets_data):
    """ Updates the sets for an existing workout. """
    conn = create_connection()
    if conn is None: return
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM workout_sets WHERE workout_id = ?", (workout_id,))
        sets_to_insert = []
        for i, s in enumerate(sets_data):
            sets_to_insert.append((workout_id, i + 1, s['reps'], s['weight']))
        cur.executemany("INSERT INTO workout_sets (workout_id, set_number, reps, weight_kg) VALUES (?, ?, ?, ?)", sets_to_insert)
        conn.commit()
    except Error as e:
        print(f"Error updating workout: {e}")
    finally:
        conn.close()

def delete_workout(workout_id):
    """ Deletes a workout and all its associated sets from the database. """
    conn = create_connection()
    if conn is None: return
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM workouts WHERE id = ?", (workout_id,))
        conn.commit()
    except Error as e:
        print(f"Error deleting workout: {e}")
    finally:
        conn.close()

def add_workout(exercise_name, date_str, sets_data):
    """ Adds a workout log and its associated sets. """
    conn = create_connection()
    if conn is None: return

    timestamp = f"{date_str} {datetime.datetime.now().strftime('%H:%M:%S')}"
    
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO workouts (exercise_name, timestamp) VALUES (?, ?)", (exercise_name, timestamp))
        workout_id = cur.lastrowid
        sets_to_insert = []
        for i, s in enumerate(sets_data):
            sets_to_insert.append((workout_id, i + 1, s['reps'], s['weight']))
        cur.executemany("INSERT INTO workout_sets (workout_id, set_number, reps, weight_kg) VALUES (?, ?, ?, ?)", sets_to_insert)
        conn.commit()
    except Error as e:
        print(f"Error adding workout: {e}")
    finally:
        conn.close()

def get_detailed_workouts_by_date(date_str):
    """ Gets all strength workouts for a date, including their detailed sets and workout ID. """
    conn = create_connection()
    if conn is None: return []
    
    workouts_on_date = []
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, exercise_name FROM workouts WHERE DATE(timestamp) = ? ORDER BY timestamp", (date_str,))
        main_workouts = cur.fetchall()

        for workout_id, exercise_name in main_workouts:
            cur.execute("SELECT reps, weight_kg FROM workout_sets WHERE workout_id = ? ORDER BY set_number", (workout_id,))
            sets_raw = cur.fetchall()
            if not sets_raw: continue
            sets_list = [{'reps': r, 'weight': w} for r, w in sets_raw]
            workouts_on_date.append({'id': workout_id, 'name': exercise_name, 'sets': sets_list, 'type': 'strength'})
            
        return workouts_on_date
    except Error as e:
        print(f"Error getting detailed workouts: {e}")
        return []
    finally:
        conn.close()

def get_dates_with_workouts():
    conn = create_connection()
    if conn is None: return []
    try:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT DATE(timestamp) FROM workouts UNION SELECT DISTINCT DATE(timestamp) FROM cardio_sessions")
        rows = cur.fetchall()
        return [row[0] for row in rows]
    except Error as e:
        print(f"Error getting dates with workouts: {e}")
        return []
    finally:
        conn.close()

def populate_exercises_if_empty():
    conn = create_connection()
    if conn is None: return
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM exercises")
        if cur.fetchone()[0] == 0:
            exercises = [
                ('Barbell Bench Press', 'Chest'), ('Dumbbell Bench Press', 'Chest'),
                ('Incline Barbell Press', 'Chest'), ('Incline Dumbbell Press', 'Chest'),
                ('Decline Bench Press', 'Chest'), ('Push Up', 'Chest'),
                ('Dips', 'Chest'), ('Chest Fly', 'Chest'),
                ('Cable Crossover', 'Chest'), ('Pec Deck Machine', 'Chest'),
                ('Barbell Squat', 'Legs'), ('Goblet Squat', 'Legs'),
                ('Leg Press', 'Legs'), ('Leg Curl', 'Legs'),
                ('Leg Extension', 'Legs'), ('Walking Lunges', 'Legs'),
                ('Bulgarian Split Squat', 'Legs'), ('Calf Raise', 'Legs'),
                ('Romanian Deadlift', 'Legs'), ('Hack Squat', 'Legs'),
                ('Deadlift', 'Back'), ('Barbell Row', 'Back'),
                ('Pull Up', 'Back'), ('Chin Up', 'Back'),
                ('Lat Pulldown', 'Back'), ('Seated Cable Row', 'Back'),
                ('T-Bar Row', 'Back'), ('Dumbbell Row', 'Back'),
                ('Bent Over Row', 'Back'), ('Good Mornings', 'Back'),
                ('Overhead Press (Barbell)', 'Shoulders'), ('Seated Dumbbell Press', 'Shoulders'),
                ('Arnold Press', 'Shoulders'), ('Lateral Raise', 'Shoulders'),
                ('Front Raise', 'Shoulders'), ('Reverse Pec Deck', 'Shoulders'),
                ('Face Pulls', 'Shoulders'), ('Upright Row', 'Shoulders'),
                ('Barbell Bicep Curl', 'Arms'), ('Dumbbell Bicep Curl', 'Arms'),
                ('Hammer Curl', 'Arms'), ('Preacher Curl', 'Arms'),
                ('Tricep Pushdown', 'Arms'), ('Skull Crushers', 'Arms'),
                ('Close Grip Bench Press', 'Arms'), ('Overhead Tricep Extension', 'Arms'),
                ('Crunches', 'Core'), ('Leg Raises', 'Core'),
                ('Plank', 'Core'), ('Russian Twist', 'Core'),
                ('Cable Crunches', 'Core'), ('Ab Roller', 'Core'),
                ('Running', 'Cardio'), ('Cycling', 'Cardio'),
                ('Swimming', 'Cardio'), ('Rowing', 'Cardio'),
                ('Stair Master', 'Cardio'), ('Elliptical', 'Cardio'),
                ('Walking (Incline)', 'Cardio')
            ]
            cur.executemany("INSERT INTO exercises (name, muscle_group) VALUES (?, ?)", exercises)
            conn.commit()
    finally:
        conn.close()

def get_all_muscle_groups():
    conn = create_connection()
    if conn is None: return []
    try:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT muscle_group FROM exercises ORDER BY muscle_group")
        rows = cur.fetchall()
        return [row[0] for row in rows]
    finally:
        conn.close()

def get_exercises_by_group(muscle_group):
    conn = create_connection()
    if conn is None: return []
    try:
        cur = conn.cursor()
        cur.execute("SELECT name FROM exercises WHERE muscle_group = ? ORDER BY name", (muscle_group,))
        rows = cur.fetchall()
        return [row[0] for row in rows]
    finally:
        conn.close()

def get_body_weight_history():
    conn = create_connection()
    if conn is None: return []
    try:
        cur = conn.cursor()
        cur.execute("SELECT strftime('%s', timestamp), weight_kg FROM body_measurements WHERE weight_kg IS NOT NULL ORDER BY timestamp ASC")
        rows = cur.fetchall()
        return [(float(ts), weight) for ts, weight in rows]
    finally:
        conn.close()
        
def add_cardio_session(name, date_str, duration, distance, calories, incline):
    conn = create_connection()
    if conn is None: return
    timestamp = f"{date_str} {datetime.datetime.now().strftime('%H:%M:%S')}"
    sql = ''' INSERT INTO cardio_sessions(type, timestamp, duration_min, distance_km, calories_burned, incline) VALUES(?,?,?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (name, timestamp, duration, distance, calories, incline))
        conn.commit()
    finally:
        conn.close()

def add_body_measurement(weight_kg, body_fat_pct=None, chest_cm=None, waist_cm=None, arms_cm=None):
    conn = create_connection()
    if conn is None: return
    sql = ''' INSERT INTO body_measurements(weight_kg, body_fat_pct, chest_cm, waist_cm, arms_cm)
              VALUES(?,?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (weight_kg, body_fat_pct, chest_cm, waist_cm, arms_cm))
        conn.commit()
    finally:
        conn.close()

def get_cardio_by_date(date_str):
    conn = create_connection()
    if conn is None: return []
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, type, duration_min, distance_km, calories_burned, incline FROM cardio_sessions WHERE DATE(timestamp) = ? ORDER BY timestamp", (date_str,))
        rows = cur.fetchall()
        return [{'id': r[0], 'name': r[1], 'duration': r[2], 'distance': r[3], 'calories': r[4], 'incline': r[5], 'type': 'cardio'} for r in rows]
    finally:
        conn.close()

def get_all_measurements():
    conn = create_connection()
    if conn is None: return []
    try:
        cur = conn.cursor()
        cur.execute("SELECT timestamp, weight_kg, body_fat_pct, chest_cm, waist_cm, arms_cm FROM body_measurements ORDER BY timestamp DESC")
        return cur.fetchall()
    finally:
        conn.close()

def delete_cardio_log(log_id):
    conn = create_connection()
    if conn is None: return
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM cardio_sessions WHERE id = ?", (log_id,))
        conn.commit()
    finally:
        conn.close()

def update_cardio_log(log_id, duration, distance, calories, incline):
    conn = create_connection()
    if conn is None: return
    try:
        cur = conn.cursor()
        cur.execute("UPDATE cardio_sessions SET duration_min = ?, distance_km = ?, calories_burned = ?, incline = ? WHERE id = ?", (duration, distance, calories, incline, log_id))
        conn.commit()
    finally:
        conn.close()

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def setup_database():
    """ Sets up the database and all necessary tables """
    sql_create_exercises_table = """
    CREATE TABLE IF NOT EXISTS exercises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        muscle_group TEXT NOT NULL,
        demo_url TEXT 
    );"""
    sql_create_measurements_table = """
    CREATE TABLE IF NOT EXISTS body_measurements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        weight_kg REAL,
        body_fat_pct REAL,
        chest_cm REAL,
        waist_cm REAL,
        arms_cm REAL
    );"""
    sql_create_workouts_table = """
    CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME,
        exercise_name TEXT NOT NULL
    );"""
    sql_create_workout_sets_table = """
    CREATE TABLE IF NOT EXISTS workout_sets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        workout_id INTEGER NOT NULL,
        set_number INTEGER NOT NULL,
        reps INTEGER,
        weight_kg REAL,
        FOREIGN KEY (workout_id) REFERENCES workouts (id) ON DELETE CASCADE
    );"""
    sql_create_cardio_table = """
    CREATE TABLE IF NOT EXISTS cardio_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME,
        type TEXT NOT NULL,
        duration_min INTEGER,
        distance_km REAL,
        calories_burned INTEGER,
        incline INTEGER
    );"""

    conn = create_connection()
    if conn is not None:
        conn.execute("PRAGMA foreign_keys = ON")
        create_table(conn, sql_create_exercises_table)
        create_table(conn, sql_create_workouts_table)
        create_table(conn, sql_create_workout_sets_table)
        create_table(conn, sql_create_cardio_table)
        create_table(conn, sql_create_measurements_table)
        conn.close()
    
    populate_exercises_if_empty()

if __name__ == '__main__':
    setup_database()
