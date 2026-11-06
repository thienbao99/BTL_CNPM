# KaraokeApp – Ứng dụng đặt phòng hát Karaoke

Đồ án môn Công nghệ phần mềm – Đề tài 9.

## 1. Mô tả
Ứng dụng hỗ trợ quản lý hoạt động kinh doanh karaoke:
- Quản lý phòng hát và giá thuê theo giờ.
- Đặt phòng theo ngày, khung giờ và số lượng khách.
- Không cho phép đặt trùng thời gian trên cùng một phòng.
- Giới hạn tối đa 15 khách/phòng.
- Quản lý món ăn, đồ uống và dịch vụ phát sinh.
- Lập hóa đơn gồm tiền phòng, dịch vụ và VAT 10%.
- Thống kê doanh thu theo phòng, ngày và tuần.
- Quản lý khách hàng thân thiết: đạt từ 10 lượt trong tháng được giảm 5%.
- Lưu thông tin thẻ và lịch sử áp dụng ưu đãi.

## 2. Công nghệ
- Backend: Python, Flask.
- Kiến trúc: MVC kết hợp DAO.
- ORM: Flask-SQLAlchemy.
- Cơ sở dữ liệu mặc định: SQLite.
- Giao diện: HTML, CSS, JavaScript, Bootstrap có thể bổ sung.
- Biểu đồ: Chart.js có thể tích hợp ở màn hình báo cáo.

## 3. Cấu trúc thư mục
- `models/`: Model – khai báo cấu trúc dữ liệu.
- `views/`: View – giao diện HTML (Flask được cấu hình `template_folder="views"`).
- `controllers/`: Controller – định tuyến và xử lý yêu cầu.
- `extensions.py`: khởi tạo extension SQLAlchemy.
- `dao.py`: các thao tác truy vấn/lưu dữ liệu dùng chung.
- `config.py`: cấu hình ứng dụng và cơ sở dữ liệu.
- `main.py`: tạo ứng dụng Flask và chạy chương trình.
- `static/`: CSS, JavaScript, hình ảnh.

## 4. Cài đặt trên Windows / PyCharm
Mở Terminal tại thư mục gốc `KaraokeApp`, sau đó chạy:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

Mở trình duyệt tại: http://127.0.0.1:5000

Nếu PowerShell chặn kích hoạt môi trường ảo, chạy:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

## 5. Cơ sở dữ liệu
Ứng dụng mặc định tạo file `karaoke.db` (SQLite) trong thư mục dự án khi chạy lần đầu.
Không đưa file database thật lên GitHub nếu chứa dữ liệu cá nhân.

Muốn dùng MySQL, cài `PyMySQL`, sau đó đặt biến môi trường `DATABASE_URL`, ví dụ:
`mysql+pymysql://username:password@localhost/karaoke_db`

## 6. Quy tắc nghiệp vụ cần thống nhất
1. Một phòng không thể có hai lượt đặt giao nhau về thời gian.
2. Số khách phải từ 1 đến 15.
3. Đơn giá dịch vụ được lưu tại thời điểm gọi món để hóa đơn không bị thay đổi khi bảng giá cập nhật.
4. Tiền trước VAT = tiền phòng + tiền dịch vụ.
5. VAT = 10% × tiền trước VAT.
6. Ưu đãi thành viên 5% áp dụng khi khách có ít nhất 10 lượt hát trong tháng. Nhóm cần thống nhất ưu đãi được tính trước VAT hay sau VAT; scaffold hiện để phần tính toán trong giai đoạn triển khai hóa đơn.
7. Báo cáo doanh thu cần thống nhất chỉ tính hóa đơn đã thanh toán hay gồm cả hóa đơn chưa thanh toán. Khuyến nghị chỉ tính hóa đơn đã thanh toán.

## 7. Phân chia nhóm đề xuất
- Thành viên 1: phòng hát, đặt phòng, dịch vụ.
- Thành viên 2: hóa đơn, thanh toán, báo cáo doanh thu.
- Thành viên 3: khách hàng, thẻ thành viên, tích hợp và kiểm thử.

## 8. Trạng thái
Đây là bộ khung MVC ban đầu. Các màn hình và model đã được tạo để nhóm tiếp tục hoàn thiện nghiệp vụ, kiểm tra dữ liệu đầu vào, phân quyền và kiểm thử.
