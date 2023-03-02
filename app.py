from flask import Flask

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    return "Hello, POST!"


if __name__ == "__main__":
    app.run()
