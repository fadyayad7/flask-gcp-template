from email import message
from flask import Flask, render_template
import json
from requests import patch, get

app = Flask(__name__)

# @app.route('/', methods=['GET'])
# def index():
#     page='index'
#     patch(f'http://127.0.0.1:5000/api/v1/visits/{page}')
#     return render_template('base.html', page=page)

# @app.route('/test', methods=['GET'])
# def test():
#     page='test'
#     patch(f'http://127.0.0.1:5000/api/v1/visits/{page}')
#     return render_template('base.html', page=page)

# @app.route('/error', methods=['GET'])
# def error():
#     page='error'
#     patch(f'http://127.0.0.1:5000/api/v1/visits/{page}')
#     return render_template('base.html', page=page)


############## START HERE #############################

backendPath = 'http://127.0.0.1:5000/api/v1'

@app.route('/', methods=['GET'])
def index():
    response = json.loads(get(backendPath).content)
    message = response['message']
    return render_template('base.html', message=message)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)