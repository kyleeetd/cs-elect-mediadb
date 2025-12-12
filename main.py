from flask import Flask, jsonify, request, make_response
import mysql.connector
import json
import xml.etree.ElementTree as ET
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root",
            database="media_db"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return None

def format_response(data, success=True, message="", status_code=200, format_type='json'):
    if format_type == 'xml':
        if isinstance(data, list):
            root = ET.Element('media_library')
            for item in data:
                media_elem = ET.SubElement(root, 'media')
                for key, value in item.items():
                    child = ET.SubElement(media_elem, key)
                    child.text = str(value)
        elif data:
            root = ET.Element('media')
            for key, value in data.items():
                child = ET.SubElement(root, key)
                child.text = str(value)
        else:
            root = ET.Element('response')
        
        xml_str = ET.tostring(root, encoding='unicode')
        response = make_response(xml_str, status_code)
        response.headers['Content-Type'] = 'application/xml'
        return response
    else:
        response_data = {
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "data": data if data else []
        }
        response = make_response(jsonify(response_data), status_code)
        response.headers['Content-Type'] = 'application/json'
        return response

@app.route('/')
def home():
    return "Media Database API - Use /api/media endpoints"

@app.route('/api/media', methods=['GET'])
def get_all_media():
    format_type = request.args.get('format', 'json')
    conn = get_db_connection()
    if not conn:
        return format_response(None, False, "Database connection failed", 500, format_type)
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM media_library")
        rows = cursor.fetchall()
        return format_response(rows, True, f"Found {len(rows)} media records", 200, format_type)
    except Exception as e:
        return format_response(None, False, str(e), 500, format_type)
    finally:
        if conn and conn.is_connected():
            conn.close()

@app.route('/api/media/<int:media_id>', methods=['GET'])
def get_one_media(media_id):
    format_type = request.args.get('format', 'json')
    conn = get_db_connection()
    if not conn:
        return format_response(None, False, "Database connection failed", 500, format_type)
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM media_library WHERE media_id = %s", (media_id,))
        row = cursor.fetchone()
        
        if row:
            return format_response(row, True, f"Found media ID {media_id}", 200, format_type)
        else:
            return format_response(None, False, f"Media ID {media_id} not found", 404, format_type)
    except Exception as e:
        return format_response(None, False, str(e), 500, format_type)
    finally:
        if conn and conn.is_connected():
            conn.close()

@app.route('/api/media', methods=['POST'])
def create_media():
    format_type = request.args.get('format', 'json')
    data = request.json
    if not data:
        return format_response(None, False, "No data provided", 400, format_type)
    
    required_fields = ['title', 'duration', 'rating', 'release_date', 'media_type']
    for field in required_fields:
        if field not in data:
            return format_response(None, False, f"Missing required field: {field}", 400, format_type)
    
    conn = get_db_connection()
    if not conn:
        return format_response(None, False, "Database connection failed", 500, format_type)
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO media_library (title, duration, rating, release_date, media_type)
            VALUES (%s, %s, %s, %s, %s)
        """, (data['title'], data['duration'], data['rating'], 
              data['release_date'], data['media_type']))
        
        conn.commit()
        new_id = cursor.lastrowid
        
        cursor.execute("SELECT * FROM media_library WHERE media_id = %s", (new_id,))
        new_record = cursor.fetchone()
        
        return format_response([new_record], True, "Media created successfully", 201, format_type)
    except Exception as e:
        return format_response(None, False, str(e), 500, format_type)
    finally:
        if conn and conn.is_connected():
            conn.close()

@app.route('/api/media/<int:media_id>', methods=['PUT'])
def update_media(media_id):
    format_type = request.args.get('format', 'json')
    data = request.json
    if not data:
        return format_response(None, False, "No data provided", 400, format_type)
    
    conn = get_db_connection()
    if not conn:
        return format_response(None, False, "Database connection failed", 500, format_type)
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM media_library WHERE media_id = %s", (media_id,))
        existing = cursor.fetchone()
        
        if not existing:
            return format_response(None, False, f"Media ID {media_id} not found", 404, format_type)
        
        update_fields = []
        values = []
        
        if 'title' in data:
            update_fields.append("title = %s")
            values.append(data['title'])
        if 'duration' in data:
            update_fields.append("duration = %s")
            values.append(data['duration'])
        if 'rating' in data:
            update_fields.append("rating = %s")
            values.append(data['rating'])
        if 'release_date' in data:
            update_fields.append("release_date = %s")
            values.append(data['release_date'])
        if 'media_type' in data:
            update_fields.append("media_type = %s")
            values.append(data['media_type'])
        
        if not update_fields:
            return format_response(None, False, "No fields to update", 400, format_type)
        
        values.append(media_id)
        query = f"UPDATE media_library SET {', '.join(update_fields)} WHERE media_id = %s"
        
        cursor.execute(query, values)
        conn.commit()
        
        cursor.execute("SELECT * FROM media_library WHERE media_id = %s", (media_id,))
        updated = cursor.fetchone()
        
        return format_response([updated], True, "Media updated successfully", 200, format_type)
    except Exception as e:
        return format_response(None, False, str(e), 500, format_type)
    finally:
        if conn and conn.is_connected():
            conn.close()

@app.route('/api/media/<int:media_id>', methods=['DELETE'])
def delete_media(media_id):
    format_type = request.args.get('format', 'json')
    conn = get_db_connection()
    if not conn:
        return format_response(None, False, "Database connection failed", 500, format_type)
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM media_library WHERE media_id = %s", (media_id,))
        existing = cursor.fetchone()
        
        if not existing:
            return format_response(None, False, f"Media ID {media_id} not found", 404, format_type)
        
        cursor.execute("DELETE FROM media_library WHERE media_id = %s", (media_id,))
        conn.commit()
        
        return format_response(None, True, f"Media ID {media_id} deleted successfully", 200, format_type)
    except Exception as e:
        return format_response(None, False, str(e), 500, format_type)
    finally:
        if conn and conn.is_connected():
            conn.close()

@app.route('/api/search', methods=['GET'])
def search_media():
    format_type = request.args.get('format', 'json')
    query = request.args.get('q', '')
    if not query:
        return format_response(None, False, "Search query required", 400, format_type)
    
    conn = get_db_connection()
    if not conn:
        return format_response(None, False, "Database connection failed", 500, format_type)
    
    try:
        cursor = conn.cursor(dictionary=True)
        search_term = f"%{query}%"
        cursor.execute("""
            SELECT * FROM media_library 
            WHERE title LIKE %s OR media_type LIKE %s OR rating LIKE %s
        """, (search_term, search_term, search_term))
        
        rows = cursor.fetchall()
        return format_response(rows, True, f"Found {len(rows)} results for '{query}'", 200, format_type)
    except Exception as e:
        return format_response(None, False, str(e), 500, format_type)
    finally:
        if conn and conn.is_connected():
            conn.close()

if __name__ == '__main__':
    print("🎬 Media Database API")
    print("=" * 50)
    print("Home: http://localhost:5000")
    print("All Media (JSON): http://localhost:5000/api/media")
    print("All Media (XML): http://localhost:5000/api/media?format=xml")
    print("Search Movies: http://localhost:5000/api/search?q=Movie")
    print("Search TV Shows: http://localhost:5000/api/search?q=TV%20Show")
    print("=" * 50)
    app.run(debug=True, port=5000)