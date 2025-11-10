# app/core/file_manager.py
import os
from typing import Optional, List
from config.settings import ATTACHMENTS_DIR
from config.constants import ALLOWED_EXTENSIONS, MAX_FILE_SIZE


class FileManager:
    """文件管理器，负责处理附件的上传、下载和删除操作"""

    @staticmethod
    def save_uploaded_file(uploaded_file, test_application_number: str, filename: str) -> Optional[str]:
        """保存上传的文件"""
        if uploaded_file is not None:
            folder_name = f"{ATTACHMENTS_DIR}/{test_application_number}"
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            base_name, extension = os.path.splitext(filename)
            counter = 1
            unique_filename = filename
            file_path = os.path.join(folder_name, unique_filename)

            while os.path.exists(file_path):
                unique_filename = f"{base_name}_{counter}{extension}"
                file_path = os.path.join(folder_name, unique_filename)
                counter += 1

            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            return file_path
        return None

    @staticmethod
    def get_attachment_files(test_application_number: str) -> List[str]:
        """获取指定测试申请单的附件文件列表"""
        record_folder = f"{ATTACHMENTS_DIR}/{test_application_number}"
        if os.path.exists(record_folder):
            return os.listdir(record_folder)
        return []

    @staticmethod
    def download_attachment(test_application_number: str, filename: str) -> Optional[bytes]:
        """下载指定附件文件"""
        file_path = f"{ATTACHMENTS_DIR}/{test_application_number}/{filename}"
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                return f.read()
        return None

    @staticmethod
    def delete_attachment(test_application_number: str, filename: str) -> bool:
        """删除指定附件文件"""
        file_path = f"{ATTACHMENTS_DIR}/{test_application_number}/{filename}"
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False

    @staticmethod
    def is_valid_file_type(filename: str) -> bool:
        """检查文件类型是否有效"""
        _, extension = os.path.splitext(filename.lower())
        return extension in ALLOWED_EXTENSIONS

    @staticmethod
    def validate_uploaded_file(uploaded_file) -> tuple[bool, str]:
        """验证上传文件"""
        if uploaded_file is None:
            return True, ""

        if not FileManager.is_valid_file_type(uploaded_file.name):
            return False, "不支持的文件类型。请上传PDF、Word、Excel或图片文件。"

        if uploaded_file.size > MAX_FILE_SIZE:
            return False, "文件大小超过10MB限制。"

        return True, ""
