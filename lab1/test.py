'''
test.py
'''

from flask import Flask, render_template
from OpenSSL import SSL

app = Flask(__name__)

# Create an SSL context and load your SSL certificate and private key

def get_passphrase(*args):
    return "your_passphrase"

context = SSL.Context(SSL.SSLv23_METHOD)
context.set_passwd_cb(get_passphrase)
context.use_privatekey_file('test.py.key')
context.use_certificate_file('test.py.crt')

@app.route("/")
def home():
    return render_template("test.html")

app.run(host="127.0.0.1", port=8443, debug=True, ssl_context = context)
