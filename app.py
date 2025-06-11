import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

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

# ---------- Chatbot Proxy (Frontend → VM Backend via NGINX) ----------
@app.route('/api/chat', methods=['POST'])
@app.route('/chat', methods=['POST'])
def chat_proxy():
    user_input = request.json.get("message")
    try:
        # ✅ FIX: Use local backend directly (no loop)
        vm_response = requests.post("https://yashwanthreddyportfolio.me/api/chat", json={"message": user_input}, timeout=15)
        return jsonify(vm_response.json())
    except Exception as e:
        print(f"[ERROR] Chat VM failed: {e}")
        return jsonify({"reply": "⚠️ Chatbot backend unavailable. Please try again later."}), 503


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
