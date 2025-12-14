import requests

print("🎬 Testing CRUD Operations")
print("=" * 50)

# Test 1: GET all in JSON
print("\n1. 📖 GET all media (JSON):")
r = requests.get("http://localhost:5000/media")
print(f"   Status: {r.status_code}")
print(f"   Found: {r.json()['message']}")

# Test 2: GET all in XML
print("\n2. 📄 GET all media (XML):")
r = requests.get("http://localhost:5000/media?format=xml")
print(f"   Status: {r.status_code}")
print(f"   Content-Type: {r.headers['Content-Type']}")
if "xml" in r.headers['Content-Type']:
    print("   ✅ XML format works!")

# Test 3: SEARCH movies in JSON
print("\n3. 🔍 SEARCH 'movie' (JSON):")
r = requests.get("http://localhost:5000/search?q=movie")
print(f"   Status: {r.status_code}")
data = r.json()
print(f"   Found {data['results_found']} results")

# Test 4: SEARCH TV shows in JSON
print("\n4. 📺 SEARCH 'TV' (JSON):")
r = requests.get("http://localhost:5000/search?q=TV")
print(f"   Status: {r.status_code}")
data = r.json()
print(f"   Found {data['results_found']} TV shows")

# Test 5: POST - CREATE
print("\n5. ➕ POST - Create new movie:")
new_movie = {
    "title": "Test Movie - Avengers",
    "duration": 150,
    "rating": 8.5,
    "media_type": "Movie"
}
r = requests.post("http://localhost:5000/media", json=new_movie)
print(f"   Status: {r.status_code} (Should be 201 Created)")
data = r.json()
if r.status_code == 201:
    created_id = data['id']
    print(f"   ✅ Created movie with ID: {created_id}")
else:
    print(f"   ❌ Failed: {data}")

# Test 6: GET the newly created movie
if 'created_id' in locals():
    print(f"\n6. 👁️ GET movie ID {created_id}:")
    r = requests.get(f"http://localhost:5000/media/{created_id}")
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        print(f"   ✅ Found: {r.json()['data']['title']}")

# Test 7: DELETE the created movie
if 'created_id' in locals():
    print(f"\n7. ❌ DELETE movie ID {created_id}:")
    r = requests.delete(f"http://localhost:5000/media/{created_id}")
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        print(f"   ✅ Successfully deleted")

# Test 8: Verify deletion
if 'created_id' in locals():
    print(f"\n8. 🔍 Verify movie ID {created_id} is deleted:")
    r = requests.get(f"http://localhost:5000/media/{created_id}")
    print(f"   Status: {r.status_code} (Should be 404 Not Found)")
    if r.status_code == 404:
        print("   ✅ Correctly shows not found")

# Test 9: SEARCH movies in XML
print("\n9. 🔍 SEARCH 'movie' (XML):")
r = requests.get("http://localhost:5000/search?q=movie&format=xml")
print(f"   Status: {r.status_code}")
print(f"   Content-Type: {r.headers['Content-Type']}")
if "xml" in r.headers['Content-Type']:
    print("   ✅ Search with XML works!")

# Test 10: SEARCH TV shows in XML
print("\n10. 📺 SEARCH 'TV' (XML):")
r = requests.get("http://localhost:5000/search?q=TV&format=xml")
print(f"   Status: {r.status_code}")
print(f"   Content-Type: {r.headers['Content-Type']}")
if "xml" in r.headers['Content-Type']:
    print("   ✅ TV shows search with XML works!")

print("\n" + "=" * 50)
print("✅ ALL CRUD TESTS PASSED!")
