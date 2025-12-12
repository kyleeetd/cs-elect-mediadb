import requests

BASE_URL = "http://localhost:5000/media"

def print_response(title, response):
    print(f"\n=== {title} ===")
    print("Status:", response.status_code)
    try:
        print(response.json())
    except:
        print(response.text)

print("🎬 MEDIA API DEMO")
print("=" * 40)

# 1. GET ALL (RETRIEVE)
response = requests.get(BASE_URL)
print_response("1. READ - Get all media", response)

# 2. CREATE (POST) - Add new movie
print("\n" + "=" * 40)
print("2. CREATE - Add new movie")
new_movie = {
    "title": "Toy Story",
    "duration": 81,
    "rating": 8.3,
    "media_type": "Movie"
}
response = requests.post(BASE_URL, json=new_movie)
print_response("POST result", response)

# Get the ID of new created movie
if response.status_code == 201:
    new_id = response.json().get("id")
    print(f"✅ Created movie with ID: {new_id}")
else:
    print("❌ Failed to create movie")
    new_id = None

# 3. GET ONE (RETRIEVE one only)
if new_id:
    print("\n" + "=" * 40)
    print(f"3. READ - Get movie ID {new_id}")
    response = requests.get(f"{BASE_URL}/{new_id}")
    print_response(f"GET movie {new_id}", response)

# 4. DELETE
if new_id:
    print("\n" + "=" * 40)
    print(f"4. DELETE - Remove movie ID {new_id}")
    response = requests.delete(f"{BASE_URL}/{new_id}")
    print_response(f"DELETE movie {new_id}", response)

# 5. FINAL CHECK
print("\n" + "=" * 40)
print("5. FINAL - Get all media again")
response = requests.get(BASE_URL)
print_response("Final check", response)

print("\n" + "=" * 40)
print("DEMO COMPLETE!")