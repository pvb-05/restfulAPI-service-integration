from flask import Flask, jsonify, request

app = Flask(__name__)

# Giữ liệu mẫu
products = {
    "1": {"id": "1", "name": "Laptop Dell", "price": 1500, "stock": 10},
    "2": {"id": "2", "name": "Chuột Logitech", "price": 50, "stock": 0} 
}

@app.route('/api/products/<product_id>', methods=['GET'])
def get_product(product_id):
    product = products.get(product_id)
    if product:
        return jsonify(product), 200
    return jsonify({"error": "Sản phẩm không tồn tại"}), 404

@app.route('/api/products/<product_id>/stock', methods=['PUT'])
def update_stock(product_id):
    product = products.get(product_id)
    if not product:
        return jsonify({"error": "Sản phẩm không tồn tại"}), 404
        
    data = request.get_json()
    quantity_change = data.get("quantity_change", 0)
    
    if product["stock"] + quantity_change < 0:
        return jsonify({"error": "Số lượng tồn kho không đủ"}), 400
        
    product["stock"] += quantity_change
    return jsonify({"message": "Cập nhật kho thành công", "stock_remaining": product["stock"]}), 200

if __name__ == '__main__':
    app.run(port=5001)