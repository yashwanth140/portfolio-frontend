import os
import time
import logging
from flask import Flask, render_template, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)

# Allow CORS only from official frontend
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

# Chatbot Proxy (Frontend → VM via subdomain) 
@app.route('/api/chat', methods=['POST'])
def chat_proxy():
    user_input = request.json.get("message", "").strip()
    if not user_input:
        return jsonify({"reply": "No input provided."}), 400

    start_time = time.time()

    try:
        vm_response = requests.post(
            "https://chatbot.yashwanthreddyportfolio.me/api/chat",
            json={"message": user_input},
            headers={"Content-Type": "application/json"},
            timeout=180
        )

        logging.info(f"[DEBUG] Status code: {vm_response.status_code}")
        logging.info(f"[DEBUG] Time taken: {time.time() - start_time:.2f}s")

        # Try to return JSON regardless of status
        try:
            return jsonify(vm_response.json())
        except Exception as parse_err:
            logging.error(f"[ERROR] Could not parse JSON: {parse_err}")
            logging.debug(f"[DEBUG] Raw backend response: {vm_response.text[:500]}")
            return jsonify({"reply": "Backend responded with unreadable format."}), 502

    except requests.exceptions.Timeout:
        logging.error("[ERROR] Backend request timed out.")
        return jsonify({"reply": "Chatbot backend timed out. Please try again later."}), 504

    except requests.exceptions.ConnectionError:
        logging.error("[ERROR] Backend connection failed.")
        return jsonify({"reply": "Chatbot backend is unreachable. Please try again shortly."}), 503

    except Exception as e:
        logging.error(f"[ERROR] Unexpected error: {e}")
        return jsonify({"reply": "Unexpected error occurred while processing your request."}), 500

# ---------- Local Dev Runner ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
