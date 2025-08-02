from classes_py.find_text import TextFinder
from classes_py.Fragment_text import Fragment
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
  r"/api/*": {
    "origins": ["http://localhost:5173"],  # URL вашего React-приложения
    "methods": ["GET", "POST"]
  }
})

@app.route('/')

def get_text():
    TEXTFIND =  TextFinder
    TEXTFIND.text = TEXTFIND.get_random_text()
    FRAGMENT = Fragment(TEXTFIND.text)

    TEXT = FRAGMENT.random_fragment()

    return jsonify({"fragment":  TEXT})

if __name__ == '__main__':
    app.run(debug=True, port=5001)