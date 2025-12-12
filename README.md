Media Database API
Simple REST API with Flask and MySQL.

How to Use
Install: pip install -r requirements.txt

Create database: media_db

Run: python main.py

Test: python test_simple.py

API
GET /media - See all media

GET /search?q=movie - Search

POST /media - Add new

DELETE /media/1 - Delete

Files
main.py - API code

test_simple.py - Test script

requirements.txt - Packages needed