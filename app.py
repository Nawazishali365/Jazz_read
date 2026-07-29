from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)

# Base domain for destination redirects
BASE_DOMAIN = os.environ.get('BASE_DOMAIN', 'https://jzmhealth2.milvikpakistan.com').rstrip('/')

@app.route('/bima_logo.jpg')
def bima_logo():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'bima_logo.jpg')

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def index(path=''):
    # Retrieve MSISDN from common header variations
    msisdn = None
    header_keys = ['X-MSISDN', 'HTTP_X_MSISDN', 'X-Msisdn', 'MSISDN', 'x-msisdn']
    
    for key in header_keys:
        val = request.headers.get(key)
        if val:
            msisdn = val
            break

    # Get URL path and query string if present
    url_path = request.path
    if request.query_string:
        url_path += '?' + request.query_string.decode('utf-8')

    # Construct action URL using the specified BASE_DOMAIN
    if not path or url_path == '/':
        action_url = f"{BASE_DOMAIN}/BimaVoucher/index2.html"
    else:
        action_url = f"{BASE_DOMAIN}{url_path}"

    return render_template('index.html', msisdn=msisdn or '', url_path=url_path, action_url=action_url)

if __name__ == '__main__':
    # Listen on all interfaces so it can be tested from other devices on mobile data
    app.run(host='0.0.0.0', port=8000, debug=True)

