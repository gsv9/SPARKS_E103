from flask import Flask, request, jsonify
from flask_cors import CORS
from intent import detect_intent
from platform_logic import process_message

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    intent = detect_intent(user_message)
    response = process_message(intent, user_message)  # ✅ FIXED
    return jsonify(response)

app.run(host="0.0.0.0", port=81)
