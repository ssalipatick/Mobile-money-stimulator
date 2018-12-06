from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

@app.route('/client')
def client(responses = None):
    return render_template('client.html', responses = responses)

@app.route('/post_client_request', methods = ['GET', 'POST'])
def post_client_request():
    if request.method == 'POST':
        req = request.form['req_text']
    incoming = response(req, 'client')
    incoming.resp()


class response():
    def __init__(self, incoming_req, origin):
        self.incoming_req = incoming_req
        self.origin = origin
        self.resp_one = {
            'pay': { 'title': 'Pay', 'items': ['Pay', 'Account'] },
            'account': { 'title': 'Account', 'items': { 'Check Balance', 'Change Pin', 'Statement' } }
        }


if __name__ == '__main__':
    app.run(debug = True)

    session[step1] = 