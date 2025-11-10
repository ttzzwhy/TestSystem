# app/pages/new_test.py
import streamlit as st
import pandas as pd
from datetime import datetime
from app.core.data_manager import DataManager
from app.core.file_manager import FileManager
from config.constants import DEPARTMENTS, TEST_PROGRESS
from app import utils

# 初始化数据
DataManager.init_database()

st.title("New Application")
st.markdown(
    """
    有新的委外测试时请填写以下内容，其中必填项如下：
    :rainbow[项目编号, 测试申请单编号, 测试申请单飞书审批编号, 申请人, 测试项目概述, 型号, 容量, 数量, 辅材/工装, 预计时长/天]
    """)

with st.form("new_test"):
    column1, column2, column3 = st.columns(3)
    program = column1.text_input("项目编号")
    test_application = column2.text_input("测试申请单编号")
    test_application_approval = column3.number_input("测试申请单飞书审批编号", step=1)
    applicant = column1.text_input("申请人")
    application_department = column2.selectbox("申请部门", DEPARTMENTS)
    application_date = column3.date_input("申请日期")
    test_project_summary = column1.text_input("测试项目概述")
    model = column2.text_input("型号")
    capacity = column3.number_input("容量", step=0.01)
    number = column1.number_input("数量", step=1)
    auxiliary_materials = column2.text_input("辅材/工装")
    expected_duration = column3.number_input("预计时长/天", step=1)
    sample_date = column1.date_input("到样日期")
    test_start_date = column2.date_input("测试开始日期")
    expected_end_date = column3.date_input("预计结束日期")
    test_progress = column1.selectbox("测试进度", TEST_PROGRESS)
    cost_center = column2.text_input("成本中心")
    purchase_application_approval = column3.number_input("采购申请单飞书审批编号", step=1)
    expected_cost = column1.number_input("预计费用", step=0.01)
    supplier = column2.text_input("供应商")
    out_of_date = column3.date_input("出厂日期")
    quote = column1.file_uploader("报价单")
    test_data_report = column2.file_uploader("测试数据/报告")
    settlement_bill = column3.file_uploader("结算单")

    if st.form_submit_button("保存"):
        # 检查测试申请单编号是否重复
        if DataManager.check_duplicate_application(test_application):
            st.error(f"测试申请单编号 '{test_application}' 已存在，请使用不同的编号")
        else:
            required_fields = {
                "项目编号": program,
                "测试申请单编号": test_application,
                "测试申请单飞书审批编号": test_application_approval,
                "申请人": applicant,
                "申请部门": application_department,
                "申请日期": str(application_date),
                "测试项目概述": test_project_summary,
                "型号": model,
                "容量": capacity,
                "数量": number,
                "辅材/工装": auxiliary_materials,
                "送样日期": str(sample_date),
                "预计时长/天": expected_duration,
            }

            missing_fields = utils.validate_required_fields(required_fields)
            if missing_fields:
                st.error(f"缺少以下必填字段：{', '.join(missing_fields)}")
            else:
                # 验证上传文件
                files_valid = True
                error_messages = []

                is_valid, error_msg = FileManager.validate_uploaded_file(quote)
                if not is_valid:
                    files_valid = False
                    error_messages.append(f"报价单: {error_msg}")

                is_valid, error_msg = FileManager.validate_uploaded_file(test_data_report)
                if not is_valid:
                    files_valid = False
                    error_messages.append(f"测试数据/报告: {error_msg}")

                is_valid, error_msg = FileManager.validate_uploaded_file(settlement_bill)
                if not is_valid:
                    files_valid = False
                    error_messages.append(f"结算单: {error_msg}")

                if not files_valid:
                    st.error("文件验证失败:\n" + "\n".join(error_messages))
                else:
                    new_record = {
                        "项目编号": program,
                        "测试申请单编号": test_application,
                        "测试申请单飞书审批编号": test_application_approval,
                        "申请人": applicant,
                        "申请部门": application_department,
                        "申请日期": str(application_date),
                        "测试项目概述": test_project_summary,
                        "型号": model,
                        "容量": capacity,
                        "数量": number,
                        "辅材/工装": auxiliary_materials,
                        "送样日期": str(sample_date),
                        "预计时长/天": expected_duration,
                        "测试开始日期": str(test_start_date),
                        "预计结束日期": str(expected_end_date),
                        "测试进度": test_progress,
                        "成本中心": cost_center,
                        "采购申请单飞书审批编号": purchase_application_approval,
                        "预计费用": expected_cost,
                        "供应商": supplier,
                        "出厂日期": str(out_of_date),
                        "报价单": None,
                        "测试数据/报告": None,
                        "结算单": None
                    }

                    # 保存记录到Excel
                    data = DataManager.load_data()
                    data.append(new_record)

                    # 保存上传的文件
                    if quote:
                        file_path = FileManager.save_uploaded_file(quote, test_application, quote.name)
                        new_record["报价单"] = file_path

                    if test_data_report:
                        file_path = FileManager.save_uploaded_file(test_data_report, test_application, test_data_report.name)
                        new_record["测试数据/报告"] = file_path

                    if settlement_bill:
                        file_path = FileManager.save_uploaded_file(settlement_bill, test_application, settlement_bill.name)
                        new_record["结算单"] = file_path

                    # 更新记录中的文件路径并保存到Excel
                    data[-1] = new_record
                    DataManager.save_data(data)

                    utils.show_success_message("数据保存成功！")
                    st.rerun()

