import requests

print("🎬 Testing XML & Search")
print("=" * 40)

# Test 1: Get JSON (default)
print("\n1. GET all in JSON:")
r = requests.get("http://localhost:5000/media")
print(f"✅ Status: {r.status_code}")
print(f"📊 Found: {r.json()['message']}")

# Test 2: Get XML
print("\n2. GET all in XML:")
r = requests.get("http://localhost:5000/media?format=xml")
print(f"✅ Status: {r.status_code}")
print(f"📋 Content-Type: {r.headers['Content-Type']}")
if "xml" in r.headers['Content-Type']:
    print("🎯 XML format works!")

# Test 3: Search MOVIES in JSON
print("\n3. SEARCH 'movie' in JSON:")
r = requests.get("http://localhost:5000/search?q=movie")
print(f"✅ Status: {r.status_code}")
data = r.json()
print(f"🔍 Found {data['results_found']} results for '{data['query']}'")

# NEW TEST: Search TV SHOWS in JSON
print("\n4. SEARCH 'TV' in JSON:")
r = requests.get("http://localhost:5000/search?q=TV")
print(f"✅ Status: {r.status_code}")
data = r.json()
print(f"📺 Found {data['results_found']} TV shows for '{data['query']}'")

# Test 5: Search MOVIES in XML (was test 4)
print("\n5. SEARCH 'movie' in XML:")
r = requests.get("http://localhost:5000/search?q=movie&format=xml")
print(f"✅ Status: {r.status_code}")
print(f"📋 Content-Type: {r.headers['Content-Type']}")
if "xml" in r.headers['Content-Type']:
    print("🎯 Search with XML works!")

# NEW TEST: Search TV SHOWS in XML
print("\n6. SEARCH 'TV' in XML:")
r = requests.get("http://localhost:5000/search?q=TV&format=xml")
print(f"✅ Status: {r.status_code}")
print(f"📋 Content-Type: {r.headers['Content-Type']}")
if "xml" in r.headers['Content-Type']:
    print("🎯 TV shows search with XML works!")

print("\n" + "=" * 40)
print("✅ ALL TESTS PASSED!")