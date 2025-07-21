import os
import logging
from flask import Flask, render_template, request, jsonify
import requests
from flask_cors import CORS
import random
import re

app = Flask(__name__)

# ✅ Allow CORS only from your official frontend
CORS(app, origins=["https://yashwanthreddyportfolio.me"], supports_credentials=True)

logging.basicConfig(level=logging.INFO)

# ---------- Static Pages ----------
@app.route('/')
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/education')
def education():
    return render_template('education.html')

@app.route('/experience')
def experience():
    return render_template('experience.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

# ---------- Chatbot Proxy ----------
@app.route('/api/chat', methods=['POST'])
def chat_proxy():
    user_input = request.json.get("message", "").strip()
    if not user_input:
        return jsonify({"reply": "No input provided."}), 400

    try:
        vm_response = requests.post(
            "https://chatbot.yashwanthreddyportfolio.me/api/chat",
            json={"message": user_input},
            headers={"Content-Type": "application/json"},
            timeout=60   # ⬅ increased timeout to handle slow backend
        )
        vm_response.raise_for_status()
        return jsonify(vm_response.json())

    except Exception as e:
        logging.error(f"[ERROR] Chat backend unreachable: {e}")

        # Normalize input to detect exaggerated greetings
        normalized_input = re.sub(r'(.)\1{2,}', r'\1', user_input.lower())
        greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]

        greeting_fallbacks = [
            "Hi there! The assistant is currently waking up — please try again shortly.",
            "Hello! I’m temporarily offline. Give me a moment and I’ll be ready to assist.",
            "Greetings! The assistant is spinning up. Try again in a few seconds."
        ]

        professional_fallbacks = [
            "The assistant is temporarily offline. Please try again in a few moments.",
            "I'm currently initializing. Kindly retry after a short while.",
            "The chatbot backend is waking up — thank you for your patience.",
            "The assistant is not reachable at the moment. It may be starting up.",
            "The chatbot is powering up. This may take a few seconds — thank you for waiting.",
            "System is starting up to serve your request. Please retry shortly."
        ]

        if any(normalized_input.startswith(greet) for greet in greetings):
            selected_message = random.choice(greeting_fallbacks)
        else:
            selected_message = random.choice(professional_fallbacks)

        return jsonify({"reply": selected_message}), 503

# ---------- Local Dev Runner ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
