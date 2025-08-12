import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def app():

    # ===================== TẢI DỮ LIỆU GỐC =====================
    dataset = r'D:\MINI_Project\DoAn3\students_grading_dataset_clean.csv'
    df = pd.read_csv(dataset)

    # Hiển thị dữ liệu gốc trên Streamlit
    st.subheader("📄 Dữ liệu gốc")
    st.dataframe(df)  # Bảng dữ liệu có thể cuộn

    # Thiết lập giao diện đồ thị của seaborn
    sns.set(style="whitegrid")

    # Tiêu đề trang chính
    st.title("📊 Phân tích hiệu suất học tập của sinh viên")

    # ===================== TẢI LẠI DỮ LIỆU (đảm bảo không bị ảnh hưởng bởi các biến đổi sau này) =====================
    sns.set(style="whitegrid")
    dataset = r'D:\MINI_Project\DoAn3\students_grading_dataset_clean.csv'
    df = pd.read_csv(dataset)

    # ===================== 1. BIỂU ĐỒ CỘT SỐ LƯỢNG TỪNG LOẠI ĐIỂM =====================
    st.subheader("1. Số lượng học sinh theo từng loại điểm")

    # Thứ tự hiển thị điểm chữ
    grade_order = ['A', 'B', 'C', 'D']
    # Đếm số lượng từng loại điểm
    grade_counts = df['Grade'].value_counts() # đếm bao nhiêu học sinh đạt từng loại điểm.

    # Vẽ biểu đồ cột
    fig_bar, ax_bar = plt.subplots(figsize=(6, 4))
    grade_counts.loc[grade_order].plot(
        kind='bar',  # Kiểu cột
        color=['#4C72B0', '#55A868', '#C44E52', '#8172B3'],  # Màu cho từng cột
        ax=ax_bar
    )
    ax_bar.set_title('Số lượng học sinh theo từng loại điểm')  # Tiêu đề biểu đồ
    ax_bar.set_xlabel('Điểm chữ')  # Nhãn trục X
    ax_bar.set_ylabel('Số lượng học sinh')  # Nhãn trục Y
    ax_bar.tick_params(axis='x', rotation=0)  # Không xoay nhãn trục X
    st.pyplot(fig_bar)  # Hiển thị trên Streamlit

    # ===================== LẤY MẪU ĐỀU TỪ MỖI KHOA =====================
    sample_size = 1000
    # Lấy ngẫu nhiên "sample_size" sinh viên từ mỗi khoa, giữ nguyên tỉ lệ
    df_sampled = df.groupby("Department").apply(lambda x: x.sample(n=sample_size, random_state=2500)).reset_index(drop=True)

    # ===================== TÍNH TOÁN CÁC GIÁ TRỊ TRUNG BÌNH =====================
    dept_avg = df_sampled.groupby("Department")["Total_Score"].mean()  # Điểm trung bình mỗi khoa
    attendance_avg = df_sampled.groupby("Department")["Attendance (%)"].mean()  # Tỉ lệ điểm danh TB mỗi khoa
    dept_grade_cnt = pd.crosstab(df_sampled['Department'], df_sampled['Grade'])  # Bảng đếm loại điểm theo khoa

    # ===================== 2.BIỂU ĐỒ PHÂN BỐ ĐIỂM & LOẠI ĐIỂM =====================
    st.subheader("2. Phân tích hiệu suất học tập theo Khoa")
    fig, axes = plt.subplots(1, 2, figsize=(16, 9))  # Tạo 2 biểu đồ cạnh nhau

    # --- Biểu đồ tròn: tỉ lệ điểm trung bình giữa các khoa ---
    axes[0].pie(
        dept_avg,
        labels=dept_avg.index,  # Nhãn là tên khoa
        autopct='%1.1f%%',  # Hiển thị phần trăm
        colors=sns.color_palette("mako", len(dept_avg))  # Bảng màu
    )
    axes[0].set_title("Tỉ lệ điểm trung bình giữa các khoa", fontsize=14, fontweight="bold")

    # --- Biểu đồ cột xếp chồng: phân bố loại điểm chữ theo khoa ---
    bar_colors = sns.color_palette("Set2", n_colors=len(dept_grade_cnt.columns))
    dept_grade_cnt.plot(
        kind="bar",
        stacked=True,  # Cột xếp chồng
        color=bar_colors,
        ax=axes[1],
        edgecolor="black",  # Viền cột
        linewidth=1.2
    )
    axes[1].set_title("Phân bố loại điểm chữ của sinh viên theo khoa", fontsize=14, fontweight="bold")
    axes[1].set_xlabel("Department")  # Trục X
    axes[1].set_ylabel("Number of Students")  # Trục Y
    axes[1].tick_params(axis='x', rotation=45)  # Xoay nhãn trục X để dễ đọc

    plt.tight_layout()
    st.pyplot(fig)

    # ===================== SUMMARY (THỐNG KÊ TÓM TẮT)=====================
    st.subheader("📋 Summary Statistics")
    st.write("Average Total Score by Department:", dept_avg)  # Điểm trung bình
    st.write("Average Attendance (%) by Department:", attendance_avg)  # Điểm danh TB

    # ===================== 3. BIỂU ĐỒ NHIỆT TƯƠNG QUAN =====================
    st.subheader("3.🔥Biểu đồ nhiệt tương quan các yếu tố hiệu suất")

    # Các cột sẽ đưa vào tính tương quan
    correlation_columns = [
        'Total_Score', 'Final_Score', 'Midterm_Score', 'Assignments_Avg', 'Quizzes_Avg',
        'Projects_Score', 'Participation_Score', 'Grade', 'Study_Hours_per_Week',
        'Internet_Access_at_Home', 'Parent_Education_Level', 'Stress_Level (1-10)',
        'Sleep_Hours_per_Night', 'Age', 'Attendance (%)'
    ]

    # Chuyển đổi dữ liệu phân loại sang số để tính toán
    df['Grade'] = df['Grade'].map({'A': 4, 'B': 3, 'C': 2, 'D': 1, 'F': 0})
    df['Internet_Access_at_Home'] = df['Internet_Access_at_Home'].map({'Yes': 1, 'No': 0})
    df['Parent_Education_Level'] = df['Parent_Education_Level'].map({
        'PhD': 4, "Master's": 3, "Bachelor's": 2, 'High School': 1, 'Unknown': 0
    })

    # Tạo ma trận tương quan
    correlation_matrix = df[correlation_columns].corr()

    # Vẽ heatmap
    fig_corr, ax_corr = plt.subplots(figsize=(9, 6))
    sns.heatmap(
        correlation_matrix,
        annot=True,  # Hiển thị số tương quan
        cmap='coolwarm',  # Bảng màu
        vmin=-1, vmax=1, center=0,  # Phạm vi màu
        square=True,  # Ô vuông
        fmt='.2f',  # Định dạng số
        ax=ax_corr,
        annot_kws={"size": 8}  # Cỡ chữ nhỏ hơn
    )
    ax_corr.set_title('Biểu đồ nhiệt tương quan của các yếu tố hiệu suất học sinh')
    plt.xticks(rotation=45, ha='right')  # Xoay nhãn X
    plt.yticks(rotation=0)  # Giữ nhãn Y ngang

    st.pyplot(fig_corr)  # Hiển thị heatmap
