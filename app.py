from flask import Flask, render_template, request

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

    # Get all headers as a dictionary for the debugger view
    all_headers = {k: v for k, v in request.headers.items()}

    return render_template('index.html', msisdn=msisdn or '', headers=all_headers)

if __name__ == '__main__':
    # Listen on all interfaces so it can be tested from other devices on mobile data
    app.run(host='0.0.0.0', port=8000, debug=True)
