from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# PostgreSQL Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://user:password@localhost:5432/flask_crud_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class Item(db.Model):
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# Create tables
with app.app_context():
    db.create_all()

# Frontend Route
@app.route("/")
def home():
    return render_template('index.html')

# Health Check
@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "health": "healthy",
        "timestamp": datetime.now().isoformat()
    }), 200

# CRUD API Routes

# CREATE - Add new item
@app.route("/api/items", methods=['POST'])
def create_item():
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({"error": "Name is required"}), 400
    
    try:
        item = Item(
            name=data.get('name'),
            description=data.get('description', '')
        )
        db.session.add(item)
        db.session.commit()
        return jsonify(item.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# READ - Get all items
@app.route("/api/items", methods=['GET'])
def get_items():
    try:
        items = Item.query.all()
        return jsonify([item.to_dict() for item in items]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# READ - Get single item
@app.route("/api/items/<int:item_id>", methods=['GET'])
def get_item(item_id):
    try:
        item = Item.query.get(item_id)
        if not item:
            return jsonify({"error": "Item not found"}), 404
        return jsonify(item.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# UPDATE - Modify item
@app.route("/api/items/<int:item_id>", methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    
    try:
        item = Item.query.get(item_id)
        if not item:
            return jsonify({"error": "Item not found"}), 404
        
        item.name = data.get('name', item.name)
        item.description = data.get('description', item.description)
        db.session.commit()
        return jsonify(item.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# DELETE - Remove item
@app.route("/api/items/<int:item_id>", methods=['DELETE'])
def delete_item(item_id):
    try:
        item = Item.query.get(item_id)
        if not item:
            return jsonify({"error": "Item not found"}), 404
        
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    