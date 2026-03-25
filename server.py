"""
StockMind v4 - Backend Server
"""
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import requests, os

app = Flask(__name__, static_folder='.')
CORS(app)

ANTHROPIC_KEY = os.environ.get('ANTHROPIC_KEY', '')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/quote/<symbol>')
def quote(symbol):
    key = request.args.get('key', '')
    r = requests.get(f'https://finnhub.io/api/v1/quote?symbol={symbol}&token={key}', timeout=10)
    return jsonify(r.json()), r.status_code

@app.route('/api/profile/<symbol>')
def profile(symbol):
    key = request.args.get('key', '')
    r = requests.get(f'https://finnhub.io/api/v1/stock/profile2?symbol={symbol}&token={key}', timeout=10)
    return jsonify(r.json()), r.status_code

@app.route('/api/metrics/<symbol>')
def metrics(symbol):
    key = request.args.get('key', '')
    r = requests.get(f'https://finnhub.io/api/v1/stock/metric?symbol={symbol}&metric=all&token={key}', timeout=10)
    return jsonify(r.json()), r.status_code

@app.route('/api/ai', methods=['POST'])
def ai():
    body = request.json or {}
    payload = body.get('payload', {})
    api_key = ANTHROPIC_KEY or body.get('api_key', '')
    r = requests.post('https://api.anthropic.com/v1/messages',
        headers={
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01',
            'x-api-key': api_key
        },
        json=payload, timeout=60)
    return jsonify(r.json()), r.status_code

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
