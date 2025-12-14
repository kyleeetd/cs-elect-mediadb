from flask import Flask, jsonify, request, make_response
import mysql.connector
import json
import xml.etree.ElementTree as ET 

app = Flask(__name__)

# connecting database
def get_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root", 
        password="root",
        database="media_db"
    )

# FOR XML/JSON FORMATTING
def format_response(data, format_type='json'):
    """Return XML or JSON response"""
    if format_type == 'xml':
        # Create XML
        if isinstance(data, list):
            root = ET.Element('media_list')
            for item in data:
                media = ET.SubElement(root, 'media')
                for key, value in item.items():
                    elem = ET.SubElement(media, key)
                    elem.text = str(value)
        else:
            root = ET.Element('response')
            for key, value in data.items():
                elem = ET.SubElement(root, key)
                elem.text = str(value)
        
        xml_str = ET.tostring(root, encoding='unicode')
        response = make_response(xml_str, 200)
        response.headers['Content-Type'] = 'application/xml'
        return response
    else:
        # Default to JSON
        return jsonify(data)

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
    
    format_type = request.args.get('format', 'json')
    
    response_data = {
        "message": f"Found {len(media)} movies",
        "data": media
    }
    
    return format_response(response_data, format_type)

# 2. GET ONE
@app.route('/media/<int:id>', methods=['GET'])
def get_one(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM media_library WHERE media_id = %s", (id,))
    media = cursor.fetchone()
    db.close()
    
    # GET FORMAT PARAMETER
    format_type = request.args.get('format', 'json')
    
    if media:
        response_data = {"success": True, "data": media}
        return format_response(response_data, format_type)
    else:
        response_data = {"error": "Not found"}
        if format_type == 'xml':
            root = ET.Element('error')
            msg = ET.SubElement(root, 'message')
            msg.text = "Not found"
            xml_str = ET.tostring(root, encoding='unicode')
            response = make_response(xml_str, 404)
            response.headers['Content-Type'] = 'application/xml'
            return response
        else:
            return jsonify(response_data), 404

# 3. CREATE/PoOST
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

# 5. SEARCH
@app.route('/search', methods=['GET'])
def search():
    """Search media by title or type"""
    query = request.args.get('q', '')
    format_type = request.args.get('format', 'json')
    
    if not query:
        response_data = {"error": "Please provide search query (?q=...)"}
        if format_type == 'xml':
            root = ET.Element('error')
            msg = ET.SubElement(root, 'message')
            msg.text = "Please provide search query"
            xml_str = ET.tostring(root, encoding='unicode')
            response = make_response(xml_str, 400)
            response.headers['Content-Type'] = 'application/xml'
            return response
        else:
            return jsonify(response_data), 400
    
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT * FROM media_library 
        WHERE title LIKE %s OR media_type LIKE %s
    """, (f"%{query}%", f"%{query}%"))
    
    results = cursor.fetchall()
    db.close()
    
    response_data = {
        "query": query,
        "results_found": len(results),
        "data": results
    }
    
    return format_response(response_data, format_type)

if __name__ == '__main__':
    print("🎬 SIMPLE Media API")
    print("=" * 40)
    print("🏠 Home: http://localhost:5000")
    print("📖 GET All: http://localhost:5000/media")
    print("📖 GET All (XML): http://localhost:5000/media?format=xml")
    print("🔍 SEARCH: http://localhost:5000/search?q=movie")
    print("🔍 SEARCH (XML): http://localhost:5000/search?q=movie&format=xml")
    print("➕ POST: Send JSON to http://localhost:5000/media")
    print("❌ DELETE: http://localhost:5000/media/1")
    print("=" * 40)
    app.run(debug=True)