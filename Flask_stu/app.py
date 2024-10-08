from flask import Flask
from controller.bp_controller import testModule

app = Flask(__name__)
app.register_blueprint(testModule, url_prefix='/testModule')

@app.route('/')
def hello_world():
    return 'flask_test is running!!!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088)