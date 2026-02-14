import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import ollama

# -----------------------
# Flask Setup
# -----------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_FOLDER = os.path.abspath(os.path.join(BASE_DIR, "../frontend"))

app = Flask(__name__, static_folder=FRONTEND_FOLDER)
CORS(app)

# -----------------------
# Serve Frontend
# -----------------------

@app.route("/")
def serve_index():
    return send_from_directory(FRONTEND_FOLDER, "index.html")

@app.route("/<path:path>")
def serve_static_files(path):
    return send_from_directory(FRONTEND_FOLDER, path)

# -----------------------
# Chat Endpoint
# -----------------------

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Message field is required"}), 400

    user_message = data["message"]

    # Load your portfolio info
    with open(os.path.join(BASE_DIR, "portfolio_data.txt"), "r", encoding="utf-8") as f:
        portfolio_data = f.read()

    prompt = f"""
You are Uttam Maurya's professional AI portfolio assistant.

Only answer using the portfolio information below.
Be professional and concise.
If question is unrelated, politely redirect to portfolio topics.

Portfolio Information:
{portfolio_data}

User Question:
{user_message}
"""

    response = ollama.generate(
        model="phi3",
        prompt=prompt,
        options={
            "temperature": 0.4,
            "num_predict": 300
        }
    )

    return jsonify({"reply": response["response"]})


if __name__ == "__main__":
    app.run(debug=True)
