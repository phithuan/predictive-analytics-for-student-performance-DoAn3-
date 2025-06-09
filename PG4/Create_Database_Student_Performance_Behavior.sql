-- Tạo database nếu chưa có
--CREATE DATABASE Student_Performance_Behavior;
--\c Student_Performance_Behavior;

-- Bảng chính: chứa toàn bộ thông tin sinh viên
CREATE TABLE students (
    student_id VARCHAR(10) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender VARCHAR(10),
    age INT,
    email VARCHAR(100) UNIQUE NOT NULL,
    department VARCHAR(100)
);

-- Bảng Yếu tố học tập: thông tin về các yếu tố học tập của sinh viên
CREATE TABLE academic_performance (
    student_id VARCHAR(10) PRIMARY KEY,
    attendance FLOAT,
    midterm_score FLOAT,
    final_score FLOAT,
    assignments_avg FLOAT,
    quizzes_avg FLOAT,
    participation_score FLOAT,
    projects_score FLOAT,
    total_score FLOAT,
    grade CHAR(1),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

-- Bảng Yếu tố bên ngoài: thông tin về các yếu tố ảnh hưởng đến sinh viên
CREATE TABLE external_factors (
    student_id VARCHAR(10) PRIMARY KEY,
    study_hours_per_week FLOAT,
    extracurricular_activities BOOLEAN,
    internet_access_at_home BOOLEAN,
    parent_education_level VARCHAR(100),
    family_income_level VARCHAR(50),
    stress_level INT CHECK (stress_level BETWEEN 1 AND 10),
    sleep_hours_per_night FLOAT,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);
