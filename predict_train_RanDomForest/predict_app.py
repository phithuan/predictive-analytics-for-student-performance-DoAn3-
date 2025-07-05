import streamlit as st
import pandas as pd
import joblib

def app():
    # Tải mô hình đã huấn luyện
    model = joblib.load(r'D:\MINI_Project\DoAn3\predict_train_RanDomForest\student_at_risk_model.pkl')

    # Tiêu đề ứng dụng
    #st.title("Dự đoán Nguy cơ Học tập Kém của Sinh viên")

    # Form nhập liệu
    st.subheader("Nhập các thông tin để dự đoán hiệu xuất học tập của bạn")

    # Tạo dictionary để lưu trữ dữ liệu đầu vào
    input_data = {}

    # Đặc trưng phân loại với các tùy chọn
    categorical_options = {
        'Gender': ['Nam', 'Nữ'],
        'Department': ['Kỹ thuật', 'Kinh doanh', 'CNTT', 'Toán học'],
        'Extracurricular_Activities': ['Có', 'Không'],
        'Internet_Access_at_Home': ['Có', 'Không'],
        'Parent_Education_Level': ['Không', 'Trung học', 'Cử nhân', 'Thạc sĩ', 'Tiến sĩ'],
        'Family_Income_Level': ['Thấp', 'Trung bình', 'Cao']
    }

    # Đặc trưng số
    numerical_features = ['Age', 'Attendance (%)', 'Study_Hours_per_Week', 'Stress_Level (1-10)', 'Sleep_Hours_per_Night']

    # Nhập liệu cho đặc trưng phân loại
    for feature in categorical_options:
        input_data[feature] = st.selectbox(f"{feature}", options=categorical_options[feature])

    # Nhập liệu cho đặc trưng số
    for feature in numerical_features:
        input_data[feature] = st.number_input(f"{feature}", min_value=0.0, step=0.1)

    # Nút dự đoán
    if st.button("Dự đoán"):
        # Chuyển dữ liệu đầu vào thành DataFrame
        input_df = pd.DataFrame([input_data])
        
        # Dự đoán
        prediction = model.predict(input_df)[0]
        probabilities = model.predict_proba(input_df)[0]
        
        # Hiển thị kết quả
        st.subheader("Kết quả dự đoán")
        if prediction == 1:
            st.error("Sinh viên này có nguy cơ học tập kém.")
        else:
            st.success("Sinh viên này không có nguy cơ học tập kém.")
        
        # Hiển thị xác suất
        st.write(f"Xác suất không có nguy cơ (at_risk=0): {probabilities[0]:.2%}")
        st.write(f"Xác suất có nguy cơ (at_risk=1): {probabilities[1]:.2%}")