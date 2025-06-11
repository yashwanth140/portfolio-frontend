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
def chat_proxy():
    user_input = request.json.get("message", "").strip()
    print(f"[MOCK] User asked: {user_input}")
    
    # Simulated fast test response
    return jsonify({
        "reply": f"✅ Test OK. You said: '{user_input}'"
    })
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
