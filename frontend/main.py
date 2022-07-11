from flask import Flask, render_template
import json
from requests import patch, get

app = Flask(__name__)

backendPath = 'https://api-template-dot-syscloud-355221.ew.r.appspot.com/api/v1/'

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)