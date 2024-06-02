from flask import Flask

app = Flask(__name__)

@app.route('/api')
def index():
    return "Hello from Backend 1"

if __name__ == '__main__':
    print("Backend 1 is running")
    app.run(host='0.0.0.0', port=5000)