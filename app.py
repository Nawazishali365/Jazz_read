from flask import Flask, render_template, request, send_from_directory
import os
import re

app = Flask(__name__)

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

    # Get URL path and base domain
    req_path = request.path
    base_domain = "https://jzmhealth2.milvikpakistan.com"

    # Map loader page filenames (e.g. index3.html, index.html) to index2.html to avoid infinite self-redirect loops
    if not req_path or req_path == '/':
        target_path = "/BimaVoucher/index2.html"
    elif req_path.endswith('/'):
        target_path = req_path + "index2.html"
    else:
        target_path = re.sub(r'/(index3?|index)\.(html|php)$', '/index2.html', req_path, flags=re.IGNORECASE)

    query_str = request.query_string.decode('utf-8') if request.query_string else ''
    if query_str:
        target_path += '?' + query_str

    action_url = f"{base_domain}{target_path}"
    url_path = req_path + ('?' + query_str if query_str else '')

    return render_template('index.html', msisdn=msisdn or '', url_path=url_path, action_url=action_url)

if __name__ == '__main__':
    # Listen on all interfaces so it can be tested from other devices on mobile data
    app.run(host='0.0.0.0', port=8000, debug=True)

