import mysql.connector

print("🔍 Testing MySQL Connection...")

try:
    # Try to connect
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="media_db"
    )
    
    if conn.is_connected():
        print("✅ Connected to MySQL!")
        
        # Check database info
        cursor = conn.cursor(dictionary=True)
        
        # Check table exists
        cursor.execute("SHOW TABLES LIKE 'media_library'")
        table_exists = cursor.fetchone()
        if table_exists:
            print("✅ Table 'media_library' exists")
            
            # Count records
            cursor.execute("SELECT COUNT(*) as count FROM media_library")
            count = cursor.fetchone()['count']
            print(f"✅ Records in table: {count}")
            
            # Show first 3 records
            cursor.execute("SELECT media_id, title, duration FROM media_library LIMIT 3")
            records = cursor.fetchall()
            print("✅ Sample data:")
            for record in records:
                print(f"   ID {record['media_id']}: {record['title']} ({record['duration']})")
        else:
            print("❌ Table 'media_library' not found!")
        
        conn.close()
        print("✅ Connection closed properly")
        
except mysql.connector.Error as err:
    print(f"❌ MySQL Error: {err}")
    print("\n🔧 Try these solutions:")
    print("   1. Start MySQL service (search 'Services' in Windows)")
    print("   2. Check if database 'media_db' exists")
    print("   3. Try host='127.0.0.1' instead of 'localhost'")
    
except Exception as e:
    print(f"❌ Error: {e}")