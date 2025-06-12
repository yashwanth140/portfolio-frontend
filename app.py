import os
from flask import Flask, render_template, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)

# ✅ Allow CORS only from your official frontend
CORS(app, origins=["https://yashwanthreddyportfolio.me"], supports_credentials=True)

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

# ---------- Chatbot Proxy (Frontend → VM via subdomain) ----------
@app.route('/api/chat', methods=['POST'])
def chat_proxy():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"reply": "No input provided."}), 400

    try:
        # Use subdomain with valid SSL cert (no verify=False needed)
        vm_response = requests.post(
            "https://chatbot.yashwanthreddyportfolio.me/api/chat",
            json={"message": user_input},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        vm_response.raise_for_status()
        return jsonify(vm_response.json())

    except Exception as e:
        print(f"[ERROR] Chat backend unreachable: {e}")
        return jsonify({"reply": "Chatbot backend unavailable. Please try again later."}), 503

# ---------- Local Dev Runner ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
