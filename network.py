from app import *
from application import client_ussd_session, agent_ussd_session
from flask import session, redirect, url_for, request,render_template,jsonify
from functools import wraps

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///swift.db'
db = SQLAlchemy(app)

session_data = {}

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'phone_number' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrap

# MAIN ROUTES
@app.route('/', methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        pin = request.form['pin']

        # first search for clients
        searched_client = Clients.query.filter_by(phone_number=phone_number,pin = pin).first()
        if searched_client:
            # redirect to client page
            session['phone_number'] = searched_client.phone_number
            session['type'] = 'client'
            session['pin'] = pin
            return redirect(url_for('client'))

        searched_agent = Agents.query.filter_by(phone_number=phone_number,pin = pin).first()
        if searched_agent:
            # redirect for agent page
            session['phone_number'] = searched_agent.phone_number
            session['type'] = 'agent'
            session['pin'] = pin
            return redirect(url_for('agent'))
        
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('phone_number', None)
    session.pop('type', None)
    session.pop('pin', None)
    return 'Success fully logedout'
@app.route('/reset')

@login_required
def reset():
    phone_number = session['phone_number']
    pin = session['pin']
    if session['type'] == 'client':
        session_data[session['phone_number']] = client_ussd_session(phone_number,pin)
    if session['type'] == 'agent':
        session_data[session['phone_number']] = agent_ussd_session(phone_number,pin)
    return '1'

@app.route('/client', methods = ['GET','POST'])
@login_required
def client():
    phone_number = session['phone_number']
    if phone_number not in session_data:
        phone_number = session['phone_number']
        pin = session['pin']
        session_data[phone_number] = client_ussd_session(phone_number,pin)
    if request.method == 'GET':
        return render_template('client.html')
    if request.method == 'POST':
        req = request.form['req_text']
        responses = session_data[phone_number].resp(req)
        if 'end' in responses:
            # log out the session
            session_data.pop(phone_number)
        return render_template('client.html',responses = responses)

@app.route('/agent',methods = ['GET','POST'])
@login_required
def agent():
    if 'phone_number' in session:
        phone_number = session['phone_number']
        if phone_number not in session_data:
            pin = session['pin']
            session_data[phone_number] = agent_ussd_session(phone_number,pin)
        if request.method == 'GET':
            return render_template('agent.html')
        if request.method == 'POST':
            req = request.form['req_text']
            responses = session_data[phone_number].resp(req)
            if 'end' in responses:
                # log out the session
                session_data.pop(phone_number)
            return render_template('agent.html',responses = responses)

# MESSAGES
@app.route('/messages', methods = ['GET'])
@login_required
def read_messages():
    number = session['phone_number']
    messages = ''
    msgs = message.query.filter_by(receiver=number)
    for msg in msgs:
        data = {}
        # data['sender']=msg.sender 
        # data['receiver']=msg.receiver 
        # data['content']=msg.content
        # data['datetime']=msg.datetime
        messages += msg.content+'<br>'
        msg.seen = 1
    db.session.commit()
    return messages

@app.route('/messages/unread', methods = ['GET'])
@login_required
def unread_messages():
    number = session['phone_number']
    messages = []
    msgs = message.query.filter_by(receiver=number, seen = 0)
    for msg in msgs:
        data = {}
        data['sender']=msg.sender 
        data['receiver']=msg.receiver 
        data['content']=msg.content
        data['datetime']=msg.datetime
        messages.append(data)
        msg.seen = 1
    db.session.commit()
    return jsonify(messages)

@app.route('/messages', methods = ['POST'])
@login_required
def send_messages():
    sender = session['phone_number']
    receiver = request.form['to']
    content = request.form['content']
    msg = message(sender= sender,
                receiver = receiver,
                content = content
                    )
    db.session.add(msg)
    db.session.commit()
    return 'Success'

@app.route('/create_client', methods = ['GET','POST'])
def create_client():
    if request.method == 'GET':
        return render_template('create_client.html')
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']
        pin = request.form['pin']
        balance = request.form['balance']

        new_client = Clients(
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
            pin = pin,
            balance = balance
            )
        db.session.add(new_client)
        db.session.commit()
        return redirect(url_for('login'))

@app.route('/create_agent', methods = ['GET','POST'])
def create_agent():
    if request.method == 'GET':
        return render_template('create_agent.html')
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']
        pin = request.form['pin']
        balance = request.form['balance']

        new_agent = Agents(
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
            pin = pin,
            balance = balance
            )
        db.session.add(new_agent)
        db.session.commit()
        return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug = True)
