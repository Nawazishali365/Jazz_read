from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Retrieve MSISDN from common header variations
    msisdn = None
    header_keys = ['X-MSISDN', 'HTTP_X_MSISDN', 'X-Msisdn', 'MSISDN', 'x-msisdn']
    
    for key in header_keys:
        val = request.headers.get(key)
        if val:
            msisdn = val
            break

    return render_template('index.html', msisdn=msisdn or '')

@app.route('/bima_logo.jpg')
def bima_logo():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'bima_logo.jpg')

if __name__ == '__main__':
    # Listen on all interfaces so it can be tested from other devices on mobile data
    app.run(host='0.0.0.0', port=8000, debug=True)
