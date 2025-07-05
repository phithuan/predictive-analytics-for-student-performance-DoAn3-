import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

# Đọc dữ liệu từ file CSV
data = pd.read_csv(r'D:\MINI_Project\DoAn3\Data\Students_Grading_Dataset_Biased.csv')

# Tạo nhãn mục tiêu 'at_risk': 1 nếu học sinh có điểm D hoặc F (nguy cơ), 0 nếu không
data['at_risk'] = data['Grade'].apply(lambda x: 1 if x in ['D', 'F'] else 0)

# Chọn các đặc trưng đầu vào cho mô hình
features = ['Gender', 'Age', 'Department', 'Attendance (%)', 'Study_Hours_per_Week', 
            'Extracurricular_Activities', 'Internet_Access_at_Home', 'Parent_Education_Level', 
            'Family_Income_Level', 'Stress_Level (1-10)', 'Sleep_Hours_per_Night']

# Biến đầu vào X và biến mục tiêu y
X = data[features]
y = data['at_risk']

# Phân loại các đặc trưng thành số và phân loại
numerical_features = ['Age', 'Attendance (%)', 'Study_Hours_per_Week', 'Stress_Level (1-10)', 'Sleep_Hours_per_Night']
categorical_features = ['Gender', 'Department', 'Extracurricular_Activities', 'Internet_Access_at_Home', 
                        'Parent_Education_Level', 'Family_Income_Level']

# Xây dựng pipeline tiền xử lý:
# - Với đặc trưng số: thay thế giá trị thiếu bằng trung vị
# - Với đặc trưng phân loại: thay thế thiếu bằng giá trị phổ biến nhất, sau đó mã hóa one-hot
preprocessor = ColumnTransformer(
    transformers=[
        ('num', SimpleImputer(strategy='median'), numerical_features),
        ('cat', Pipeline([
            ('imputer', SimpleImputer(strategy='most_frequent')),  # xử lý thiếu cho dữ liệu phân loại
            ('onehot', OneHotEncoder(handle_unknown='ignore'))     # mã hóa one-hot cho dữ liệu phân loại
        ]), categorical_features)
    ]
)

# Xây dựng pipeline hoàn chỉnh: tiền xử lý + huấn luyện mô hình Random Forest
model = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42))  # random_state để đảm bảo tính tái lập
])

# Chia tập dữ liệu thành train và test (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Huấn luyện mô hình trên tập train
model.fit(X_train, y_train)

# Lưu mô hình đã huấn luyện vào file .pkl để sử dụng sau
joblib.dump(model, 'student_at_risk_model.pkl')
print("Mô hình đã được huấn luyện và lưu vào 'student_at_risk_model.pkl'")


from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Dự đoán trên tập kiểm tra
y_pred = model.predict(X_test)

# Tính độ chính xác
accuracy = accuracy_score(y_test, y_pred)
print(f"Độ chính xác của mô hình: {accuracy:.2f}")

# In báo cáo phân loại chi tiết
print("\n=== Classification Report ===")
print(classification_report(y_test, y_pred))

# In ma trận nhầm lẫn
print("\n=== Confusion Matrix ===")
print(confusion_matrix(y_test, y_pred))

