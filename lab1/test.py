#testing
'''
this should contain: 
username: abc
password: 123
'''

from flask import Flask, render_template
from OpenSSL import SSL

app = Flask(__name__)


# Create an SSL context and load your SSL certificate and private key
context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file('test.py.key')  # Replace 'your_domain.key' with your private key filename
context.use_certificate_file('test.py.crt')  # Replace 'your_domain.crt' with your certificate filename


@app.route("/")
def home():
    return render_template("test.html")


@app.route('/hello')
def hello():
    return 'Hello, World'

app.run(debug=True)
app.run(host="127.0.0.9", port=443, debug=True, ssl_context = context)
