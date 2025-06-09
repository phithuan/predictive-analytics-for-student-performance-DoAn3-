import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

def app():
    st.title("📊 Phân tích hiệu suất học tập theo Khoa")

    # ===================== KẾT NỐI DATABASE =====================
    #engine = create_engine('postgresql://postgres:123@localhost:5432/student_performance_behavior')

    # ===================== TẢI DỮ LIỆU ==========================
    # Thiết lập seaborn cho đẹp hơn
    sns.set(style="whitegrid")

    # Load dataset
    dataset = r'D:\MINI_Project\DoAn3\students_grading_dataset_clean.csv'
    df = pd.read_csv(dataset)

    # 1. Lấy mẫu đều từ mỗi khoa
    sample_size = 1000  # Số lượng mẫu muốn lấy từ mỗi khoa
    df_sampled = df.groupby("Department").apply(lambda x: x.sample(n=sample_size, random_state=2500)).reset_index(drop=True)

    # 2. Tính điểm trung bình theo khoa
    dept_avg = df_sampled.groupby("Department")["Total_Score"].mean()

    # 3. Tính điểm danh trung bình theo khoa
    attendance_avg = df_sampled.groupby("Department")["Attendance (%)"].mean()

    # 4. Đếm số lượng học sinh theo từng loại điểm (Grade) trong mỗi khoa
    dept_grade_cnt = pd.crosstab(df_sampled['Department'], df_sampled['Grade'])

    fig, axes = plt.subplots(1, 2, figsize=(16, 9))  # 1 hàng, 2 cột

    # 5.1 Biểu đồ Pie thể hiện phân phối điểm trung bình theo khoa
    axes[0].pie(
        dept_avg,
        labels=dept_avg.index,
        autopct='%1.1f%%',
        colors=sns.color_palette("mako", len(dept_avg))
    )
    axes[0].set_title("Equal Sampled Total Score Distribution", fontsize=14, fontweight="bold")

    # 5.3 Biểu đồ cột xếp chồng thể hiện phân phối điểm (Grade) theo khoa
    bar_colors = sns.color_palette("Set2", n_colors=len(dept_grade_cnt.columns))
    dept_grade_cnt.plot(
        kind="bar",
        stacked=True,
        color=bar_colors,
        ax=axes[1],
        edgecolor="black",
        linewidth=1.2
    )
    axes[1].set_title("Grade Distribution Across Departments", fontsize=14, fontweight="bold")
    axes[1].set_xlabel("Department")
    axes[1].set_ylabel("Number of Students")
    axes[1].tick_params(axis='x', rotation=45)  # Xoay trục X 45 độ cho dễ đọc

    # 6. Tối ưu bố cục và hiển thị trên Streamlit
    plt.tight_layout()
    st.pyplot(fig)

    # Thêm thông tin bổ sung
    st.subheader("📋 Summary Statistics")
    st.write("Average Total Score by Department:", dept_avg)
    st.write("Average Attendance (%) by Department:", attendance_avg)
