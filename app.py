from flask import Flask, render_template, request, jsonify
from chatbot import generate_response
from database import log_chat, init_db

app = Flask(__name__)
init_db()  # Initialize the SQLite DB at startup

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.form["message"]
    bot_reply = generate_response(user_message)
    log_chat(user_message, bot_reply)
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
