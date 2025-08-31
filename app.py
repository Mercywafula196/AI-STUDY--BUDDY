import os
import mysql.connector
from mysql.connector import pooling
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from utils.hf_client import generate_flashcards

load_dotenv()

app = Flask(__name__)

# Environment
HF_API_KEY = os.getenv("HF_API_KEY", "").strip()
HF_MODEL = os.getenv("HF_MODEL", "google/flan-t5-base")

MYSQL_CFG = {
    "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DB", "flashcards_db"),
}

# Simple MySQL connection pool
db_pool = pooling.MySQLConnectionPool(pool_name="flashcards_pool", pool_size=5, **MYSQL_CFG)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    if not HF_API_KEY:
        return jsonify({"error": "Missing HF_API_KEY"}), 400

    data = request.get_json(silent=True) or {}
    notes = (data.get("notes") or "").strip()
    if not notes:
        return jsonify({"error": "Notes text is required."}), 400

    try:
        cards = generate_flashcards(notes, HF_API_KEY, HF_MODEL)
        # save to DB
        conn = db_pool.get_connection()
        cur = conn.cursor()
        cur.executemany(
            "INSERT INTO flashcards (question, answer) VALUES (%s, %s)",
            [(c["question"], c["answer"]) for c in cards]
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(cards), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/flashcards", methods=["GET"])
def list_flashcards():
    conn = db_pool.get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, question, answer, created_at FROM flashcards ORDER BY id DESC LIMIT 100")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows), 200

if __name__ == "__main__":
    app.run(debug=True)