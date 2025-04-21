import unittest
from app import app

class BookmarkTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_bookmarks_empty(self):
        response = self.app.get('/bookmarks')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_add_bookmark(self):
        bookmark = {
            "title": "OpenAI",
            "url": "https://openai.com",
            "remember_date": "2025-04-19"
        }
        response = self.app.post('/bookmarks', json=bookmark)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['message'], 'Bookmark added!')

    def test_get_bookmarks_after_adding(self):
        response = self.app.get('/bookmarks')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.get_json()), 0)

if __name__ == '__main__':
    unittest.main()
