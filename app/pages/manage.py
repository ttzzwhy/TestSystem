# app/pages/manage.py
import streamlit as st
import pandas as pd
import io
from app.core.data_manager import DataManager
from app.core.file_manager import FileManager
from config.constants import DEPARTMENTS, TEST_PROGRESS

def show_success_message(message):
    """显示成功消息"""
    st.success(message)
    st.balloons()

def show_error_message(message):
    """显示错误消息"""
    st.error(message)
    st.snow()

def search_data(data, search_term):
    """搜索数据"""
    if not search_term:
        return data

    filtered_data = []
    search_term = search_term.lower()

    for record in data:
        for value in record.values():
            if isinstance(value, str) and search_term in value.lower():
                filtered_data.append(record)
                break
            elif isinstance(value, (int, float)) and search_term in str(value):
                filtered_data.append(record)
                break

    return filtered_data

# 初始化数据
DataManager.init_database()
st.title("Update Application")

# 加载数据
data = DataManager.load_data()

# 在显示数据前添加搜索框
search_term = st.text_input("搜索数据", "")
if search_term:
    data = search_data(data, search_term)
    st.info(f"找到 {len(data)} 条匹配记录")

# 使用data_editor进行数据管理
if data:
    df = pd.DataFrame(data)

    # 转换日期列格式
    df = DataManager.convert_date_columns(df)

    # 添加索引列以便识别记录
    df_with_index = df.reset_index()
    df_with_index.rename(columns={'index': '记录ID'}, inplace=True)

    st.subheader("编辑数据")
    edited_df = st.data_editor(
        df_with_index,
        use_container_width=True,
        num_rows="dynamic",
        hide_index=True,
        column_config={
            "申请部门": st.column_config.SelectboxColumn(
                "申请部门",
                options=DEPARTMENTS
            ),
            "测试进度": st.column_config.SelectboxColumn(
                "测试进度",
                options=TEST_PROGRESS
            ),
            "申请日期": st.column_config.DateColumn("申请日期"),
            "送样日期": st.column_config.DateColumn("送样日期"),
            "测试开始日期": st.column_config.DateColumn("测试开始日期"),
            "预计结束日期": st.column_config.DateColumn("预计结束日期"),
            "出厂日期": st.column_config.DateColumn("出厂日期"),
        }
    )

    # 显示附件信息
    st.subheader("附件信息")
    for idx, record in enumerate(data):
        # 获取测试申请单编号
        test_application_number = record.get("测试申请单编号")
        if test_application_number:
            # 检查该测试申请单是否有附件
            attachment_files = FileManager.get_attachment_files(test_application_number)

            if attachment_files:
                with st.expander(f"记录 {idx} ({test_application_number}) 的附件"):
                    for filename in attachment_files:
                        file_data = FileManager.download_attachment(test_application_number, filename)
                        if file_data:
                            st.download_button(
                                label=f"下载附件: {filename}",
                                data=file_data,
                                file_name=filename,
                                key=f"download_{idx}_{filename}"
                            )
                        else:
                            st.warning(f"附件: {filename} (文件未找到)")

    # 保存更改
    if st.button("保存更改"):
        # 移除索引列
        updated_df = edited_df.drop(columns=['记录ID'])

        # 将日期对象转换回字符串格式以便保存
        date_columns = ["申请日期", "送样日期", "测试开始日期", "预计结束日期", "出厂日期"]
        for col in date_columns:
            if col in updated_df.columns:
                updated_df[col] = updated_df[col].apply(
                    lambda x: x.strftime('%Y-%m-%d') if pd.notna(x) else ""
                )

        updated_data = updated_df.to_dict('records')
        DataManager.save_data(updated_data)
        show_success_message("数据已保存")
        st.rerun()

else:
    st.info("暂无测试数据")

# 导出数据功能
st.subheader("数据导出")

if st.button("导出为Excel"):
    if data:
        df = pd.DataFrame(data)
        # 创建字节流缓冲区
        excel_buffer = io.BytesIO()
        # 导出为Excel格式
        df.to_excel(excel_buffer, index=False, engine='openpyxl')
        excel_buffer.seek(0)

        st.download_button(
            label="下载Excel文件",
            data=excel_buffer,
            file_name="test_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
