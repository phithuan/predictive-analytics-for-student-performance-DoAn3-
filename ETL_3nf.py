import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import numpy as np

# Database connection parameters
db_params = {
    "dbname": "student_PB",
    "user": "postgres",
    "password": "123",
    "host": "localhost",
    "port": "5432"
}

# File path for the CSV
csv_file = r'D:\MINI_Project\DoAn3\Data\Students_Grading_Dataset.csv'

def extract_data(file_path):
    """
    Extract data from CSV file using pandas
    """
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
        print(f"Successfully read {len(df)} records from CSV")
        return df
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

def transform_data(df):
    """
    Transform and clean the data, including categorical standardization, Total_Score calculation, and grade consistency check
    """
    df = df.copy()
    
    # Replace empty strings with NaN
    df.replace('', np.nan, inplace=True)
    
    # Clean and convert numeric columns
    numeric_columns = ['Attendance (%)', 'Midterm_Score', 'Final_Score', 'Assignments_Avg', 
                      'Quizzes_Avg', 'Participation_Score', 'Projects_Score', 
                      'Total_Score', 'Study_Hours_per_Week', 'Sleep_Hours_per_Night']
    
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Handle boolean columns before standardization
    # Map valid values and convert invalid ones to False
    df['Extracurricular_Activities'] = df['Extracurricular_Activities'].map({'Yes': True, 'No': False}).fillna(False)
    df['Internet_Access_at_Home'] = df['Internet_Access_at_Home'].map({'Yes': True, 'No': False}).fillna(False)
    
    # Ensure Stress_Level is within 1-10
    df['Stress_Level (1-10)'] = df['Stress_Level (1-10)'].clip(1, 10)
    
    # Handle missing values
    df['Gender'] = df['Gender'].fillna('Unknown')
    df['Age'] = df['Age'].fillna(df['Age'].median())
    df['Department'] = df['Department'].fillna('Unknown')
    df['Parent_Education_Level'] = df['Parent_Education_Level'].fillna('Unknown')
    df['Family_Income_Level'] = df['Family_Income_Level'].fillna('Unknown')
    df['Grade'] = df['Grade'].fillna('F')
    
    # Standardize categorical columns (excluding boolean columns)
    categorical_columns = ['Gender', 'Family_Income_Level']
    
    # Print unique values before cleaning
    for col in categorical_columns:
        print(f"Các giá trị duy nhất trong cột {col} trước khi làm sạch: {df[col].unique()}")
    
    # Standardize Gender values
    df['Gender'] = df['Gender'].replace({'M': 'Male', 'F': 'Female'})
    
    # Define valid categories
    valid_categories = {
        'Gender': ['Male', 'Female'],
        'Family_Income_Level': ['Low', 'Medium', 'High']
    }
    
    # Replace invalid values with 'Unknown'
    for col, valid_values in valid_categories.items():
        df[col] = df[col].apply(lambda x: x if x in valid_values or pd.isna(x) else 'Unknown')
    
    # Print unique values after cleaning
    for col in categorical_columns:
        print(f"Các giá trị duy nhất trong cột {col} sau khi làm sạch: {df[col].unique()}")
    
    # Print unique values for boolean columns
    print(f"Các giá trị duy nhất trong cột Internet_Access_at_Home sau khi làm sạch: {df['Internet_Access_at_Home'].unique()}")
    print(f"Các giá trị duy nhất trong cột Extracurricular_Activities sau khi làm sạch: {df['Extracurricular_Activities'].unique()}")
    
    # Calculate Total_Score based on provided weights
    df['Total_Score'] = (
        0.15 * df['Midterm_Score'].fillna(0) +
        0.25 * df['Final_Score'].fillna(0) +
        0.15 * df['Assignments_Avg'].fillna(0) +
        0.10 * df['Quizzes_Avg'].fillna(0) +
        0.05 * df['Participation_Score'].fillna(0) * 10 +  # Scale Participation_Score (0-10) to 0-100
        0.30 * df['Projects_Score'].fillna(0)
    )
    
    # Handle NaN in Total_Score
    df['Total_Score'] = df['Total_Score'].fillna(0)
    
    # Check for inconsistencies between Total_Score and Grade
    def expected_grade(score):
        if pd.isna(score) or score < 50:
            return 'F'
        elif score >= 80:
            return 'A'
        elif score >= 70:
            return 'B'
        elif score >= 60:
            return 'C'
        else:
            return 'D'
    
    # Create a copy for grade consistency check
    total_score_grade = df[['Total_Score', 'Grade']].copy()
    total_score_grade['Expected_Grade'] = total_score_grade['Total_Score'].apply(expected_grade)
    
    # Identify inconsistent rows
    inconsistent_rows = total_score_grade[total_score_grade['Grade'] != total_score_grade['Expected_Grade']]
    print(f"Số lượng hàng không nhất quán giữa Total_Score và Grade: {len(inconsistent_rows)}")
    
    # Save inconsistent rows for review
    if len(inconsistent_rows) > 0:
        inconsistent_rows.to_csv('inconsistent_grades.csv', index=False)
        print("Hàng không nhất quán đã được lưu vào 'inconsistent_grades.csv'")
    
    # Correct inconsistent grades
    df.loc[inconsistent_rows.index, 'Grade'] = total_score_grade.loc[inconsistent_rows.index, 'Expected_Grade']
    
    # Verify no inconsistencies remain
    total_score_grade = df[['Total_Score', 'Grade']].copy()
    total_score_grade['Expected_Grade'] = total_score_grade['Total_Score'].apply(expected_grade)
    inconsistent_rows_after = total_score_grade[total_score_grade['Grade'] != total_score_grade['Expected_Grade']]
    print(f"Số lượng hàng không nhất quán sau khi sửa: {len(inconsistent_rows_after)}")
    
    return df

