from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return jsonify(bakeries), 200

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    if bakery:
        return jsonify(bakery.to_dict()), 200
    else:
        return jsonify({'error': 'Bakery not found'}), 404

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [baked_good.to_dict() for baked_good in baked_goods_by_price]
    return jsonify(baked_goods_by_price_serialized), 200

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if most_expensive:
        return jsonify(most_expensive.to_dict()), 200
    else:
        return jsonify({'error': 'No baked goods found'}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)
