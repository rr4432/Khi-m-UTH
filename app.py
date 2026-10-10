from flask import Flask, render_template, request, jsonify
import pandas as pd
import json

app = Flask(__name__)

# ==================== HOME ROUTES ====================
@app.route('/')
def home():
    """Trang chủ - Hiển thị danh sách nhà hoặc tìm kiếm"""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """API tìm kiếm nhà"""
    data = request.get_json()
    location = data.get('location', '')
    price_min = data.get('price_min', 0)
    price_max = data.get('price_max', float('inf'))
    
    # TODO: Kết nối với database hoặc file dữ liệu
    # Ví dụ với CSV
    # df = pd.read_csv('data/houses.csv')
    # results = df[(df['location'] == location) & 
    #              (df['price'] >= price_min) & 
    #              (df['price'] <= price_max)]
    # return jsonify(results.to_dict(orient='records'))
    
    return jsonify({'message': 'Chưa cấu hình dữ liệu'})

@app.route('/price-prediction', methods=['POST'])
def predict_price():
    """API dự báo giá nhà"""
    data = request.get_json()
    # TODO: Implement ML model để dự báo giá
    # Có thể dùng scikit-learn, xgboost, v.v.
    return jsonify({'predicted_price': 'TBD'})

@app.route('/houses')
def get_houses():
    """API lấy danh sách tất cả nhà"""
    # TODO: Lấy từ database hoặc CSV
    return jsonify({'houses': []})

# ==================== ERROR HANDLERS ====================
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Không tìm thấy'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Lỗi server'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
