import streamlit as st
import pandas as pd
import joblib
def app():
    # Load mô hình
    model = joblib.load(r'D:\MINI_Project\DoAn3\CatBoost\catboost_model.pkl')

    # Tiêu đề ứng dụng
    st.title("Dự đoán Total_Score cho Kỳ Học Tiếp Theo")

    # Nhập liệu từ người dùng
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.number_input("Age", min_value=18, max_value=24, value=20)
    department = st.selectbox("Department", ["Mathematics", "Business", "Engineering", "CS"])
    attendance = st.number_input("Attendance (%)", min_value=0.0, max_value=100.0, value=80.0)
    midterm_score = st.number_input("Midterm Score", min_value=0.0, max_value=100.0, value=50.0)
    final_score = st.number_input("Final Score", min_value=0.0, max_value=100.0, value=50.0)
    assignments_avg = st.number_input("Assignments Average", min_value=0.0, max_value=100.0, value=50.0)
    quizzes_avg = st.number_input("Quizzes Average", min_value=0.0, max_value=100.0, value=50.0)
    participation_score = st.number_input("Participation Score", min_value=0.0, max_value=100.0, value=50.0)
    projects_score = st.number_input("Projects Score", min_value=0.0, max_value=100.0, value=50.0)
    study_hours = st.number_input("Study Hours per Week", min_value=0.0, max_value=30.0, value=15.0)
    extracurricular = st.selectbox("Extracurricular Activities", ["Yes", "No"])
    internet_access = st.selectbox("Internet Access at Home", ["Yes", "No"])
    parent_education = st.selectbox("Parent Education Level", ["Master's", "High School", "Bachelor's", "PhD", "Unknown"])
    family_income = st.selectbox("Family Income Level", ["Medium", "Low", "High"])
    stress_level = st.number_input("Stress Level (1-10)", min_value=1, max_value=10, value=5)
    sleep_hours = st.number_input("Sleep Hours per Night", min_value=0.0, max_value=10.0, value=7.0)

    # Tạo DataFrame từ input
    input_data = pd.DataFrame({
        "Gender": [gender],
        "Age": [age],
        "Department": [department],
        "Attendance (%)": [attendance],
        "Midterm_Score": [midterm_score],
        "Final_Score": [final_score],
        "Assignments_Avg": [assignments_avg],
        "Quizzes_Avg": [quizzes_avg],
        "Participation_Score": [participation_score],
        "Projects_Score": [projects_score],
        "Study_Hours_per_Week": [study_hours],
        "Extracurricular_Activities": [extracurricular],
        "Internet_Access_at_Home": [internet_access],
        "Parent_Education_Level": [parent_education],
        "Family_Income_Level": [family_income],
        "Stress_Level (1-10)": [stress_level],
        "Sleep_Hours_per_Night": [sleep_hours]
    })

    # Dự đoán khi nhấn nút
    if st.button("Dự đoán Total_Score"):
        prediction = model.predict(input_data)
        st.success(f"Dự đoán Total_Score cho kỳ học tiếp theo: {prediction[0]:.2f}")
        
        # Lời khuyên cải thiện hiệu suất học tập
        st.subheader("Lời khuyên cải thiện hiệu suất học tập:")
        if sleep_hours < 7:
            st.write("- Bạn nên ngủ đủ 7-8 tiếng mỗi ngày để tăng khả năng tập trung và ghi nhớ.")
        if study_hours < 10:
            st.write("- Hãy dành ít nhất 10-12 giờ mỗi tuần cho việc tự học và ôn tập.")
        if attendance < 85:
            st.write("- Cần đi học đầy đủ hơn để không bỏ lỡ nội dung quan trọng.")
        if assignments_avg < 70:
            st.write("- Hãy cải thiện điểm bài tập bằng cách luyện thêm và nhờ sự hỗ trợ từ giảng viên.")
        if stress_level > 5:
            st.write("- Bạn nên nghỉ ngơi, tập thể dục hoặc thiền để giảm căng thẳng.")
        if extracurricular == "No":
            st.write("- Tham gia hoạt động ngoại khóa để phát triển kỹ năng mềm và mở rộng mối quan hệ.")