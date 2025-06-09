import pandas as pd
import psycopg2
from psycopg2 import sql
from typing import Literal

# Database connection parameters
db_params = {
    "dbname": "student_performance_behavior",
    "user": "postgres",
    "password": "123",
    "host": "localhost",
    "port": "5432"
}

# Path to the dataset
data_path = r"D:\MINI_Project\DoAn3\Data\Students_Grading_Dataset.csv"

# Function to convert score (0–100) to letter grade (A, B, C, D, F)
def score_to_grade(score: float) -> Literal['A', 'B', 'C', 'D', 'F']:
    grade_mapping = {
        (85, 101): 'A',  # 85 to <101 → A
        (70, 85): 'B',   # 70 to <85  → B
        (55, 70): 'C',   # 55 to <70  → C
        (40, 55): 'D',   # 40 to <55  → D
        (0, 40): 'F'     # 0  to <40  → F
    }
    for (lower, upper), grade in grade_mapping.items():
        if lower <= score < upper:
            return grade
    raise ValueError(f"Invalid score ({score})")

# Step 1: Extract - Load the CSV file
try:
    df = pd.read_csv(data_path)
    print("Data extracted successfully from CSV!")
except Exception as e:
    print(f"Error reading CSV: {e}")
    exit()

# Step 2: Transform
# Handle missing data
df['Parent_Education_Level'] = df['Parent_Education_Level'].fillna('Unknown')

# Calculate Total_Score with weights
df['Total_Score'] = (
    0.15 * df['Midterm_Score'].fillna(0) +
    0.25 * df['Final_Score'].fillna(0) +
    0.15 * df['Assignments_Avg'].fillna(0) +
    0.10 * df['Quizzes_Avg'].fillna(0) +
    0.05 * df['Participation_Score'].fillna(0) * 10 +  # Scale Participation_Score (0-10) to 0-100
    0.30 * df['Projects_Score'].fillna(0)
).clip(0, 100)  # Ensure values are between 0 and 100

# Apply grading
df['Grade'] = df['Total_Score'].apply(score_to_grade)

# Add dummy columns for missing fields (to match database schema)
df['first_name'] = 'Unknown'  # Placeholder: no first_name in CSV
df['last_name'] = 'Unknown'   # Placeholder: no last_name in CSV
df['email'] = df['Student_ID'].apply(lambda x: f"{x}@example.com")  # Generate dummy email
df['department'] = 'Unknown'  # Placeholder: no department in CSV
df['extracurricular_activities'] = False  # Placeholder: no data, assume False
df['internet_access_at_home'] = True  # Placeholder: no data, assume True
df['family_income_level'] = 'Unknown'  # Placeholder: no data
df['stress_level'] = 5  # Placeholder: no data, assume moderate (5)
df['sleep_hours_per_night'] = 7.0  # Placeholder: no data, assume 7 hours
print("Data transformed successfully!")

# Step 3: Load - Connect to PostgreSQL and load data
try:
    # Establish connection
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # Insert data into students table
    for _, row in df.iterrows():
        insert_students = sql.SQL("""
            INSERT INTO students (student_id, first_name, last_name, gender, age, email, department)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (student_id) DO NOTHING
        """)
        cursor.execute(insert_students, (
            row['Student_ID'], row['first_name'], row['last_name'], row['Gender'],
            row['Age'], row['email'], row['department']
        ))

    # Insert data into academic_performance table
    for _, row in df.iterrows():
        insert_academic = sql.SQL("""
            INSERT INTO academic_performance (
                student_id, attendance, midterm_score, final_score, assignments_avg,
                quizzes_avg, participation_score, projects_score, total_score, grade
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (student_id) DO NOTHING
        """)
        cursor.execute(insert_academic, (
            row['Student_ID'], row['Attendance (%)'], row['Midterm_Score'],
            row['Final_Score'], row['Assignments_Avg'], row['Quizzes_Avg'],
            row['Participation_Score'], row['Projects_Score'], row['Total_Score'],
            row['Grade']
        ))

    # Insert data into external_factors table
    for _, row in df.iterrows():
        insert_external = sql.SQL("""
            INSERT INTO external_factors (
                student_id, study_hours_per_week, extracurricular_activities,
                internet_access_at_home, parent_education_level, family_income_level,
                stress_level, sleep_hours_per_night
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (student_id) DO NOTHING
        """)
        cursor.execute(insert_external, (
            row['Student_ID'], row['Study_Hours_per_Week'], row['extracurricular_activities'],
            row['internet_access_at_home'], row['Parent_Education_Level'],
            row['family_income_level'], row['stress_level'], row['sleep_hours_per_night']
        ))

    conn.commit()
    print("Data successfully loaded into Student_Performance_Behavior database!")

except Exception as e:
    print(f"Error: {e}")
    conn.rollback()

finally:
    cursor.close()
    conn.close()