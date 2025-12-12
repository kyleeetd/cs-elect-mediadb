from flask import Flask, jsonify, request
import mysql.connector
import json

app = Flask(__name__)

# Simple database
def get_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root", 
        password="root",
        database="media_db"
    )

@app.route('/')
def home():
    return "🎬 Media API - Use /media"

# 1. GET ALL
@app.route('/media', methods=['GET'])
def get_all():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM media_library")
    media = cursor.fetchall()
    db.close()
    
    return jsonify({
        "message": f"Found {len(media)} movies",
        "data": media
    })

# 2. GET ONE
@app.route('/media/<int:id>', methods=['GET'])
def get_one(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM media_library WHERE media_id = %s", (id,))
    media = cursor.fetchone()
    db.close()
    
    if media:
        return jsonify({"success": True, "data": media})
    else:
        return jsonify({"error": "Not found"}), 404

# 3. CREATE
@app.route('/media', methods=['POST'])
def create():
    data = request.json
    
    if not data or 'title' not in data:
        return jsonify({"error": "Need title"}), 400
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO media_library (title, duration, rating, media_type)
        VALUES (%s, %s, %s, %s)
    """, (
        data.get('title'),
        data.get('duration', 0),
        data.get('rating', 5),
        data.get('media_type', 'Movie')
    ))
    
    db.commit()
    new_id = cursor.lastrowid
    db.close()
    
    return jsonify({"success": True, "id": new_id}), 201

# 4. DELETE
@app.route('/media/<int:id>', methods=['DELETE'])
def delete(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM media_library WHERE media_id = %s", (id,))
    db.commit()
    deleted = cursor.rowcount
    db.close()
    
    if deleted:
        return jsonify({"success": True, "deleted": id})
    else:
        return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    print("🎬 SIMPLE Media API")
    print("=" * 40)
    print("🏠 Home: http://localhost:5000")
    print("📖 GET All: http://localhost:5000/media")
    print("➕ POST: Send JSON to http://localhost:5000/media")
    print("❌ DELETE: http://localhost:5000/media/1")
    print("=" * 40)
    app.run(debug=True)