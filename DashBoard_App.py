# Import các thư viện cần thiết
import streamlit as st  # Thư viện Streamlit để tạo ứng dụng web tương tác
import pandas as pd     # Thư viện xử lý dữ liệu bảng
import plotly.express as px  # Thư viện vẽ biểu đồ tương tác
from sqlalchemy import create_engine  # Tạo kết nối cơ sở dữ liệu SQL
import time  # Thư viện để sử dụng sleep (ngủ chờ)

    # ===================== CẤU HÌNH GIAO DIỆN STREAMLIT =====================
    # Thiết lập tiêu đề trang và bố cục hiển thị (rộng toàn màn hình)
#st.set_page_config(page_title="🎓 Student Performance Dashboard", layout="wide")

def app():
    # ===================== KẾT NỐI CƠ SỞ DỮ LIỆU ============================
    # Tạo kết nối tới PostgreSQL thông qua SQLAlchemy
    # Định dạng: 'postgresql://<username>:<password>@<host>:<port>/<database>'
    engine = create_engine('postgresql://postgres:123@localhost:5432/student_PB')


    # Tiêu đề chính của trang dashboard
    st.title("📊 Real-Time Student Performance Dashboard")

    # ===================== SIDEBAR: CHỌN THỜI GIAN REFRESH =================
    # Cho phép người dùng chọn khoảng thời gian làm mới dữ liệu (giây)
    refresh_interval = st.sidebar.slider("⏱ Refresh Interval (seconds)", 5, 60, 10)

    # ===================== HÀM LOAD DỮ LIỆU TỪ POSTGRESQL ==================
    # Dùng cache để tránh truy vấn DB liên tục, TTL xác định thời gian cache tồn tại
    @st.cache_data(ttl=refresh_interval)
    def load_data():
        query = """
        SELECT s.student_id, s.first_name, s.last_name, s.gender, s.age, d.department_name,
            ap.total_score, ap.grade, ef.stress_level, ef.study_hours_per_week
        FROM students s
        JOIN departments d ON s.department_id = d.department_id
        JOIN academic_performance ap ON s.student_id = ap.student_id
        JOIN external_factors ef ON s.student_id = ef.student_id;
        """
        df = pd.read_sql(query, engine)  # Thực hiện truy vấn và lấy dữ liệu dưới dạng DataFrame
        return df

    # ===================== TẢI DỮ LIỆU =====================
    df = load_data()

    # ===================== SIDEBAR: BỘ LỌC DỮ LIỆU ==========================
    # Bộ lọc theo khoa (department)
    departments = st.sidebar.multiselect(
        "🏫 Chọn Khoa", 
        options=df['department_name'].unique(),  # Danh sách khoa duy nhất
        default=df['department_name'].unique()   # Mặc định chọn tất cả
    )

    # Bộ lọc theo giới tính
    genders = st.sidebar.multiselect(
        "⚧️ Giới tính", 
        options=df['gender'].unique(), 
        default=df['gender'].unique()
    )

    # ===================== ÁP DỤNG BỘ LỌC ============================
    filtered_df = df[
        (df['department_name'].isin(departments)) & 
        (df['gender'].isin(genders))
    ]

    # ===================== HIỂN THỊ METRIC ===========================
    # Hiển thị số lượng sinh viên theo bộ lọc
    st.metric("👩‍🎓 Số sinh viên", len(filtered_df))

    # ===================== BIỂU ĐỒ 1: Histogram điểm tổng ===================
    # Biểu đồ histogram thể hiện phân phối điểm tổng của sinh viên
    fig1 = px.histogram(
        filtered_df, 
        x="total_score", 
        nbins=20, 
        title="📈 Phân phối điểm tổng"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # ===================== BIỂU ĐỒ 2: Trung bình Stress theo khoa ===========
    # Tính trung bình stress theo từng khoa
    stress_avg = filtered_df.groupby("department_name")["stress_level"].mean().reset_index()

    # Vẽ biểu đồ cột
    fig2 = px.bar(
        stress_avg, 
        x="department_name", 
        y="stress_level", 
        title="😣 Trung bình Stress theo Khoa"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # ===================== BIỂU ĐỒ 3: Pie chart phân loại theo Grade ========
    # Đếm số lượng sinh viên theo Grade
    grade_count = filtered_df['grade'].value_counts().reset_index()
    grade_count.columns = ['grade', 'count']  # Đặt lại tên cột

    # Vẽ biểu đồ tròn
    fig3 = px.pie(
        grade_count, 
        names='grade', 
        values='count', 
        title="🎯 Phân loại sinh viên theo Grade"
    )
    st.plotly_chart(fig3, use_container_width=True)

    # ===================== TỰ ĐỘNG REFRESH GIAO DIỆN ========================
    # Thông báo cho người dùng biết sẽ tự động làm mới sau X giây
    st.info(f"Tự động làm mới sau {refresh_interval} giây...")

    # Tạm dừng chương trình trong khoảng thời gian đã chọn
    time.sleep(refresh_interval)

    # Gọi lại script từ đầu (để thực hiện cập nhật dữ liệu)
    st.rerun()  # Dùng trong Streamlit >= 1.27, thay cho st.experimental_rerun()
