# Imports
from flask import Flask
from api import config

app = Flask(__name__)

@app.route('/ping')
def ping():
    return 'pong!'

@app.route('/var')
def var():
    return config.s3_host

if __name__ == '__main__':
    app.run()
