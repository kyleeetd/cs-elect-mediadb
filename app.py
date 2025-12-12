from flask import Flask, jsonify, request
import mysql.connector
from datetime import datetime

import xml.etree.ElementTree as ET
from flask import make_response

def get_all_media():
    format_type = request.args.get('format', 'json')  # Get ?format=xml
    
    if format_type == 'xml':
        # Return XML instead of JSON
        root = ET.Element('media_library')
        for media in rows:
            item = ET.SubElement(root, 'media')
            for key, value in media.items():
                ET.SubElement(item, key).text = str(value)
        
        xml_str = ET.tostring(root, encoding='unicode')
        return make_response(xml_str, 200)
    else:
        return jsonify(rows)  # Normal JSON

app = Flask(__name__)

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="media_db"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return None

def format_response(data, success=True, message="", status_code=200):
    response = {
        "success": success,
        "message": message,
        "timestamp": datetime.now().isoformat(),
        "data": data if data else []
    }
    return jsonify(response), status_code

@app.route('/api/media', methods=['GET'])
def get_all_media():
    conn = get_db_connection()
    if not conn:
        return format_response(None, False, "Database connection failed", 500)
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM media_library")
        rows = cursor.fetchall()
        return format_response(rows, True, f"Found {len(rows)} media records")
    except Exception as e:
        return format_response(None, False, str(e), 500)
    finally:
        if conn and conn.is_connected():
            conn.close()

@app.route('/api/media/<int:media_id>', methods=['GET'])
def get_one_media(media_id):
    conn = get_db_connection()
    if not conn:
        return format_response(None, False, "Database connection failed", 500)
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM media_library WHERE media_id = %s", (media_id,))
        row = cursor.fetchone()
        
        if row:
            return format_response(row, True, f"Found media ID {media_id}")
        else:
            return format_response(None, False, f"Media ID {media_id} not found", 404)
    except Exception as e:
        return format_response(None, False, str(e), 500)
    finally:
        if conn and conn.is_connected():
            conn.close()

@app.route('/api/media', methods=['POST'])
def create_media():
    data = request.json
    if not data:
        return format_response(None, False, "No data provided", 400)
    
    required_fields = ['title', 'duration', 'rating', 'release_date', 'media_type']
    for field in required_fields:
        if field not in data:
            return format_response(None, False, f"Missing required field: {field}", 400)
    
    conn = get_db_connection()
    if not conn:
        return format_response(None, False, "Database connection failed", 500)
    
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
        
        return format_response(new_record, True, "Media created successfully", 201)
    except Exception as e:
        return format_response(None, False, str(e), 500)
    finally:
        if conn and conn.is_connected():
            conn.close()

@app.route('/api/media/<int:media_id>', methods=['PUT'])
def update_media(media_id):
    data = request.json
    if not data:
        return format_response(None, False, "No data provided", 400)
    
    conn = get_db_connection()
    if not conn:
        return format_response(None, False, "Database connection failed", 500)
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM media_library WHERE media_id = %s", (media_id,))
        existing = cursor.fetchone()
        
        if not existing:
            return format_response(None, False, f"Media ID {media_id} not found", 404)
        
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
            return format_response(None, False, "No fields to update", 400)
        
        values.append(media_id)
        query = f"UPDATE media_library SET {', '.join(update_fields)} WHERE media_id = %s"
        
        cursor.execute(query, values)
        conn.commit()
        
        cursor.execute("SELECT * FROM media_library WHERE media_id = %s", (media_id,))
        updated = cursor.fetchone()
        
        return format_response(updated, True, "Media updated successfully")
    except Exception as e:
        return format_response(None, False, str(e), 500)
    finally:
        if conn and conn.is_connected():
            conn.close()

@app.route('/api/media/<int:media_id>', methods=['DELETE'])
def delete_media(media_id):
    conn = get_db_connection()
    if not conn:
        return format_response(None, False, "Database connection failed", 500)
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM media_library WHERE media_id = %s", (media_id,))
        existing = cursor.fetchone()
        
        if not existing:
            return format_response(None, False, f"Media ID {media_id} not found", 404)
        
        cursor.execute("DELETE FROM media_library WHERE media_id = %s", (media_id,))
        conn.commit()
        
        return format_response(None, True, f"Media ID {media_id} deleted successfully")
    except Exception as e:
        return format_response(None, False, str(e), 500)
    finally:
        if conn and conn.is_connected():
            conn.close()

@app.route('/api/search', methods=['GET'])
def search_media():
    query = request.args.get('q', '')
    if not query:
        return format_response(None, False, "Search query required", 400)
    
    conn = get_db_connection()
    if not conn:
        return format_response(None, False, "Database connection failed", 500)
    
    try:
        cursor = conn.cursor(dictionary=True)
        search_term = f"%{query}%"
        cursor.execute("""
            SELECT * FROM media_library 
            WHERE title LIKE %s OR media_type LIKE %s OR rating LIKE %s
        """, (search_term, search_term, search_term))
        
        rows = cursor.fetchall()
        return format_response(rows, True, f"Found {len(rows)} results for '{query}'")
    except Exception as e:
        return format_response(None, False, str(e), 500)
    finally:
        if conn and conn.is_connected():
            conn.close()

@app.route('/')
def home():
    return "Media Database API - Use /api/media endpoints"

if __name__ == '__main__':
    print("Starting Media Database API...")
    print("Home: http://localhost:5000")
    print("All Media: http://localhost:5000/api/media")
    print("Search: http://localhost:5000/api/search?q=Movie")