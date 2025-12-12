import requests

def test_api():
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Media Database API...")
    
    # Test 1: Homepage
    print("\n1. Testing homepage...")
    try:
        response = requests.get(base_url)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:50]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Get all media
    print("\n2. Testing GET /api/media...")
    try:
        response = requests.get(f"{base_url}/api/media")
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Success: {data.get('success', False)}")
        print(f"   Count: {data.get('count', 0)} records")
        
        if data.get('data'):
            print(f"   First record: ID {data['data'][0]['media_id']} - {data['data'][0]['title']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Get single media
    print("\n3. Testing GET /api/media/1...")
    try:
        response = requests.get(f"{base_url}/api/media/1")
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Success: {data.get('success', False)}")
        if data.get('data'):
            print(f"   Data: {data['data']['title']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_api()