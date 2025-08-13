Dưới đây là nội dung được chuyển đổi từ mã `home.py` sang định dạng `README.md` theo phong cách ví dụ bạn cung cấp:

```markdown
# 🎓 Phân Tích Hiệu Xuất Học Tập Của Sinh Viên

## 📌 Mô tả dự án

Dự án này sử dụng bộ dữ liệu từ [Kaggle - Students Grading Dataset](https://www.kaggle.com/datasets/mahmoudelhemaly/students-grading-dataset) để xây dựng một hệ thống phân tích và dự đoán hiệu suất học tập của sinh viên. Mục tiêu chính bao gồm:

1. **Phát hiện sớm nguy cơ tụt hậu**: Xác định sinh viên có nguy cơ học kém hoặc bỏ học để hỗ trợ kịp thời.
2. **Trực quan hóa dữ liệu**: Cung cấp cái nhìn tổng quan về hiệu suất học tập thông qua các yếu tố gián tiếp.
3. **Xây dựng mô hình học máy**: Dự đoán kết quả học tập dựa trên các đặc trưng như giờ học, mức độ căng thẳng, giấc ngủ, và tỷ lệ chuyên cần.

---

## 📊 Thông tin về dữ liệu

- **Tên tệp**: `Students_Grading_Dataset.csv`
- **Nguồn**: [Kaggle Dataset](https://www.kaggle.com/datasets/mahmoudelhemaly/students-grading-dataset)
- **Số lượng đặc trưng**: 23 đặc trưng về học tập và thông tin cá nhân.

### 📜 Chi tiết 23 thuộc tính
1. **Student_ID**: Mã định danh duy nhất cho mỗi sinh viên.
2. **First_Name**: Tên của học sinh.
3. **Last_Name**: Họ của học sinh.
4. **Email**: Email liên hệ (có thể ẩn danh).
5. **Giới tính**: Nam, Nữ, Khác.
6. **Tuổi**: Độ tuổi của học sinh.
7. **Khoa**: Khoa của sinh viên (VD: Khoa học máy tính, Kỹ thuật, Kinh doanh).
8. **Attendance (%)**: Tỷ lệ tham dự (0-100%).
9. **Midterm_Score**: Điểm thi giữa kỳ (0 Ordering-100).
10. **Final_Score**: Điểm thi cuối kỳ (0-100).
11. **Assignments_Avg**: Điểm trung bình của bài tập (0-100).
12. **Quizzes_Avg**: Điểm trả lời câu hỏi trên lớp trung bình (0-100).
13. **Participation_Score**: Điểm tham gia lớp (0-10).
14. **Projects_Score**: Điểm dự án (0-100).
15. **Total_Score**: Tổng điểm có trọng số.
16. **Điểm (Grade)**: Điểm chữ (A, B, C, D, F).
17. **Study_Hours_per_Week**: Giờ học mỗi tuần.
18. **Hoạt động ngoại khóa**: Có/Không.
19. **Internet_Access_at_Home**: Có/Không.
20. **Parent_Education_Level**: Trình độ học vấn cao nhất của cha mẹ.
21. **Mức thu nhập gia đình**: Thấp, Trung bình, Cao.
22. **Mức độ căng thẳng**: Thang 1-10.
23. **Sleep_Hours_per_Night**: Giờ ngủ mỗi đêm.

**Lưu ý**:
- Các thuộc tính điểm thi (`Final_Score`, `Midterm_Score`, …) được loại bỏ để tránh mô hình trở thành phép tính cộng điểm, đảm bảo ý nghĩa dự đoán.
- Chỉ sử dụng các yếu tố gián tiếp như giờ học, điều kiện internet, trình độ cha mẹ, mức căng thẳng, giấc ngủ, tuổi, và tỷ lệ chuyên cần.

---

## 🧮 Mô hình học máy

### Lựa chọn mô hình: CatBoost
Dự án sử dụng **CatBoost** vì các lý do sau:
- **Xử lý đặc trưng phân loại tự động**: Không cần One-Hot Encoding, tiết kiệm thời gian tiền xử lý.
- **Hiệu suất ổn định**: Phù hợp với dữ liệu nhỏ hoặc không cân bằng.
- **Chống overfitting**: Kỹ thuật Ordered Boosting độc quyền giúp cải thiện độ chính xác.

#### So sánh với các mô hình khác
| Thuộc tính                  | CatBoost                  | LightGBM        | XGBoost          |
|-----------------------------|---------------------------|----------------|------------------|
| Xử lý đặc trưng phân loại   | Tự động                   | Hỗ trợ cơ bản  | Cần tiền xử lý   |
| Chiến lược chia cây         | Đối xứng                  | Theo lá        | Theo độ sâu      |
| Tốc độ & hiệu suất          | Tối ưu                    | Lớn            | Nhanh & mở rộng  |

#### Kết quả so sánh
- **CatBoost**: Accuracy **0.65**, F1 **0.51** ✅
- **XGBoost**: Accuracy **0.597**, F1 **0.5524** 🔻
- **LightGBM**: Tốc độ huấn luyện nhanh nhưng yêu cầu xử lý dữ liệu kỹ lưỡng.

---

## 📈 Quá trình huấn luyện & cải thiện mô hình CatBoost

### 1️⃣ Mô hình ban đầu (Baseline)
- Tham số mặc định.
- **Accuracy**: 57%
- Hạn chế: Dự đoán kém ở lớp thiểu số **A** và **D**.

### 2️⃣ Tinh chỉnh sơ bộ
- **Tham số**:
  - `iterations = 100`: Số vòng lặp (cây).
  - `learning_rate = 0.1`: Tốc độ học.
  - `depth = 6`: Độ sâu cây.
  - `verbose = 0`: Ẩn log huấn luyện.
  - `class_weights = [5.0, 1.0, 1.0, 10.0]`: Ưu tiên lớp **A** và **D**.
- **Accuracy**: 59%

### 3️⃣ Tối ưu bằng RandomizedSearchCV
- **Tập siêu tham số**:
  ```python
  param_grid = {
      'iterations': [100, 300, 500],
      'learning_rate': [0.01, 0.05, 0.1, 0.2],
      'depth': [4, 6, 8, 10],
      'l2_leaf_reg': [1, 3, 5, 7],
      'border_count': [32, 64, 128]
  }
  ```
- **Phương pháp**:
  - Thử 20 tổ hợp tham số ngẫu nhiên (`n_iter=20`).
  - Đánh giá bằng `f1_weighted`, kiểm định chéo 3 lần (`cv=3`).
  - Chạy song song (`n_jobs=-1`) để tăng tốc.
- **Accuracy**: 60%
- Hạn chế: Vẫn gặp khó khăn với lớp thiểu số.

### 4️⃣ Chuyển sang bài toán nhị phân
- **Quy ước**:
  - `at_risk = 1` nếu Grade ∈ {C, D}
  - `at_risk = 0` nếu Grade ∈ {A, B}
- **Kết quả**: Accuracy **65%**, hiệu quả hơn trong nhận diện nhóm sinh viên **nguy cơ yếu**.

---

## 📊 Kết luận & Hướng phát triển

### Kết quả
- Mô hình CatBoost đạt **Accuracy 65%** trên 23 đặc trưng.

### Hạn chế
- Tương quan đặc trưng thấp.
- Dữ liệu nhiễu, mất cân bằng nhãn.
- Tập dữ liệu nhỏ.

### Hướng phát triển
- Xây dựng chatbot hỗ trợ tư vấn học tập.
- Mở rộng dữ liệu từ nhiều nguồn.
- Tích hợp dashboard thời gian thực.
- Thêm các yếu tố tâm lý và hành vi.

---

## 🛠 Công cụ sử dụng
- **Ngôn ngữ lập trình**: Python
- **Thư viện**: Streamlit, CatBoost, Scikit-learn
- **Nguồn dữ liệu**: Kaggle
```

### Giải thích
- **Cấu trúc**: Nội dung được tổ chức theo các mục chính như trong ví dụ (`Mô tả dự án`, `Thông tin về dữ liệu`, `Mô hình học máy`, `Quá trình huấn luyện`, `Kết luận & Hướng phát triển`).
- **Ngôn ngữ**: Sử dụng tiếng Việt, giữ nguyên các thuật ngữ kỹ thuật và định dạng tương tự ví dụ.
- **Biểu tượng**: Thêm các biểu tượng emoji (📌, 📊, 🧮, v.v.) để tăng tính trực quan, đúng theo phong cách ví dụ.
- **Định dạng Markdown**: Sử dụng tiêu đề (`#`, `##`), danh sách, bảng, và khối mã (` ```python `) để trình bày rõ ràng và chuyên nghiệp.
- **Nội dung**: Chuyển đổi toàn bộ thông tin từ `home.py` sang dạng văn bản Markdown, giữ nguyên các chi tiết kỹ thuật và kết quả.

Nếu bạn cần chỉnh sửa thêm hoặc muốn thêm phần nào (ví dụ: cách chạy dự án, hướng dẫn cài đặt), hãy cho tôi biết!