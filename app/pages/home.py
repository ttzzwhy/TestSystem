# home.py
import streamlit as st

st.set_page_config(page_title="测试管理系统", page_icon="📋")

st.title("Welcome")
st.markdown("""
    <div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px; border-left: 5px solid #4CAF50;">
        <h3>📘 系统介绍</h3>
        <p>本系统用于测试数据管理，请根据提示进行操作。</p>
        <ul>
            <li>📝 <strong>新测试</strong> - 创建新的测试申请</li>
            <li>⚙️ <strong>管理后台</strong> - 编辑和管理现有数据</li>
            <li>📊 <strong>结果汇总</strong> - 数据分析和可视化</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

st.info("请选择左侧导航栏中的功能模块开始使用系统")
