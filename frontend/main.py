from crypt import methods
from flask import Flask, render_template, request
import json
from requests import get, post
from wtforms import Form, validators, StringField, SubmitField
from datetime import datetime

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

######### POOL ######################
@app.route('/pool', methods=['GET'])
def get_pool_status():
    today = datetime.now().strftime("%Y-%m-%d")
    reservs = get(f"{backendPath}pool-status/{today}").json()
    reservs = reservs["reservations"]

    now_time = int(datetime.now().strftime("%H"))
    if now_time%2 == 1: now_time-=1

    now_time = f"{now_time}-{now_time+2}"

    now_reservs = [ reserv for reserv in reservs if reserv["time"] == now_time ]
    # return now_reservs
    free_lanes = {}
    for r in now_reservs:
        lane = r["lane"]
        if lane not in free_lanes: free_lanes[lane] = 0
        free_lanes[lane] += 1

    print(free_lanes)
    return render_template('pool.html', lanes=free_lanes, now_time=now_time)

@app.route('/lane/<lane_number>', methods=['GET'])
def get_lane_info(lane_number):
    today = datetime.now().strftime("%Y-%m-%d")
    reservs = get(f"{backendPath}pool-status/{today}").json()
    reservs = reservs["reservations"]

    now_time = int(datetime.now().strftime("%H"))
    if now_time%2 == 1: now_time-=1

    now_time = f"{now_time}-{now_time+2}"

    now_reservs = [ reserv for reserv in reservs if reserv["time"] == now_time and reserv["lane"] == int(lane_number) ]
    print(now_reservs)

    return render_template('lane.html', reservations=now_reservs, lane=lane_number, now_time=now_time)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)