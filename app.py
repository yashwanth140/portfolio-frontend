import os
import time
import logging
from flask import Flask, render_template, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)

# Allow CORS only from your official domain
CORS(app, origins=["https://yashwanthreddyportfolio.me"], supports_credentials=True)

# Logging setup
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

# Static Pages
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

# Chatbot Proxy (Frontend → VM via Subdomain) 
@app.route('/api/chat', methods=['POST'])
def chat_proxy():
    user_input = request.json.get("message", "").strip()
    if not user_input:
        return jsonify({"reply": "No input provided."}), 400

    backend_url = "https://chatbot.yashwanthreddyportfolio.me/api/chat"
    start_time = time.time()

    try:
        vm_response = requests.post(
            backend_url,
            json={"message": user_input},
            headers={"Content-Type": "application/json"},
            timeout=180
        )

        duration = time.time() - start_time
        logging.info(f"[DEBUG] Backend status: {vm_response.status_code}, Time: {duration:.2f}s")

        # Parse backend response safely
        try:
            return jsonify(vm_response.json())
        except Exception as json_error:
            logging.error(f"[ERROR] Failed to parse JSON from backend: {json_error}")
            logging.debug(f"[DEBUG] Raw response: {vm_response.text[:300]}")
            return jsonify({"reply": "The assistant responded in an unexpected format."}), 502

    except requests.exceptions.Timeout:
        logging.error("[TIMEOUT] Chatbot backend took too long to respond.")
        return jsonify({"reply": "The assistant timed out. Please try again shortly."}), 504

    except requests.exceptions.ConnectionError:
        logging.error("[CONNECTION ERROR] Chatbot backend is unreachable.")
        return jsonify({"reply": "The assistant is currently unavailable. Please try again later."}), 503

    except Exception as e:
        logging.exception(f"[UNEXPECTED ERROR] {e}")
        return jsonify({"reply": "An internal error occurred. Please try again later."}), 500

# ---------- Dev Runner ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
