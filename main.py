# main.py
import streamlit as st
import os
import sys

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from config.settings import APP_CONFIG, PAGES

st.set_page_config(**APP_CONFIG)

pages = []
for file_path, title in PAGES.items():
    if os.path.exists(file_path):
        pages.append(st.Page(file_path, title=title))
    else:
        st.error(f"页面文件不存在: {file_path}")

if pages:
    pg = st.navigation(pages=pages)
    pg.run()
else:
    st.error("没有找到有效的页面文件")
