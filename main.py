import streamlit as st
from streamlit_option_menu import option_menu
import os
from dotenv import load_dotenv
import sys
#sys.path.append(r"D:\MINI_Project\DoAn3\predict_train_RanDomForest")
sys.path.append(r"D:\MINI_Project\DoAn3\perdict_train_XGBoost")  # đường dẫn chứa predict_app.py
sys.path.append(r"D:\MINI_Project\DoAn3\CatBoost") 
#from predict_train_RanDomForest import predict_app
from perdict_train_XGBoost import app_catboost, DuDoanDiemTuongLai_Grade

import home, DashBoard_App, DuDoanDiemTuongLai_Grade, app_catboost , account  # đảm bảo 2 file này tồn tại và có hàm app()

# Load biến môi trường từ .env
load_dotenv()

# Cấu hình tiêu đề trang
st.set_page_config(page_title="🎓 Student Performance", layout="wide")

# Thêm Google Analytics (nếu có)
analytics_tag = os.getenv('analytics_tag')
if analytics_tag:
    st.markdown(
        f"""
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id={analytics_tag}"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments);}}
            gtag('js', new Date());
            gtag('config', '{analytics_tag}');
        </script>
        """,
        unsafe_allow_html=True
    )
    print(f"Analytics Tag: {analytics_tag}")
else:
    print("❌ analytics_tag chưa được khai báo trong .env")


# Class để điều hướng giữa các app nhỏ
class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({"title": title, "function": func})

    def run(self):
        with st.sidebar:
            app = option_menu(
                menu_title="📚 Menu",
                options=["Home", "Dashboard","DuDoanDiemTuongLai_Grade","predict student performance use CatBoost","account"],
                icons=["house-fill", "bar-chart-line-fill","trophy-fill","trophy-fill","person-circle"],
                menu_icon="chat-text-fill",
                default_index=0,
                styles={
                    "container": {"padding": "5!important", "background-color": "#000000"},
                    "icon": {"color": "white", "font-size": "23px"},
                    "nav-link": {
                        "color": "white",
                        "font-size": "20px",
                        "text-align": "left",
                        "margin": "0px",
                        "--hover-color": "#6c63ff"
                    },
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )

        # Điều hướng đến các module tương ứng
        if app == "Home":
            home.app()
        if app == "Dashboard":
            DashBoard_App.app()
        if app == "DuDoanDiemTuongLai_Grade":
            DuDoanDiemTuongLai_Grade.app()
        if app == "predict student performance use CatBoost":
            app_catboost.app()    
        if app == "account":
            account.app()
        


# Chạy ứng dụng
app = MultiApp()
app.add_app("Home", home.app)
app.add_app("Dashboard", DashBoard_App.app)
app.add_app("DuDoanDiemTuongLai_Grade",DuDoanDiemTuongLai_Grade.app)
app.add_app("predict student performance use CatBoost",app_catboost.app )
app.add_app("account", account.app)
    
app.run()
