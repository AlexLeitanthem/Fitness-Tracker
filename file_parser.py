# file_parser.py
import re
import os
import database as db

def parse_log_file(file_path):
    """
    Reads a text file, parses its content, and adds the data to the database.
    Deletes the file after successful processing.
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read().strip()
        
        print(f"Processing file: {file_path} with content: '{content}'")

        # --- Rule 1: Workout ---
        # Example: "Workout: Bench Press, 3 sets, 10 reps, 70kg"
        workout_match = re.search(r"Workout: (.*), (\d+)\s*sets, (\d+)\s*reps, ([\d.]+)\s*kg", content, re.IGNORECASE)
        if workout_match:
            exercise, sets, reps, weight = workout_match.groups()
            db.add_workout(exercise.strip(), int(sets), int(reps), float(weight))
            print("Successfully parsed and added a workout.")
            os.remove(file_path)
            return True

        # --- Rule 2: Body Weight ---
        # Example: "Weight: 74.5kg"
        weight_match = re.search(r"Weight: ([\d.]+)\s*kg", content, re.IGNORECASE)
        if weight_match:
            weight = weight_match.groups()[0]
            db.add_body_measurement(weight_kg=float(weight))
            print("Successfully parsed and added body weight.")
            os.remove(file_path)
            return True

        # --- Rule 3: Cardio ---
        # Example: "Cardio: Running, 30 min, 5 km, 300 kcal"
        cardio_match = re.search(r"Cardio: (.*), ([\d.]+)\s*min, ([\d.]+)\s*km, ([\d.]+)\s*kcal", content, re.IGNORECASE)
        if cardio_match:
            ctype, duration, distance, calories = cardio_match.groups()
            db.add_cardio_session(ctype.strip(), int(duration), float(distance), int(calories))
            print("Successfully parsed and added a cardio session.")
            os.remove(file_path)
            return True

        print(f"No matching rule found for content: '{content}'")
        return False

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return False

