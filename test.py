import unittest
import json
from main import app

class TestMediaAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_1_homepage(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        print("Homepage works")
    
    def test_2_get_all_media_json(self):
        response = self.app.get('/api/media')
        self.assertEqual(response.status_code, 200)
        print("GET /api/media works")
    
    def test_3_get_all_media_xml(self):
        response = self.app.get('/api/media?format=xml')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/xml')
        print("XML format works")
    
    def test_4_get_single_media(self):
        response = self.app.get('/api/media/1')
        self.assertEqual(response.status_code, 200)
        print("GET /api/media/1 works")
    
    def test_5_search_media(self):
        response = self.app.get('/api/search?q=Movie')
        self.assertEqual(response.status_code, 200)
        print("Search works")
    
    def test_6_create_media(self):
        new_media = {
            "title": "Test Movie",
            "duration": "120 min",
            "rating": "PG-13",
            "release_date": "2024",
            "media_type": "Movie"
        }
        response = self.app.post('/api/media', 
                               json=new_media,
                               content_type='application/json')
        self.assertEqual(response.status_code, 201)
        print("POST /api/media works")
    
    def test_7_update_media(self):
        update_data = {"rating": "PG"}
        response = self.app.put('/api/media/1', 
                              json=update_data,
                              content_type='application/json')
        self.assertEqual(response.status_code, 200)
        print("PUT /api/media/1 works")
    
    def test_8_delete_media(self):
        response = self.app.delete('/api/media/100')
        self.assertEqual(response.status_code, 404)
        print("DELETE returns proper error for non-existent ID")

if __name__ == '__main__':
    print("Testing Media API...")
    print("=" * 50)
    unittest.main(verbosity=2)