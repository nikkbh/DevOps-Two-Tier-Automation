from flask import Flask, render_template, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "health": "healthy",
        "timestamp": datetime.now().isoformat()
    }), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    