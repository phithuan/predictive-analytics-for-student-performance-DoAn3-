# home.py
import streamlit as st

def app():
    st.title("🏠 Giới thiệu Đề tài")

    # --- Lý do chọn đề tài ---
    st.markdown(
        """
        <h3 style='color:#FF6F61'>1️⃣ Lý do chọn đề tài</h3>
        <ul>
            <li>📈 <b>Hiệu suất học tập</b> phản ánh <span style='color:#4CAF50'>chất lượng đào tạo</span>.</li>
            <li>🤖 Ứng dụng <b>AI</b> & <b>khoa học dữ liệu</b> giúp phát hiện sớm sinh viên gặp khó khăn.</li>
            <li>🎯 Mục tiêu: <span style='color:#2196F3'>nâng cao chất lượng</span> & <span style='color:#E91E63'>giảm tỷ lệ bỏ học</span>.</li>
        </ul>
        """,
        unsafe_allow_html=True
    )

    # --- Mục tiêu nghiên cứu ---
    st.markdown(
        """
        <h3 style='color:#FF9800'>2️⃣ Mục tiêu nghiên cứu</h3>
        <ul>
            <li>🧠 Xây dựng mô hình ML <b>dự đoán hiệu suất học tập</b>.</li>
            <li>📊 Phân tích & trực quan hóa dữ liệu sinh viên.</li>
            <li>⚖️ So sánh các thuật toán: <b>Random Forest</b>, <b>CatBoost</b>, <b>XGBoost</b>...</li>
            <li>💻 Xây dựng <b>ứng dụng dự đoán thân thiện</b> hỗ trợ nhà trường.</li>
        </ul>
        """,
        unsafe_allow_html=True
    )

    # --- Phương pháp nghiên cứu ---
    st.markdown(
        """
        <h3 style='color:#9C27B0'>3️⃣ Phương pháp nghiên cứu</h3>
        <ul>
            <li>📥 Thu thập dữ liệu: điểm số, chuyên cần, áp lực học tập, thời gian ngủ...</li>
            <li>🧹 Tiền xử lý: làm sạch, chuẩn hóa, mã hóa dữ liệu.</li>
            <li>📈 Phân tích thống kê & trực quan hóa dữ liệu.</li>
            <li>🤝 Xây dựng, đánh giá & triển khai mô hình dự đoán bằng <b>Streamlit</b>.</li>
        </ul>
        """,
        unsafe_allow_html=True
    )
