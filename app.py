from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

def get_db():
    """Connect to MySQL database"""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="media_db"
        )
        return conn
    except Exception as e:
        print(f"Database Error: {e}")
        return None

@app.route('/')
def home():
    return "🎬 Media Database API is running! Try /api/media"

@app.route('/api/media', methods=['GET'])
def get_all_media():
    """Get all media from database"""
    conn = get_db()
    if not conn:
        return jsonify({"error": "Cannot connect to database"}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT media_id, title, duration FROM media_library")
        media_list = cursor.fetchall()
        
        return jsonify({
            "success": True,
            "count": len(media_list),
            "data": media_list
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn.is_connected():
            conn.close()

@app.route('/api/media/<int:id>', methods=['GET'])
def get_media_by_id(id):
    """Get specific media by ID"""
    conn = get_db()
    if not conn:
        return jsonify({"error": "Cannot connect to database"}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM media_library WHERE media_id = %s", (id,))
        media = cursor.fetchone()
        
        if media:
            return jsonify({
                "success": True,
                "data": media
            })
        else:
            return jsonify({
                "success": False,
                "error": f"Media with ID {id} not found"
            }), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn.is_connected():
            conn.close()

if __name__ == '__main__':
    print("=" * 50)
    print("🎬 Media Database REST API")
    print("=" * 50)
    print("Homepage: http://localhost:5000")
    print("All Media: http://localhost:5000/api/media")
    print("Single Media: http://localhost:5000/api/media/1")
    print("=" * 50)
    app.run(debug=True, port=5000)