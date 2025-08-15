import streamlit as st
import pandas as pd
import joblib
def app():
    # Tải mô hình và bộ mã hóa
    model = joblib.load(r'perdict_train_XGBoost/catboost_modelNEW.pkl')
    label_encoders = joblib.load(r'perdict_train_XGBoost/label_encodersNEW.pkl')
    class_mappings = joblib.load(r'perdict_train_XGBoost/class_mappingsNEW.pkl')


    st.title("📚 Student Risk Predictor")
    st.markdown("Nhập thông tin sinh viên để dự đoán nguy cơ học tập kém.")

    # Khởi tạo các trường input
    input_data = {}

    input_data['Gender'] = st.selectbox("Gender", class_mappings['Gender'])
    input_data['Age'] = st.slider("Age", 15, 30, 20)
    input_data['Department'] = st.selectbox("Department", class_mappings['Department'])
    #input_data['Attendance (%)'] = st.slider("Attendance (%)", 0, 100, 85)
    input_data['Study_Hours_per_Week'] = st.slider("Study Hours per Week", 0, 60, 10)
    input_data['Extracurricular_Activities'] = st.selectbox("Extracurricular Activities", class_mappings['Extracurricular_Activities'])
    input_data['Internet_Access_at_Home'] = st.selectbox("Internet Access at Home", class_mappings['Internet_Access_at_Home'])
    input_data['Parent_Education_Level'] = st.selectbox("Parent Education Level", class_mappings['Parent_Education_Level'])
    input_data['Family_Income_Level'] = st.selectbox("Family Income Level", class_mappings['Family_Income_Level'])
    input_data['Stress_Level (1-10)'] = st.slider("Stress Level (1-10)", 1, 10, 5)
    input_data['Sleep_Hours_per_Night'] = st.slider("Sleep Hours per Night", 0, 12, 7)
    #input_data['Assignments_Avg'] = st.slider("Assignments Avg (0-100)", 0, 100, 75)
    #input_data['Quizzes_Avg'] = st.slider("Quizzes Avg (0-100)", 0, 100, 70)
    #input_data['Participation_Score'] = st.slider("Participation Score (0-100)", 0, 100, 80)

    # Dữ liệu dưới dạng DataFrame
    input_df = pd.DataFrame([input_data])

    # Mã hóa nhãn categorial
    for col in input_df.select_dtypes(include='object').columns:
        le = label_encoders[col]
        input_df[col] = le.transform(input_df[col])

    # Dự đoán
    if st.button("Dự đoán nguy cơ"):
        prediction = model.predict(input_df)[0]
        proba = model.predict_proba(input_df)[0][1]

        if prediction == 1:
            st.error(f"⚠️ Có nguy cơ học tập kém! (Xác suất: {proba:.2%})")
            st.subheader("📌 Lời khuyên:")
            if input_data['Sleep_Hours_per_Night'] < 7:
                st.write("- Ngủ đủ 7-8 tiếng mỗi đêm để cải thiện sự tập trung.")
            if input_data['Study_Hours_per_Week'] < 15:
                st.write("- Tăng thời gian học lên ít nhất 15 giờ/tuần.")
            if input_data['Stress_Level (1-10)'] > 7:
                st.write("- Giảm căng thẳng bằng thể dục hoặc hoạt động giải trí.")
            st.write("- Tham gia lớp phụ đạo hoặc nhóm học tập để hỗ trợ kiến thức.")
        else:
            st.success(f"✅ Học tập ổn định (Xác suất nguy cơ: {proba:.2%})")
            st.subheader("📌 Lời khuyên:")
            st.write("- Tiếp tục duy trì thời gian học và ngủ hợp lý.")
            st.write("- Giữ mức căng thẳng thấp và tham gia hoạt động ngoại khóa lành mạnh.")
