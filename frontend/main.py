from crypt import methods
from flask import Flask, render_template, request
import json
from requests import get, post
from wtforms import Form, validators, StringField, SubmitField

app = Flask(__name__)

backendPath = 'https://api-template-dot-syscloud-355221.ew.r.appspot.com/api/v1/'
# backendPath = 'http://127.0.0.1:5000/api/v1/'

class InsertForm(Form):
    username = StringField(validators=[validators.input_required()])
    submit = SubmitField(label=('Submit'))

@app.route('/', methods=['GET'])
def index():
    response = json.loads(get(backendPath).content)
    message = response['message']
    return render_template('base.html', message=message)

@app.route('/users', methods=['GET'])
def users():
    print(get(backendPath + 'fake-users').content)
    response = json.loads(get(backendPath + 'fake-users').content)
    return render_template('users.html', users=response)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method=='GET':
        return render_template('create.html')
    username = request.form['username']

    payload = {
        'username': username
    }
    insert_resp = post(f'{backendPath}fake-users', json=payload).json()
    return render_template('base.html')

@app.route('/deleteAllUsers', methods=['GET'])
def deleteAllUsers():
    get(backendPath + 'fake-users/clean')
    return None, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)