def load_data(df, conn_params):
    """
    Load transformed data into PostgreSQL database
    """
    try:
        # Create SQLAlchemy engine
        engine = create_engine(f"postgresql+psycopg2://{conn_params['user']}:{conn_params['password']}@{conn_params['host']}:{conn_params['port']}/{conn_params['dbname']}")
        
        # Create connection
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        
        # Insert departments and create mapping
        departments = df['Department'].unique()
        department_map = {}
        
        # Ensure 'Unknown' department exists
        cursor.execute(
            "INSERT INTO departments (department_name) VALUES (%s) ON CONFLICT (department_name) DO NOTHING RETURNING department_id",
            ('Unknown',)
        )
        result = cursor.fetchone()
        if result:
            department_map['Unknown'] = result[0]
        else:
            cursor.execute("SELECT department_id FROM departments WHERE department_name = %s", ('Unknown',))
            department_map['Unknown'] = cursor.fetchone()[0]
        
        # Insert other departments
        for dept in departments:
            if pd.notna(dept) and dept != 'Unknown':
                cursor.execute(
                    "INSERT INTO departments (department_name) VALUES (%s) ON CONFLICT (department_name) DO NOTHING RETURNING department_id",
                    (dept,)
                )
                result = cursor.fetchone()
                if result:
                    department_map[dept] = result[0]
                else:
                    cursor.execute("SELECT department_id FROM departments WHERE department_name = %s", (dept,))
                    result = cursor.fetchone()
                    if result:
                        department_map[dept] = result[0]
                    else:
                        print(f"Warning: Department '{dept}' could not be found or inserted. Assigning to 'Unknown'.")
                        department_map[dept] = department_map['Unknown']
        
        # Commit department insertions to ensure IDs are persisted
        conn.commit()
        print("Department map:", department_map)
        
        # Insert education levels
        education_levels = df['Parent_Education_Level'].unique()
        education_map = {}
        for edu in education_levels:
            if pd.notna(edu):
                cursor.execute(
                    "INSERT INTO education_levels (education_level_name) VALUES (%s) ON CONFLICT (education_level_name) DO NOTHING RETURNING education_level_id",
                    (edu,)
                )
                result = cursor.fetchone()
                if result:
                    education_map[edu] = result[0]
                else:
                    cursor.execute("SELECT education_level_id FROM education_levels WHERE education_level_name = %s", (edu,))
                    result = cursor.fetchone()
                    if result:
                        education_map[edu] = result[0]
                    else:
                        print(f"Warning: Education level '{edu}' could not be found or inserted.")
                        education_map[edu] = education_map.get('Unknown', None)
        
        # Commit education level insertions
        conn.commit()
        
        # Insert income levels
        income_levels = df['Family_Income_Level'].unique()
        income_map = {}
        for income in income_levels:
            if pd.notna(income):
                cursor.execute(
                    "INSERT INTO income_levels (income_level_name) VALUES (%s) ON CONFLICT (income_level_name) DO NOTHING RETURNING income_level_id",
                    (income,)
                )
                result = cursor.fetchone()
                if result:
                    income_map[income] = result[0]
                else:
                    cursor.execute("SELECT income_level_id FROM income_levels WHERE income_level_name = %s", (income,))
                    result = cursor.fetchone()
                    if result:
                        income_map[income] = result[0]
                    else:
                        print(f"Warning: Income level '{income}' could not be found or inserted.")
                        income_map[income] = income_map.get('Unknown', None)
        
        # Commit income level insertions
        conn.commit()
        
        # Prepare dataframes for each table
        students_df = df[['Student_ID', 'First_Name', 'Last_Name', 'Email', 'Gender', 'Age', 'Department']].copy()
        students_df['department_id'] = students_df['Department'].map(department_map)
        
        # Check for unmapped departments
        if students_df['department_id'].isna().any():
            print("Warning: Some departments could not be mapped. Assigning to 'Unknown' department.")
            students_df['department_id'] = students_df['department_id'].fillna(department_map['Unknown'])
        
        # Rename columns to match database schema
        students_df = students_df.rename(columns={
            'Student_ID': 'student_id',
            'First_Name': 'first_name',
            'Last_Name': 'last_name',
            'Email': 'email',
            'Gender': 'gender',
            'Age': 'age'
        })
        
        academic_df = df[['Student_ID', 'Attendance (%)', 'Midterm_Score', 'Final_Score', 
                        'Assignments_Avg', 'Quizzes_Avg', 'Participation_Score', 
                        'Projects_Score', 'Total_Score', 'Grade']].copy()
        academic_df.columns = ['student_id', 'attendance', 'midterm_score', 'final_score', 
                              'assignments_avg', 'quizzes_avg', 'participation_score', 
                              'projects_score', 'total_score', 'grade']
        
        external_df = df[['Student_ID', 'Study_Hours_per_Week', 'Extracurricular_Activities', 
                        'Internet_Access_at_Home', 'Parent_Education_Level', 
                        'Family_Income_Level', 'Stress_Level (1-10)', 
                        'Sleep_Hours_per_Night']].copy()
        external_df['education_level_id'] = external_df['Parent_Education_Level'].map(education_map)
        external_df['income_level_id'] = external_df['Family_Income_Level'].map(income_map)
        
        # Handle unmapped education and income levels
        if external_df['education_level_id'].isna().any():
            print("Warning: Some education levels could not be mapped. Assigning to 'Unknown'.")
            external_df['education_level_id'] = external_df['education_level_id'].fillna(education_map['Unknown'])
        if external_df['income_level_id'].isna().any():
            print("Warning: Some income levels could not be mapped. Assigning to 'Unknown'.")
            external_df['income_level_id'] = external_df['income_level_id'].fillna(income_map['Unknown'])
        
        external_df = external_df.rename(columns={
            'Student_ID': 'student_id',
            'Study_Hours_per_Week': 'study_hours_per_week',
            'Extracurricular_Activities': 'extracurricular_activities',
            'Internet_Access_at_Home': 'internet_access_at_home',
            'Stress_Level (1-10)': 'stress_level',
            'Sleep_Hours_per_Night': 'sleep_hours_per_night'
        })
        
        # Load data into tables
        print("Inserting into students table...")
        students_df[['student_id', 'first_name', 'last_name', 'email', 'gender', 'age', 'department_id']].to_sql('students', engine, if_exists='append', index=False)
        print("Inserting into academic_performance table...")
        academic_df.to_sql('academic_performance', engine, if_exists='append', index=False)
        print("Inserting into external_factors table...")
        external_df[['student_id', 'study_hours_per_week', 'extracurricular_activities', 
                   'internet_access_at_home', 'education_level_id', 'income_level_id', 
                   'stress_level', 'sleep_hours_per_night']].to_sql('external_factors', engine, if_exists='append', index=False)
        
        # Commit changes
        conn.commit()
        print("Data successfully loaded into database")
        
    except Exception as e:
        print(f"Error loading data: {e}")
        conn.rollback()
    
    finally:
        cursor.close()
        conn.close()

def main():
    # Extract
    df = extract_data(csv_file)
    if df is None:
        return
    
    # Transform
    df_transformed = transform_data(df)
    
    # Load
    load_data(df_transformed, db_params)

if __name__ == "__main__":
    main()