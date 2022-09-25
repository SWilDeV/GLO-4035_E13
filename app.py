from flask import Flask
app = Flask(__name__)


@app.route("/heartbeat")
def home():
    return {"Quebec":"str"}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)