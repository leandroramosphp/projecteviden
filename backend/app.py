from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
app = Flask(__name__)
CORS(app)  

bookmarks = []

@app.route('/bookmarks', methods=['GET'])
def get_bookmarks():
    return jsonify(bookmarks)

@app.route('/bookmarks', methods=['POST'])
def add_bookmark():
    data = request.get_json()
    # Validação simples
    if not all(key in data for key in ("title", "url", "remember_date")):
        return jsonify({"error": "Missing fields"}), 400

    try:
        datetime.strptime(data['remember_date'], '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format, expected YYYY-MM-DD"}), 400

    bookmarks.append(data)
    return jsonify(data), 201

if __name__ == '__main__':
    app.run(debug=True)
