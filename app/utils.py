# app/utils.py
import streamlit as st
import pandas as pd

def validate_required_fields(fields):
    """验证必填字段"""
    required_fields = {
        "项目编号": fields["项目编号"],
        "测试申请单编号": fields["测试申请单编号"],
        "测试申请单飞书审批编号": fields["测试申请单飞书审批编号"],
        "申请人": fields["申请人"],
        "申请部门": fields["申请部门"],
        "申请日期": fields["申请日期"],
        "测试项目概述": fields["测试项目概述"],
        "型号": fields["型号"],
        "容量": fields["容量"],
        "数量": fields["数量"],
        "辅材/工装": fields["辅材/工装"],
        "送样日期": fields["送样日期"],
        "预计时长/天": fields["预计时长/天"],
    }

    missing_fields = [field_name for field_name, field_value in required_fields.items()
                      if not field_value or (isinstance(field_value, (int, float)) and field_value == 0)]
    return missing_fields

def show_success_message(message):
    """显示成功消息"""
    st.success(message)
    st.balloons()

def show_error_message(message):
    """显示错误消息"""
    st.error(message)
    st.snow()

@st.cache_data
def load_data_cached():
    """缓存版本的数据加载函数"""
    from app.core.data_manager import DataManager
    return DataManager.load_data()
