# 🎓 Student Performance & Behavior Dataset– Data Cleaning, Analysis & Machine Learning

## 📌 Mô tả dự án

Dự án này sử dụng bộ dữ liệu từ [Kaggle - Students Grading Dataset](https://www.kaggle.com/datasets/mahmoudelhemaly/students-grading-dataset), nhằm mục tiêu:

1. **Làm sạch dữ liệu**: Kiểm tra và xử lý các giá trị thiếu, dữ liệu không hợp lệ, chuẩn hóa các cột.
2. **Phân tích dữ liệu**: Khám phá các xu hướng, mối quan hệ giữa điểm số và các yếu tố như thời gian học, mức độ căng thẳng, giấc ngủ, v.v.
3. **Xây dựng mô hình học máy**: Dự đoán khả năng học sinh đạt điểm thấp hoặc có nguy cơ bỏ học dựa trên các đặc trưng đầu vào.

---

## 📊 Thông tin về dữ liệu

- **Tên tệp**: `Students_Grading_Dataset.csv`
- **Nguồn**: [Kaggle Dataset](https://www.kaggle.com/datasets/mahmoudelhemaly/students-grading-dataset)

---

## 🧹 Các bước chính

### 1. Làm sạch dữ liệu (Data Cleaning)
- Xử lý dữ liệu bị thiếu (`NaN`)
- Chuyển đổi kiểu dữ liệu phù hợp
- Loại bỏ các giá trị ngoại lai (outliers)
- Chuẩn hóa dữ liệu

### 2. Phân tích dữ liệu (EDA - Exploratory Data Analysis)
- Phân phối điểm số học sinh
- Mối quan hệ giữa thời gian học/ngủ và kết quả học tập
- Ảnh hưởng của stress và chuyên cần đến điểm số
- Biểu đồ trực quan: histogram, heatmap, scatterplot,...

### 3. Áp dụng mô hình học máy (ML Modeling)
- Mục tiêu:
  - Dự đoán xác suất học sinh **có kết quả thấp**
  - Ước lượng nguy cơ **bỏ học**
- Các mô hình sử dụng:
  - Random Forest
  - Logistic Regression
  - Decision Tree
- Đánh giá mô hình:
  - Accuracy, Precision, Recall, F1-score
  - ROC-AUC

---

## 🧰 Công nghệ sử dụng

- Python (Pandas, Scikit-learn, Seaborn, Matplotlib)
- Jupyter Notebook
- Streamlit (nếu xây dựng giao diện người dùng)
- PostgreSQL (nếu sử dụng lưu trữ dữ liệu)
- Power BI / Tableau / Grafana (nếu có trực quan hóa nâng cao)

---

## 📁 Cấu trúc thư mục đề xuất



## 📌 Mô tả dự án

Dự án này sử dụng bộ dữ liệu từ [Kaggle - Students Grading Dataset](https://www.kaggle.com/datasets/mahmoudelhemaly/students-grading-dataset), nhằm mục tiêu:

1. **Làm sạch dữ liệu**: Kiểm tra và xử lý các giá trị thiếu, dữ liệu không hợp lệ, chuẩn hóa các cột.
2. **Phân tích dữ liệu**: Khám phá các xu hướng, mối quan hệ giữa điểm số và các yếu tố như thời gian học, mức độ căng thẳng, giấc ngủ, v.v.
3. **Xây dựng mô hình học máy**: Dự đoán khả năng học sinh đạt điểm thấp hoặc có nguy cơ bỏ học dựa trên các đặc trưng đầu vào.

---


## ✅ Kết quả kỳ vọng

- Báo cáo phân tích dữ liệu đầy đủ, trực quan
- Mô hình học máy có thể dự đoán chính xác học sinh gặp khó khăn
- Dashboard hoặc giao diện dễ sử dụng cho người dùng không chuyên

---

## 📚 Tài liệu tham khảo

- Kaggle Dataset: https://www.kaggle.com/datasets/mahmoudelhemaly/students-grading-dataset
- Scikit-learn documentation: https://scikit-learn.org/
- Pandas documentation: https://pandas.pydata.org/
- Matplotlib: https://matplotlib.org/
- Streamlit: https://streamlit.io/


