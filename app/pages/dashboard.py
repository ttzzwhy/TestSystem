# app/pages/dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from app.core.data_manager import DataManager


def load_data():
    """读取数据"""
    try:
        return DataManager.load_data()
    except Exception as e:
        st.error(f"读取数据文件时出错: {str(e)}")
        return []


def preprocess_data(data):
    """预处理数据，转换日期列"""
    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data)
    date_columns = ["申请日期", "送样日期", "测试开始日期", "预计结束日期", "出厂日期"]
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df


# 主页面
st.set_page_config(page_title="数据分析看板", layout="wide")
st.title("Summary")

# 加载数据
raw_data = load_data()
df = preprocess_data(raw_data)

if df.empty:
    st.info("暂无数据，请先添加测试项目数据")
else:
    # 侧边栏筛选器
    st.sidebar.header("筛选器")

    # 按申请部门筛选
    departments = df["申请部门"].dropna().unique().tolist() if "申请部门" in df.columns else []
    selected_departments = st.sidebar.multiselect("申请部门", departments, default=departments)

    # 按测试进度筛选
    progress_options = df["测试进度"].dropna().unique().tolist() if "测试进度" in df.columns else []
    selected_progress = st.sidebar.multiselect("测试进度", progress_options, default=progress_options)

    # 按日期范围筛选
    if "申请日期" in df.columns:
        min_date = df["申请日期"].min()
        max_date = df["申请日期"].max()
        if pd.notna(min_date) and pd.notna(max_date):
            date_range = st.sidebar.date_input(
                "申请日期范围",
                value=(min_date.date(), max_date.date()),
                min_value=min_date.date(),
                max_value=max_date.date()
            )
        else:
            date_range = None
    else:
        date_range = None

    # 应用筛选器
    filtered_df = df.copy()
    if selected_departments:
        filtered_df = filtered_df[filtered_df["申请部门"].isin(selected_departments)]
    if selected_progress:
        filtered_df = filtered_df[filtered_df["测试进度"].isin(selected_progress)]
    if date_range and len(date_range) == 2 and "申请日期" in filtered_df.columns:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df["申请日期"] >= pd.Timestamp(start_date)) &
            (filtered_df["申请日期"] <= pd.Timestamp(end_date))
            ]

    # 显示筛选后的数据概览
    st.subheader("数据概览")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("总项目数", len(filtered_df))
    col2.metric("进行中项目",
                len(filtered_df[filtered_df["测试进度"] == "进行中"]) if "测试进度" in filtered_df.columns else 0)
    col3.metric("已完成项目",
                len(filtered_df[filtered_df["测试进度"] == "已完成"]) if "测试进度" in filtered_df.columns else 0)
    col4.metric("总预计费用", f"¥{filtered_df['预计费用'].sum():,.2f}" if "预计费用" in filtered_df.columns else "N/A")

    # 可视化配置
    st.subheader("数据可视化")

    # 图表类型选择
    chart_type = st.selectbox(
        "选择图表类型",
        ["柱状图", "折线图", "饼图", "散点图", "面积图"]
    )

    # X轴和Y轴选择（根据图表类型动态调整）
    numeric_columns = filtered_df.select_dtypes(include=['number']).columns.tolist()
    date_columns = filtered_df.select_dtypes(include=['datetime']).columns.tolist()
    categorical_columns = filtered_df.select_dtypes(include=['object']).columns.tolist()

    all_columns = numeric_columns + date_columns + categorical_columns

    if chart_type in ["柱状图", "折线图", "散点图", "面积图"]:
        col_x = st.selectbox("选择X轴", all_columns, index=0 if all_columns else 0)
        col_y = st.selectbox("选择Y轴", numeric_columns, index=0 if numeric_columns else 0)
        color_col = st.selectbox("颜色分类（可选）", ["无"] + categorical_columns, index=0)
    elif chart_type == "饼图":
        col_x = st.selectbox("选择分类维度", categorical_columns, index=0 if categorical_columns else 0)
        col_y = st.selectbox("选择数值维度", numeric_columns, index=0 if numeric_columns else 0)

    # 生成图表
    if chart_type in ["柱状图", "折线图", "散点图", "面积图"] and col_x and col_y:
        if chart_type == "柱状图":
            if color_col != "无":
                fig = px.bar(filtered_df, x=col_x, y=col_y, color=color_col, title=f"{col_y} 按 {col_x} 分组")
            else:
                fig = px.bar(filtered_df, x=col_x, y=col_y, title=f"{col_y} 按 {col_x} 分组")
        elif chart_type == "折线图":
            if color_col != "无":
                fig = px.line(filtered_df, x=col_x, y=col_y, color=color_col, title=f"{col_y} 趋势图")
            else:
                fig = px.line(filtered_df, x=col_x, y=col_y, title=f"{col_y} 趋势图")
        elif chart_type == "散点图":
            if color_col != "无":
                fig = px.scatter(filtered_df, x=col_x, y=col_y, color=color_col, title=f"{col_y} vs {col_x}")
            else:
                fig = px.scatter(filtered_df, x=col_x, y=col_y, title=f"{col_y} vs {col_x}")
        elif chart_type == "面积图":
            if color_col != "无":
                fig = px.area(filtered_df, x=col_x, y=col_y, color=color_col, title=f"{col_y} 面积图")
            else:
                fig = px.area(filtered_df, x=col_x, y=col_y, title=f"{col_y} 面积图")

        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "饼图" and col_x and col_y:
        grouped_data = filtered_df.groupby(col_x)[col_y].sum().reset_index()
        fig = px.pie(grouped_data, values=col_y, names=col_x, title=f"{col_y} 按 {col_x} 分布")
        st.plotly_chart(fig, use_container_width=True)

    # 统计分析
    st.subheader("统计分析")

    # 测试进度分布
    if "测试进度" in filtered_df.columns:
        st.write("### 测试进度分布")
        progress_counts = filtered_df["测试进度"].value_counts()
        fig_progress = px.pie(values=progress_counts.values, names=progress_counts.index,
                              title="测试进度分布")
        st.plotly_chart(fig_progress, use_container_width=True)

    # 预计费用趋势（如果有申请日期）
    if "申请日期" in filtered_df.columns and "预计费用" in filtered_df.columns:
        st.write("### 预计费用趋势")
        cost_trend = filtered_df.groupby(filtered_df["申请日期"].dt.date)["预计费用"].sum().reset_index()
        fig_cost = px.line(cost_trend, x="申请日期", y="预计费用", title="预计费用时间趋势")
        st.plotly_chart(fig_cost, use_container_width=True)

    # 申请部门项目数量
    if "申请部门" in filtered_df.columns:
        st.write("### 各部门项目数量")
        dept_counts = filtered_df["申请部门"].value_counts()
        fig_dept = px.bar(x=dept_counts.index, y=dept_counts.values,
                          labels={'x': '申请部门', 'y': '项目数量'},
                          title="各部门项目数量")
        st.plotly_chart(fig_dept, use_container_width=True)

    # 数据表格
    st.subheader("详细数据")
    st.dataframe(filtered_df, use_container_width=True)
