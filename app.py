from flask import Flask, render_template, request, jsonify
import csv
from pathlib import Path

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / 'data' / 'houses.csv'


def get_sample_houses():
    return [
        {
            'id': 1,
            'title': 'Căn hộ cao cấp Quận 7',
            'location': 'Quận 7',
            'price': 2850000000,
            'bedrooms': 3,
            'bathrooms': 2,
            'area': 110,
            'property_type': 'Apartment',
            'image_url': 'https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&fit=crop&w=900&q=80',
            'description': 'Căn hộ hiện đại, view thành phố, gần trung tâm thương mại.'
        },
        {
            'id': 2,
            'title': 'Biệt thự gia đình Phú Mỹ Hưng',
            'location': 'Phú Mỹ Hưng',
            'price': 5200000000,
            'bedrooms': 4,
            'bathrooms': 3,
            'area': 220,
            'property_type': 'Villa',
            'image_url': 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=900&q=80',
            'description': 'Biệt thự 2 tầng, sân vườn rộng, phù hợp gia đình.'
        },
        {
            'id': 3,
            'title': 'Nhà phố Thủ Đức',
            'location': 'Thủ Đức',
            'price': 3900000000,
            'bedrooms': 3,
            'bathrooms': 2,
            'area': 150,
            'property_type': 'Townhouse',
            'image_url': 'https://images.unsplash.com/photo-1568605114967-8130f3a36994?auto=format&fit=crop&w=900&q=80',
            'description': 'Nhà phố tiện ích, nhiều không gian, giao thông thuận tiện.'
        },
        {
            'id': 4,
            'title': 'Chung cư trung tâm Hà Nội',
            'location': 'Hà Nội',
            'price': 2100000000,
            'bedrooms': 2,
            'bathrooms': 1,
            'area': 80,
            'property_type': 'Apartment',
            'image_url': 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=900&q=80',
            'description': 'Căn hộ nhỏ hiện đại, gần chợ và trường học.'
        },
        {
            'id': 5,
            'title': 'Nhà ở mới Bình Dương',
            'location': 'Bình Dương',
            'price': 2600000000,
            'bedrooms': 3,
            'bathrooms': 2,
            'area': 130,
            'property_type': 'House',
            'image_url': 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=900&q=80',
            'description': 'Nhà xây mới, nội thất đẹp, an ninh tốt.'
        },
        {
            'id': 6,
            'title': 'Đất nền khu dân cư',
            'location': 'Đà Nẵng',
            'price': 1800000000,
            'bedrooms': 0,
            'bathrooms': 0,
            'area': 200,
            'property_type': 'Land',
            'image_url': 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=900&q=80',
            'description': 'Đất nền phù hợp xây nhà hoặc đầu tư.'
        }
    ]


def load_houses():
    if not DATA_FILE.exists():
        return get_sample_houses()

    with DATA_FILE.open('r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        houses = []
        for row in reader:
            row['price'] = int(row.get('price', 0))
            row['bedrooms'] = int(row.get('bedrooms', 0))
            row['bathrooms'] = int(row.get('bathrooms', 0))
            row['area'] = int(row.get('area', 0))
            houses.append(row)
        return houses or get_sample_houses()


def filter_houses(houses, location=None, min_price=0, max_price=999999999999, bedrooms=0, property_type='all'):
    result = []
    for h in houses:
        if location and location.lower() not in str(h.get('location', '')).lower():
            continue
        if int(h.get('price', 0)) < int(min_price):
            continue
        if int(h.get('price', 0)) > int(max_price):
            continue
        if int(h.get('bedrooms', 0)) < int(bedrooms):
            continue
        if property_type != 'all' and str(h.get('property_type', '')).lower() != property_type.lower():
            continue
        result.append(h)
    return result


@app.route('/')
def home():
    location = request.args.get('location', '').strip()
    min_price = request.args.get('min_price', 0, type=int)
    max_price = request.args.get('max_price', 999999999999, type=int)
    bedrooms = request.args.get('bedrooms', 0, type=int)
    property_type = request.args.get('property_type', 'all')

    houses = load_houses()
    filtered = filter_houses(houses, location, min_price, max_price, bedrooms, property_type)

    return render_template(
        'index.html',
        houses=filtered,
        filters={
            'location': location,
            'min_price': min_price,
            'max_price': max_price,
            'bedrooms': bedrooms,
            'property_type': property_type,
        },
    )


@app.route('/api/properties')
def api_properties():
    houses = load_houses()
    return jsonify({'count': len(houses), 'houses': houses})


@app.route('/api/search')
def api_search():
    location = request.args.get('location', '').strip()
    min_price = request.args.get('min_price', 0, type=int)
    max_price = request.args.get('max_price', 999999999999, type=int)
    bedrooms = request.args.get('bedrooms', 0, type=int)
    property_type = request.args.get('property_type', 'all')

    houses = filter_houses(load_houses(), location, min_price, max_price, bedrooms, property_type)
    return jsonify({'count': len(houses), 'houses': houses})


@app.route('/health')
def health():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
