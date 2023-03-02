from flask import Flask

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    return "Hello, Webhook!"

@app.route("/health", methods=["POST"])
def webhook():
    return "Hello, Health Check!"

@app.route("/rasp", methods=["POST"])
def webhook():
    return "Hello, Raspberry Pi!"


if __name__ == "__main__":
    app.run()


