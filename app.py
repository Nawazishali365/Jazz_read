from flask import Flask, render_template, request, send_from_directory
import os
import re

app = Flask(__name__)

@app.route('/bima_logo.jpg')
def bima_logo():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'bima_logo.jpg')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path=''):
    # Retrieve MSISDN from common header variations
    msisdn = None
    header_keys = ['X-MSISDN', 'HTTP_X_MSISDN', 'X-Msisdn', 'MSISDN', 'x-msisdn']
    
    for key in header_keys:
        val = request.headers.get(key)
        if val:
            msisdn = val
            break

    # Remove '/fetch' segment from request URL path
    clean_path = re.sub(r'/fetch(?=/|$)', '', request.path, flags=re.IGNORECASE)
    if not clean_path:
        clean_path = '/'

    query_str = request.query_string.decode('utf-8') if request.query_string else ''
    url_path = clean_path + ('?' + query_str if query_str else '')

    base_domain = "https://jzmhealth2.milvikpakistan.com"

    if clean_path == '/':
        action_url = f"{base_domain}/BimaVoucher/index2.html"
    else:
        action_url = f"{base_domain}{url_path}"

    return render_template('index.html', msisdn=msisdn or '', url_path=url_path, action_url=action_url)

if __name__ == '__main__':
    # Listen on all interfaces so it can be tested from other devices on mobile data
    app.run(host='0.0.0.0', port=8000, debug=True)

