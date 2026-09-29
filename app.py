from flask import Flask, render_template, request, send_from_directory
import os
import re
from urllib.parse import urlparse


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

    #base_domain = os.getenv("BASE_DOMAIN", "https://jzmhealth2.milvikpakistan.com")
    #base_domain = f"{request.scheme}://{request.headers.get('X-Forwarded-Host', request.host)}"
    base_domain = f"https://{urlparse(request.url).netloc}"
    print("REQUEST URL:", request.url)
    print("HOST:", request.host)
    print("HEADERS:", dict(request.headers))



    if clean_path == '/':
        action_url = f"{base_domain}/BimaVoucher/index2.html"
    else:
        action_url = f"{base_domain}{url_path}"

    print("Action URL",action_url)
    return render_template('index.html', msisdn=msisdn or '', url_path=url_path, action_url=action_url)

if __name__ == '__main__':
    # Load .env file if available
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    os.environ.setdefault(k.strip(), v.strip())

    port = int(os.getenv("PORT", 8000))
    # Listen on all interfaces so it can be tested from other devices on mobile data
    app.run(host='0.0.0.0', port=port, debug=True)

