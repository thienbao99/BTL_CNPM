"""Các hàm truy vấn dùng chung. Nghiệp vụ cụ thể đặt trong controller/service."""
from extensions import db

def commit():
    """Lưu các thay đổi đang chờ vào cơ sở dữ liệu."""
    db.session.commit()

def rollback():
    """Hủy các thay đổi nếu xảy ra lỗi."""
    db.session.rollback()
