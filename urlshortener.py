from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

url_map = {}

def generate_short_url(original_url):
    hash_object = hashlib.sha1(original_url.encode())
    hex_dig = hash_object.hexdigest()
    return "https://short.est/" + hex_dig[:7]

@app.route('/encode', methods=['POST'])
def encode():
    data = request.get_json()
    if 'url' not in data:
        return jsonify({'error': 'URL not provided'}), 400
    original_url = data['url']
    short_url = generate_short_url(original_url)
    url_map[short_url] = original_url
    return jsonify({'short_url': short_url}), 200

@app.route('/decode', methods=['POST'])
def decode():
    data = request.get_json()
    if 'short_url' not in data:
        return jsonify({'error': 'No short URL provided'}), 400
    short_url = data['short_url']
    if short_url not in url_map:
        return jsonify({'error': 'No short URL found'}), 404
    original_url = url_map[short_url]
    return jsonify({'original_url': original_url}), 200

if __name__ == '__main__':
    app.run(debug=True)
