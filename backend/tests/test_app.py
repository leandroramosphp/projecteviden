import unittest
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)


bookmarks = []

@app.route('/bookmarks', methods=['GET'])
def get_bookmarks():
    return jsonify(bookmarks)

@app.route('/bookmarks', methods=['POST'])
def add_bookmark():
    data = request.get_json()

    if not all(key in data for key in ("title", "url", "remember_date")):
        return jsonify({"error": "Missing fields"}), 400


    try:
        datetime.strptime(data['remember_date'], '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format, expected YYYY-MM-DD"}), 400

    bookmarks.append(data)
    return jsonify(data), 201

# Testes
class BookmarkTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Inicializa a aplicação para os testes"""
        cls.client = app.test_client()
        app.config['TESTING'] = True

    def setUp(self):
        """Limpa os dados antes de cada teste"""
        global bookmarks
        bookmarks = []  

    def test_get_empty_bookmarks(self):
        """Deve retornar lista vazia inicialmente"""
        response = self.client.get('/bookmarks')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])  

    def test_add_bookmark(self):
        """Deve adicionar um novo bookmark"""
        new_bookmark = {
            'title': 'Meu novo bookmark',
            'url': 'https://meusite.com',
            'remember_date': '2025-04-21'
        }

        response = self.client.post('/bookmarks', 
                                    json=new_bookmark)
        self.assertEqual(response.status_code, 201)
        
        response = self.client.get('/bookmarks')
        self.assertEqual(response.status_code, 200)
        bookmarks = response.get_json()
        self.assertEqual(len(bookmarks), 1)
        self.assertEqual(bookmarks[0]['title'], 'Meu novo bookmark')

    def test_add_bookmark_missing_field(self):
        """Deve retornar erro se algum campo estiver faltando"""
        invalid_bookmark = {
            'title': 'Bookmark sem URL',
            'remember_date': '2025-04-21'
        }

        response = self.client.post('/bookmarks', 
                                    json=invalid_bookmark)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Missing fields"})

    def test_add_bookmark_invalid_date_format(self):
        """Deve retornar erro se o formato da data for inválido"""
        invalid_date_bookmark = {
            'title': 'Bookmark com data errada',
            'url': 'https://meusite.com',
            'remember_date': '21-04-2025'  
        }

        response = self.client.post('/bookmarks', 
                                    json=invalid_date_bookmark)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Invalid date format, expected YYYY-MM-DD"})

if __name__ == '__main__':
    unittest.main()
