# app/core/data_manager.py
import pandas as pd
import os
from datetime import datetime
from typing import List, Dict, Any
from config.settings import DATABASE_FILE


class DataManager:
    """数据管理器，负责处理Excel数据的读写操作"""

    @staticmethod
    def init_database():
        """初始化数据库文件"""
        if not os.path.exists(DATABASE_FILE):
            df = pd.DataFrame()
            df.to_excel(DATABASE_FILE, index=False)

    @staticmethod
    def load_data() -> List[Dict[str, Any]]:
        """从Excel文件加载数据"""
        if os.path.exists(DATABASE_FILE):
            try:
                df = pd.read_excel(DATABASE_FILE)
                return df.to_dict('records')
            except Exception as e:
                raise Exception(f"读取数据文件时出错: {str(e)}")
        return []

    @staticmethod
    def save_data(data: List[Dict[str, Any]]):
        """将数据保存到Excel文件"""
        df = pd.DataFrame(data)
        df.to_excel(DATABASE_FILE, index=False)

    @staticmethod
    def convert_date_columns(df: pd.DataFrame) -> pd.DataFrame:
        """转换日期列格式"""
        date_columns = ["申请日期", "送样日期", "测试开始日期", "预计结束日期", "出厂日期"]
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce').dt.date
        return df

    @staticmethod
    def check_duplicate_application(test_app_number: str) -> bool:
        """检查测试申请单编号是否已存在"""
        data = DataManager.load_data()
        for record in data:
            if record.get("测试申请单编号") == test_app_number:
                return True
        return False
