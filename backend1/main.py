from flask import Flask, request, jsonify
from flask_cors import CORS
from platform_logic import process_message

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    response = process_message(message)
    return jsonify(response)

if __name__ == "__main__":
    print("### BACKEND STARTED ###")
    app.run(host="0.0.0.0", port=81)
