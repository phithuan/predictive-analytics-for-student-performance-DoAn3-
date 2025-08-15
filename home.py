# home.py
import streamlit as st

def app():
    st.title("🏠 PHÂN TÍCH HIỆU XUẤT HỌC TẬP CỦA SINH VIÊN")

    with st.expander("📌 1️⃣ Mở đầu – Giới thiệu tổng quan"):
        st.markdown("""
        **Lý do chọn đề tài:**  
        - Có nhiều sinh viên gặp khó khăn nhưng chưa được hỗ trợ kịp thời 
        - tạo mô hình nhầm mục đích phát hiện sớm sinh viên có nguy cơ tụt hậu hoặc bỏ học
        - từ đó hỗ trợ kịp thời và nâng cao chất lượng đào tạo  

        **Mục tiêu:**  
        Xây dựng hệ thống dự đoán & trực quan hóa kết quả học tập.  

        **Đối tượng áp dụng:**  
        Sinh viên, giảng viên, cố vấn học tập nhằm dự đoán hiệu suất và cải thiện điểm yếu.
        """)

    with st.expander("📂 2️⃣ Dữ liệu"):
        st.markdown("""
        **Nguồn dữ liệu:** Kaggle (students grading dataset).  
        **Trích xuất đặc trưng:** 23 đặc trưng về học tập.  
                      
        ---
        ### 📜 Chi tiết 23 thuộc tính:
        1. **Student_ID**: Mã định danh duy nhất cho mỗi sinh viên.  
        2. **First_Name**: Tên của học sinh.  
        3. **Last_Name**: Họ của học sinh.  
        4. **Email**: Email liên hệ (có thể ẩn danh).  
        5. **Giới tính**: Nam, Nữ, Khác.✅  
        6. **Tuổi**: Độ tuổi của học sinh. ✅  
        7. **Khoa**: Khoa của sinh viên (VD: Khoa học máy tính, Kỹ thuật, Kinh doanh).✅  
        8. **Attendance (%)**: Tỷ lệ tham dự (0-100%).✅  
        9. **Midterm_Score**: Điểm thi giữa kỳ (0-100).  
        10. **Final_Score**: Điểm thi cuối kỳ (0-100).  
        11. **Assignments_Avg**: Điểm trung bình của bài tập (0-100). ✅   
        12. **Quizzes_Avg**: Điểm trả lời câu đó trên lớp trung bình (0-100).✅  
        13. **Participation_Score**: Điểm tham gia lớp (0-10).✅  
        14. **Projects_Score**: Điểm dự án (0-100).  
        15. **Total_Score**: Tổng điểm có trọng số.  
        16. **Điểm (Grade)**: Điểm chữ (A, B, C, D, F).  
        17. **Study_Hours_per_Week**: Giờ học mỗi tuần.✅  
        18. **Hoạt động ngoại khóa**: Có/Không.✅  
        19. **Internet_Access_at_Home**: Có/Không.✅  
        20. **Parent_Education_Level**: Trình độ học vấn cao nhất của cha mẹ.✅  
        21. **Mức thu nhập gia đình**: Thấp, Trung bình, Cao.✅  
        22. **Mức độ căng thẳng**: Thang 1-10.✅  
        23. **Sleep_Hours_per_Night**: Giờ ngủ mỗi đêm. ✅ 
                    
        - Cố tình loại bỏ các thuộc tính điểm thi (Final_Score, Midterm_Score, …) vì chúng phản ánh trực tiếp kết quả học tập và sẽ biến mô hình thành phép tính cộng điểm, không còn ý nghĩa dự đoán.
                    
        - Thay vào đó, chỉ dùng các yếu tố gián tiếp như giờ học, điều kiện internet, trình độ cha mẹ, mức căng thẳng, giấc ngủ, tuổi, và tỷ lệ chuyên cần — dù tương quan tuyến tính thấp — để mô hình có thể dự đoán trước khi có điểm thi.
        """)


    with st.expander("🧮 3️⃣ Lựa chọn mô hình – Vì sao CatBoost?"):
        st.markdown("""
        **So sánh nhanh:**

        | Thuộc tính                  | CatBoost                  | LightGBM        | XGBoost          |
        |-----------------------------|---------------------------|----------------|------------------|
        | Xử lý đặc trưng phân loại   | Tự động                   | Hỗ trợ cơ bản  | Cần tiền xử lý   |
        | Chiến lược chia cây         | Đối xứng                   | Theo lá        | Theo độ sâu      |
        | Tốc độ & hiệu suất          | Ổn định và tối ưu với dữ liệu vừa & nhỏ, đặc biệt khi có nhiều đặc trưng phân loại                     | Rất nhanh với tập dữ liệu lớn, tối ưu cho hàng triệu bản ghi            | Nhanh, linh hoạt, mở rộng tốt trên CPU & GPU  |

        **🎯 Vì sao chọn CatBoost?**
        - 🔍 Xử lý đặc trưng phân loại tốt mà không cần One-Hot Encoding ➡️ tiết kiệm thời gian tiền xử lý.
        - ⚡ Hiệu suất ổn định ngay cả khi dữ liệu không quá lớn hoặc không cân bằng.
        - 🛡 Chống overfitting tốt nhờ kỹ thuật Ordered Boosting độc quyền.
        - 🧠 dữ liệu chỉ 5000 mẫu, nhưng vẫn đạt được kết quả tốt ở thuật toán CatBoost.

        **📈 So sánh kết quả:**
        - CatBoost: Accuracy **0.65**, F1 **0.51** ✅
        - XGBoost: Accuracy **0.597**, F1 **0.5524** 🔻
        - LightGBM: Tốc độ huấn luyện nhanh nhưng cần xử lý dữ liệu rất kỹ.
        """)

    with st.expander("🔍 4: QUÁ TRÌNH HUẤN LUYỆN & CẢI THIỆN MÔ HÌNH CATBOOST"):
        st.markdown("""
        **1️⃣ Mô hình CatBoost ban đầu (Baseline)**  
        - Tham số mặc định.  
        - Accuracy: **57%**  
        - Dự đoán kém ở lớp thiểu số **A** và **D**.  

        ---

        **2️⃣ Tinh chỉnh sơ bộ**  
        - `iterations = 100` → Số vòng lặp (cây). Cao hơn giúp mô hình học kỹ hơn nhưng dễ overfit nếu quá lớn.  
        - `learning_rate=0.1` → Tốc độ học:  
            - Nhỏ → Học chậm, chính xác hơn, cần nhiều vòng lặp.  
            - Lớn → Học nhanh, nhưng có thể bỏ sót thông tin quan trọng.    
        - `depth = 6` → Độ sâu cây. Độ sâu cao giúp mô hình học được quan hệ phức tạp nhưng dễ bị overfit.  
        - `verbose = 0` → Ẩn log huấn luyện (có thể đặt `verbose=100` để xem tiến trình).  
        - `class_weights = [5.0, 1.0, 1.0, 10.0]` → Cân bằng dữ liệu, ưu tiên lớp **A** và **D**.  
                    
        - Accuracy: **59%**  

        ---

        **3️⃣ Tối ưu bằng RandomizedSearchCV**  
        - **Tập siêu tham số cần thử:**  
            ```python
            param_grid = {
                'iterations': [100, 300, 500],
                'learning_rate': [0.01, 0.05, 0.1, 0.2],
                'depth': [4, 6, 8, 10],
                'l2_leaf_reg': [1, 3, 5, 7], # để kiểm soát độ phức tạp.
                'border_count': [32, 64, 128] # để điều chỉnh độ chi tiết khi xử lý biến số liên tục.
            }
            ```
        - **Cách thực hiện:**  
            - Sử dụng `RandomizedSearchCV` thử 20 tổ hợp tham số ngẫu nhiên (`n_iter=20`).  
            - Đánh giá bằng `f1_weighted`, kiểm định chéo 3 lần (`cv=3`).  
            - Chạy song song (`n_jobs=-1`) để tăng tốc.  
                    
        - Accuracy: **60%**  
        - Cải thiện nhẹ nhưng vẫn hạn chế ở lớp thiểu số.  

        ---

        **4️⃣ Chuyển sang bài toán nhị phân**  
        Trong thực tế, việc đánh giá học lực thông qua điểm chữ (Grade: A, B, C, D) giúp phân loại trình độ học sinh. 
        Tuy nhiên, ở góc độ quản lý và hỗ trợ học tập, chỉ cần số nhị phân phản ánh `nguy cơ học yếu` để:
            	 Cảnh báo sớm
            	- Tập trung nguồn lực hỗ trợ
            	- Đơn giản hóa dự đoán
        - Quy ước:  
            - `at_risk = 1` nếu Grade ∈ {C, D}  
            - `at_risk = 0` nếu Grade ∈ {A, B}  
        - Huấn luyện với tham số tối ưu từ RandomizedSearchCV.  
                    
        - Accuracy: **65%**  
        - Nhận diện nhóm sinh viên **nguy cơ yếu** hiệu quả hơn.
        """)



    with st.expander("📊 5️⃣ Kết luận & Hướng phát triển"):
        st.markdown("""
        **Kết quả:**  
        - CatBoost dự đoán trên 14 đặc trưng, Accuracy 65%.  

        **Hạn chế:**  
        - Tương quan đặc trưng thấp dữ liệu , mất cân bằng nhãn, tập dữ liệu nhỏ.  
        -> độ chính xác của mô hình sẽ không được cao

        **Hướng phát triển:**
        - chat bot hỗ trợ tư vấn học tập.  
        - Mở rộng dữ liệu từ nhiều nguồn.  
        - Tích hợp dashboard thời gian thực/ giao diện thân hiện hơn
        """)
