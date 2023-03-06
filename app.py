import os
from flask import Flask, request, jsonify
import json

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    # basically what was send to telegram, it sends to somewhere else
    #token = ""
    # methodName = "setWebhook"
    # hostUrl = ""
    # url = "https://api.telegram.org/bot" + token + "/" + methodName +"?url=" + hostUrl

    result = None
    if request.is_json:
        result = request.get_json()
        
    else:
        data = request.get_data()
        print("Received an invalid Json:")
        print(data)
        return jsonify({"code": 400,
                        # make the data string as we dunno what could be the actual format
                        "data": str(data),
                        "message": "Request should be in JSON."}), 400  # Bad Request input

    return result

@app.route("/health", methods=["POST"])
def health():
    return "Hello, Health Check!"

@app.route("/rasp", methods=["POST"])
def rasp():
    return "Hello, Raspberry Pi!"


if __name__ == "__main__":
    app.run(port=5000, debug=True)


