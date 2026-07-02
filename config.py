# config.py
import os

DATABASE_NAME = "mwalimu.db"

# Helper loader function to safely import and enforce dictionary types
def load_grade_data(module_path, variable_name):
    try:
        mod = __import__(module_path, fromlist=[variable_name])
        data = getattr(mod, variable_name)
        # If it accidentally became a tuple due to a trailing comma, unpack it
        if isinstance(data, tuple) and len(data) > 0:
            data = data[0]
        return data if isinstance(data, dict) else {}
    except Exception as e:
        # This will print the exact reason a grade file fails to load in your terminal
        print(f"❌ Error loading {module_path}: {e}")
        return {}

# --- CBC MODULAR CURRICULUM ASSEMBLER ---
GRADE_1 = load_grade_data("curriculum.grade1", "GRADE_1")
GRADE_2 = load_grade_data("curriculum.grade2", "GRADE_2")
GRADE_3 = load_grade_data("curriculum.grade3", "GRADE_3")
GRADE_4 = load_grade_data("curriculum.grade4", "GRADE_4")
GRADE_5 = load_grade_data("curriculum.grade5", "GRADE_5")
GRADE_6 = load_grade_data("curriculum.grade6", "GRADE_6")
GRADE_7 = load_grade_data("curriculum.grade7", "GRADE_7")
GRADE_8 = load_grade_data("curriculum.grade8", "GRADE_8")
GRADE_9 = load_grade_data("curriculum.grade9", "GRADE_9")
GRADE_10 = load_grade_data("curriculum.grade10", "GRADE_10")
GRADE_11 = load_grade_data("curriculum.grade11", "GRADE_11")
GRADE_12 = load_grade_data("curriculum.grade12", "GRADE_12")

# Master CBC Registry Map used across the App application layer
CBC = {
    "Grade 1": GRADE_1,
    "Grade 2": GRADE_2,
    "Grade 3": GRADE_3,
    "Grade 4": GRADE_4,
    "Grade 5": GRADE_5,
    "Grade 6": GRADE_6,
    "Grade 7": GRADE_7,
    "Grade 8": GRADE_8,
    "Grade 9": GRADE_9,   # Changed from Form 1
    "Grade 10": GRADE_10, # Changed from Form 2
    "Grade 11": GRADE_11, # Changed from Form 3
    "Grade 12": GRADE_12, # Changed from Form 4
}
