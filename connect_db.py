import psycopg2

# Thông tin kết nối PostgreSQL
db_params = {
    "dbname": "student_performance_behavior",
    "user": "postgres",
    "password": "123",
    "host": "localhost",
    "port": "5432"
}

try:
    # Kết nối đến PostgreSQL
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # Thực hiện một truy vấn kiểm tra
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    print(f"Kết nối thành công! Phiên bản PostgreSQL: {db_version[0]} - Thời gian: 03:54 PM +07, Thursday, May 29, 2025")

    # Đóng kết nối
    cursor.close()
    conn.close()

except Exception as e:
    print(f"Lỗi khi kết nối: {e}")