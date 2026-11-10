from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)
PRODUCT_SERVICE_URL = "http://127.0.0.1:5001/api/products"

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)
    
    try:
        # 1. Gọi GET Product Service để kiểm tra tồn kho (có Timeout bảo vệ hệ thống)
        res = requests.get(f"{PRODUCT_SERVICE_URL}/{product_id}", timeout=3)
        
        if res.status_code == 404:
            return jsonify({"error": "Sản phẩm không tồn tại"}), 404
            
        product_data = res.json()
        if product_data["stock"] < quantity:
            return jsonify({"error": "Không đủ hàng trong kho"}), 400

        # 2. Gọi PUT Product Service để trừ kho
        update_payload = {"quantity_change": -quantity}
        update_res = requests.put(f"{PRODUCT_SERVICE_URL}/{product_id}/stock", json=update_payload, timeout=3)
        
        if update_res.status_code == 200:
            return jsonify({
                "message": "Tạo đơn hàng thành công",
                "order_details": {
                    "product": product_data["name"], 
                    "quantity": quantity, 
                    "total": product_data["price"] * quantity
                }
            }), 201
        else:
            return jsonify({"error": "Lỗi hệ thống khi cập nhật kho"}), 500

    # XỬ LÝ LỖI TRỌNG TÂM: Khi Product Service bị sập hoặc nghẽn mạng
    except requests.exceptions.RequestException:
        return jsonify({"error": "Dịch vụ kho hiện không phản hồi, vui lòng thử lại sau"}), 503

if __name__ == '__main__':
    app.run(port=5002)