from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

# ---------- ENV VARIABLES ----------
INDEX_FILE = os.getenv("INDEX_FILE", "index.txt")
DATA_FILE = os.getenv("DATA_FILE", "file.json")

# ---------- LOAD DATA ----------
def load_lines():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print("File load error:", e)
        return []

lines = load_lines()

# ---------- INDEX ----------
def get_index():
    try:
        with open(INDEX_FILE, "r") as f:
            return int(f.read())
    except:
        return 0

def save_index(i):
    try:
        with open(INDEX_FILE, "w") as f:
            f.write(str(i))
    except Exception as e:
        print("Index save error:", e)

# ---------- SEQUENTIAL ----------
@app.route("/")
def get_next():
    if not lines:
        return jsonify({"error": "No data found"}), 500

    index = get_index()
    line = lines[index]

    response = {
        "index": index + 1,
        "total": len(lines),
        "flirt_line": line
    }

    index = (index + 1) % len(lines)
    save_index(index)

    return jsonify(response)

# ---------- DIRECT ACCESS ----------
@app.route("/<int:num>")
def get_by_number(num):
    if not lines:
        return jsonify({"error": "No data found"}), 500

    index = (num - 1) % len(lines)
    save_index(index + 1)

    return jsonify({
        "requested": num,
        "index": index + 1,
        "total": len(lines),
        "flirt_line": lines[index]
    })

# ---------- RENDER ENTRY ----------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
