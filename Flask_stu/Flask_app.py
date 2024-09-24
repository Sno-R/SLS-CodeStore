from flask import Flask
from flask import request
from flask import make_response


app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to the Home Page!'

@app.route('/about')
def about():
    return 'This is the About Page.'

@app.route('/greet/<name>')
def greet(name):
    return f'Hello, {name}!'

@app.route('/user/<int:user_id>')
def user_profile(user_id):
    return f'User ID: {user_id}'

@app.route('/files/<path:filename>')
def serve_file(filename):
    return f'Serving file: {filename}'

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username') 
    return f'Hello, {username}!'
    # return 'Form submitted!'

@app.route('/custom_response')
def custom_response():
    response = make_response('This is a custom response!')
    response.headers['X-Custom-Header'] = 'Value'
    return response

@app.route('/info')
def info():
    user_agent = request.headers.get('User-Agent')
    return f'Your user agent is {user_agent}'

from flask import make_response

@app.route('/header')
def custom_header():
    response = make_response('Response with custom header')
    response.headers['X-Custom-Header'] = 'Value'
    return response


# @app.route('10.1.1.123')
# def test():
#     return 'test'

if __name__ == '__main__':
    app.run(debug=True)