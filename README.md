# 🛒 Tích hợp dịch vụ RESTful API

## 📖 Giới thiệu

Dự án minh họa cách tích hợp các dịch vụ RESTful trong một quy trình đặt hàng đơn giản. `Order Service` giao tiếp với `Product Service` qua HTTP để kiểm tra thông tin và tồn kho sản phẩm, sau đó cập nhật số lượng khi đơn hàng được tạo.

Mục tiêu là trình bày cách phối hợp các dịch vụ độc lập, xử lý lỗi nghiệp vụ và phản hồi khi dịch vụ phụ thuộc không khả dụng. Dữ liệu sản phẩm hiện được lưu trong bộ nhớ để phục vụ mục đích minh họa; dữ liệu sẽ được khởi tạo lại khi dịch vụ khởi động lại.

## ✨ Chức năng chính

- **Tra cứu sản phẩm:** lấy thông tin sản phẩm theo mã; trả về `404` nếu không tìm thấy.
- **Cập nhật tồn kho:** điều chỉnh số lượng tồn kho và từ chối yêu cầu khiến số lượng âm.
- **Tạo đơn hàng:** kiểm tra sản phẩm và tồn kho, trừ kho khi đủ hàng, sau đó trả về thông tin đơn hàng và tổng tiền.
- **Xử lý lỗi tích hợp:** giới hạn thời gian chờ khi gọi dịch vụ kho và trả về `503` nếu dịch vụ không phản hồi.
- **Giao diện demo:** trang HTML cho phép chọn sản phẩm, nhập số lượng và gửi yêu cầu đặt hàng.
- **Kịch bản kiểm thử thủ công:** minh họa các trường hợp đặt hàng thành công, hết hàng và dịch vụ phụ thuộc không khả dụng.

## 🧰 Công nghệ sử dụng

- **Python** — ngôn ngữ triển khai các dịch vụ phía máy chủ.
- **Flask** — xây dựng HTTP API.
- **Flask-CORS** — bật CORS cho Order Service để giao diện demo có thể gọi API.
- **Requests** — gọi Product Service từ Order Service.
- **HTML, CSS và JavaScript** — giao diện demo không sử dụng framework frontend.

## 🗂️ Cấu trúc dự án

```text
.
├── frontend/
│   └── index.html             # Giao diện demo đặt hàng
├── reports/
│   └── baocao.docx            # Báo cáo dự án
├── slides/
│   ├── script.docx            # Kịch bản thuyết trình
│   └── slide.pptx             # Slide trình bày
├── src/
│   ├── order_service.py       # API tạo đơn hàng, cổng 5002
│   └── product_service.py     # API sản phẩm và tồn kho, cổng 5001
├── test/
│   ├── test_case.txt          # Các kịch bản kiểm thử thủ công
│   ├── success.png            # Ảnh minh họa đặt hàng thành công
│   ├── badrequest.png         # Ảnh minh họa lỗi yêu cầu
│   └── unavailable.png        # Ảnh minh họa dịch vụ không khả dụng
├── requirements.txt           # Danh sách các gói Python
├── sequence_diagram.png       # Sơ đồ tuần tự
└── README.md
```

## ⚙️ Cài đặt

### Yêu cầu

- Python 3.9 trở lên.
- `pip`.

### Thiết lập môi trường

```bash
git clone https://github.com/pvb-05/restfulAPI-service-integration.git
cd restfulAPI-service-integration

python -m venv .venv
```

Kích hoạt môi trường ảo:

```bash
# Linux / macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Cài các thư viện cần cho hai dịch vụ:

```bash
pip install Flask flask-cors requests
```

> `requirements.txt` hiện chứa nhiều gói ngoài phạm vi chạy hai dịch vụ này và chưa liệt kê `requests`. Nếu cần cài theo danh sách của repository, hãy cài thêm `requests` sau khi chạy `pip install -r requirements.txt`.

## 🚀 Chạy và sử dụng

Mở hai terminal riêng, kích hoạt cùng môi trường ảo trong mỗi terminal và chạy dịch vụ theo thứ tự sau.

**Terminal 1 — Product Service:**

```bash
python src/product_service.py
```

Dịch vụ lắng nghe tại `http://127.0.0.1:5001`.

**Terminal 2 — Order Service:**

```bash
python src/order_service.py
```

Dịch vụ lắng nghe tại `http://127.0.0.1:5002`.

### API có sẵn

| Phương thức | Endpoint | Mô tả |
|---|---|---|
| `GET` | `/api/products/<product_id>` | Lấy thông tin sản phẩm và tồn kho. |
| `PUT` | `/api/products/<product_id>/stock` | Điều chỉnh tồn kho bằng `quantity_change`. |
| `POST` | `/api/orders` | Tạo đơn hàng và trừ tồn kho tương ứng. |

Ví dụ tạo đơn hàng cho hai sản phẩm có mã `1`:

```bash
curl -X POST http://127.0.0.1:5002/api/orders \
  -H "Content-Type: application/json" \
  -d '{"product_id":"1","quantity":2}'
```

Yêu cầu hợp lệ trả về `201 Created` cùng thông tin sản phẩm, số lượng và tổng tiền. Dữ liệu mẫu ban đầu gồm sản phẩm mã `1` (Laptop Dell, tồn kho 10) và mã `2` (Chuột Logitech, tồn kho 0). Có thể chạy các kịch bản trong `test/test_case.txt` để kiểm tra hành vi thành công, hết hàng và timeout.

### Giao diện demo

Sau khi khởi động cả hai dịch vụ, mở `frontend/index.html` trong trình duyệt và gửi yêu cầu đặt hàng. Giao diện gọi Order Service tại `http://127.0.0.1:5002`.

## 👤 Tác giả

**pvb-05** — [Trang GitHub](https://github.com/pvb-05).

## 📚 Tài liệu tham khảo và giấy phép

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Requests Documentation](https://requests.readthedocs.io/)
- [Sơ đồ tuần tự](sequence_diagram.png)
- [Báo cáo dự án](reports/baocao.docx)
- Repository hiện **chưa khai báo giấy phép**. Vui lòng liên hệ tác giả trước khi sử dụng hoặc phân phối lại theo điều khoản cấp phép cụ thể.
