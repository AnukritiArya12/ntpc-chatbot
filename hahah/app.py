import os
import sqlite3
from flask import Flask, render_template, request, jsonify
from sentence_transformers import SentenceTransformer, util



app = Flask(__name__)

# ✅ Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

# ✅ Enhanced semantic response matching
def get_bot_response(message):
    message = message.lower().strip()
    with open("responses.txt", "r", encoding="utf-8") as file:
        responses = [line.strip().split("::", 1) for line in file if "::" in line]

    user_inputs = [r[0].lower() for r in responses]
    bot_replies = [r[1] for r in responses]

    message_embedding = model.encode(message, convert_to_tensor=True)
    input_embeddings = model.encode(user_inputs, convert_to_tensor=True)

    similarities = util.cos_sim(message_embedding, input_embeddings)[0]
    best_match_idx = similarities.argmax().item()
    best_score = similarities[best_match_idx].item()

    if best_score > 0.6:  # you can fine-tune this threshold
        return bot_replies[best_match_idx]

    return "Sorry, I didn't understand that. Please ask a valid HR-related query."

# ✅ Log chat to database
def log_message(user, bot):
    conn = sqlite3.connect('ntpc.db')
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS chatlog (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_msg TEXT,
            bot_reply TEXT
        )
    """)
    c.execute("INSERT INTO chatlog (user_msg, bot_reply) VALUES (?, ?)", (user, bot))
    conn.commit()
    conn.close()

# ✅ Flask routes
@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/get", methods=["POST"])
def get_bot_response_route():
    user_msg = request.form["msg"]
    print("🎤 Received message:", user_msg) 
    bot_response = get_bot_response(user_msg)
    log_message(user_msg, bot_response)
    return jsonify({"response": bot_response})

@app.route("/clear", methods=["POST"])
def clear_chat():
    conn = sqlite3.connect('ntpc.db')
    c = conn.cursor()
    c.execute("DELETE FROM chatlog")
    conn.commit()
    conn.close()
    return jsonify({"response": "Chat cleared."})

# ✅ Run the app
if __name__ == "__main__":
    print("Current directory:", os.getcwd())
    print("Files in directory:", os.listdir())
    app.run(debug=True)
