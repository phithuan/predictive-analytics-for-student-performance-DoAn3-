import streamlit as st
import pandas as pd
import joblib

def app():
    # =========================
    # 2. Load model
    # =========================
    @st.cache_resource
    def load_model():
        model = joblib.load(r"D:\MINI_Project\DoAn3\perdict_train_XGBoost\catboost_model_final.pkl")
        cat_features = joblib.load(r"D:\MINI_Project\DoAn3\perdict_train_XGBoost\cat_features_final.pkl")
        label_map = joblib.load(r"D:\MINI_Project\DoAn3\perdict_train_XGBoost\label_map_final.pkl")
        return model, cat_features, label_map

    model, cat_features, label_map = load_model()
    inv_label_map = {v: k for k, v in label_map.items()}  # map ngược

    # =========================
    # 3. Hàm dự đoán
    # =========================
    def predict_single_with_proba(input_dict):
        df_input = pd.DataFrame([input_dict])
        y_proba = model.predict_proba(df_input)[0]  # Xác suất dự đoán
        pred_class = int(y_proba.argmax())  # Chỉ số class có xác suất cao nhất
        return inv_label_map[pred_class], y_proba

    # =========================
    # 4. Giao diện
    # =========================
    st.title("🎓 dự đoán điểm học kì tiếp theo - CatBoost Model")
    st.write("Dự đoán điểm **Grade** (A/B/C/D)")

    st.subheader("Nhập thông tin để dự đoán")
    col1, col2 = st.columns(2)

    with col1:
        Gender = st.selectbox("Gender", ["Male", "Female"])
        Age = st.number_input("Age", min_value=16, max_value=60, value=20)
        Department = st.selectbox("Department", ["Mathematics", "Business", "Engineering", "Science", "Arts"])
        Attendance = st.number_input("Attendance (%)", min_value=0.0, max_value=100.0, value=90.0)
        Midterm_Score = st.number_input("Midterm_Score", 0.0, 100.0, 50.0)
        Final_Score = st.number_input("Final_Score", 0.0, 100.0, 50.0)
        Assignments_Avg = st.number_input("Assignments_Avg", 0.0, 100.0, 50.0)
        Quizzes_Avg = st.number_input("Quizzes_Avg", 0.0, 100.0, 50.0)
        Participation_Score = st.number_input("Participation_Score", 0.0, 10.0, 5.0)

    with col2:
        Projects_Score = st.number_input("Projects_Score", 0.0, 100.0, 50.0)
        Total_Score = st.number_input("Total_Score", 0.0, 100.0, 50.0)
        Study_Hours_per_Week = st.number_input("Study_Hours_per_Week", 0.0, 60.0, 10.0)
        Extracurricular_Activities = st.selectbox("Extracurricular_Activities", ["Yes", "No"])
        Internet_Access_at_Home = st.selectbox("Internet_Access_at_Home", ["Yes", "No"])
        Parent_Education_Level = st.selectbox("Parent_Education_Level", ["High School", "Bachelor's", "Master's", "PhD"])
        Family_Income_Level = st.selectbox("Family_Income_Level", ["Low", "Medium", "High"])
        Stress_Level = st.number_input("Stress_Level (1-10)", 1, 10, 5)
        Sleep_Hours_per_Night = st.number_input("Sleep_Hours_per_Night", 0.0, 24.0, 8.0)

    # =========================
    # 5. Dự đoán khi nhấn nút
    # =========================
    if st.button("🔮 Dự đoán Grade"):
        input_data = {
            "Gender": Gender,
            "Age": Age,
            "Department": Department,
            "Attendance (%)": Attendance,
            "Midterm_Score": Midterm_Score,
            "Final_Score": Final_Score,
            "Assignments_Avg": Assignments_Avg,
            "Quizzes_Avg": Quizzes_Avg,
            "Participation_Score": Participation_Score,
            "Projects_Score": Projects_Score,
            "Total_Score": Total_Score,
            "Study_Hours_per_Week": Study_Hours_per_Week,
            "Extracurricular_Activities": Extracurricular_Activities,
            "Internet_Access_at_Home": Internet_Access_at_Home,
            "Parent_Education_Level": Parent_Education_Level,
            "Family_Income_Level": Family_Income_Level,
            "Stress_Level (1-10)": Stress_Level,
            "Sleep_Hours_per_Night": Sleep_Hours_per_Night
        }
        grade, probs = predict_single_with_proba(input_data)

        # =========================
        # 5.1 Hiển thị kết quả với màu theo grade
        # =========================
        if grade in ["C", "D"]:
            st.markdown(
                f"""
                <div style="background-color:#ff4d4d; padding:15px; border-radius:10px; color:white; 
                            text-align:center; font-size:20px; font-weight:bold;">
                    🎯 Dự đoán điểm học kỳ tiếp theo của bạn: {grade}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style="background-color:#2ecc71; padding:15px; border-radius:10px; color:white; 
                            text-align:center; font-size:20px; font-weight:bold;">
                    🎯 Dự đoán điểm học kỳ tiếp theo của bạn: {grade}
                </div>
                """,
                unsafe_allow_html=True
            )

        # =========================
        # 5.2 Hiển thị xác suất dự đoán
        # =========================
        st.write("📊 Xác suất dự đoán cho từng lớp:")
        prob_df = pd.DataFrame([probs], columns=[inv_label_map[i] for i in range(len(probs))])
        st.dataframe(prob_df.style.format("{:.2%}"))

        # =========================
        # 6. Lời khuyên cá nhân hóa
        # =========================
        advice = []
        if grade in ["C", "D"]:
            advice.append(
                "🎯 Bạn nên tập trung ôn lại các kiến thức trọng tâm, lập kế hoạch học tập rõ ràng "
                "và dành thêm thời gian luyện tập các dạng bài quan trọng."
            )
            advice.append(
                "📌 Hãy ưu tiên hoàn thành bài tập về nhà, tham gia hỏi đáp trên lớp, "
                "và trao đổi với giảng viên khi chưa hiểu bài."
            )
            advice.append(
                "🕒 Chia nhỏ thời gian học thành các phiên 25-30 phút, xen kẽ nghỉ ngắn để duy trì sự tập trung."
            )

        if Sleep_Hours_per_Night < 4:
            advice.append("🛌 Bạn nên ngủ ít nhất 7-8 tiếng mỗi đêm để cải thiện sức khỏe và khả năng tập trung.")
        elif Sleep_Hours_per_Night < 6:
            advice.append("🛌 Ngủ thêm một chút nữa sẽ giúp bạn tỉnh táo và tiếp thu bài nhanh hơn.")

        if Attendance < 75:
            advice.append("🏫 Hãy cố gắng tham gia đầy đủ các buổi học để không bỏ lỡ kiến thức quan trọng.")

        if Study_Hours_per_Week < 5:
            advice.append("📚 Tăng thời gian tự học lên ít nhất 7-10 giờ mỗi tuần để cải thiện kết quả.")

        if Stress_Level > 7:
            advice.append("🧘 Hãy tìm cách giảm căng thẳng qua thể thao, thiền hoặc nghỉ ngơi hợp lý.")

        if Assignments_Avg < 50:
            advice.append("✍️ Hoàn thành bài tập đầy đủ và luyện tập thêm để nâng cao điểm trung bình.")

        if len(advice) > 0:
            st.subheader("💡 Lời khuyên để cải thiện hiệu suất học tập")
            for tip in advice:
                st.write(tip)
        else:
            st.info("✅ Thói quen học tập của bạn đang rất tốt, hãy duy trì nhé!")


if __name__ == "__main__":
    app()
