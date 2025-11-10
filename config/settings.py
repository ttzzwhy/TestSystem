# config/settings.py
import os

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 数据目录
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# 数据库配置
DATABASE_FILE = os.path.join(DATA_DIR, "database.xlsx")
ATTACHMENTS_DIR = os.path.join(DATA_DIR, "attachments")
os.makedirs(ATTACHMENTS_DIR, exist_ok=True)

# 应用配置
APP_CONFIG = {
    "page_title": "测试管理系统",
    "layout": "wide",
    "page_icon": "📋"
}

# 页面配置
PAGES = {
    "app/pages/home.py": "主页",
    "app/pages/new_test.py": "新测试",
    "app/pages/manage.py": "管理后台",
    "app/pages/dashboard.py": "结果汇总"
}
