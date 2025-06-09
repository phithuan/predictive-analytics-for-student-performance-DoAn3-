-- Kết nối đến cơ sở dữ liệu DoAn3_SV
--CREATE DATABASE Students_PBe

--\c Students_Performance_Behavior
-- Bảng departments: Lưu thông tin khoa
CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(50) UNIQUE NOT NULL
);

-- Bảng education_levels: Lưu các mức giáo dục của phụ huynh
CREATE TABLE education_levels (
    education_level_id SERIAL PRIMARY KEY,
    education_level_name VARCHAR(50) UNIQUE NOT NULL
);

-- Bảng income_levels: Lưu các mức thu nhập gia đình
CREATE TABLE income_levels (
    income_level_id SERIAL PRIMARY KEY,
    income_level_name VARCHAR(20) UNIQUE NOT NULL
);

-- Bảng students: Lưu thông tin cá nhân sinh viên
CREATE TABLE students (
    student_id VARCHAR(10) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    gender VARCHAR(10),
    age INT,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);




-- Bảng academic_performance: Lưu dữ liệu học tập
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

-- Bảng external_factors: Lưu các yếu tố ảnh hưởng đến học tập
CREATE TABLE external_factors (
    student_id VARCHAR(10) PRIMARY KEY,
    study_hours_per_week FLOAT,
    extracurricular_activities BOOLEAN,
    internet_access_at_home BOOLEAN,
    education_level_id INT,
    income_level_id INT,
    stress_level INT CHECK (stress_level BETWEEN 1 AND 10),
    sleep_hours_per_night FLOAT,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (education_level_id) REFERENCES education_levels(education_level_id),
    FOREIGN KEY (income_level_id) REFERENCES income_levels(income_level_id)
);

ALTER TABLE departments
ALTER COLUMN department_id TYPE BIGINT;

ALTER TABLE students
ALTER COLUMN department_id TYPE BIGINT;

ALTER TABLE students
ALTER COLUMN age TYPE BIGINT;

