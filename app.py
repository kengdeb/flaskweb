from flask import Flask

app = Flask(__name__)

@app.route('/')

def hello_world():
    return "Hello world test 1"

if __name__ == '__main':
    app.run(debug =)