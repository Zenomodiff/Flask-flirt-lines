from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

# ---------- LOAD FILE SAFELY ----------
def load_lines():
    try:
        with open("file.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print("File load error:", e)
        return []

lines = load_lines()

INDEX_FILE = "index.txt"

# ---------- INDEX HANDLING ----------
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

# ---------- ROOT: SEQUENTIAL MODE ----------
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

    # move forward
    index = (index + 1) % len(lines)
    save_index(index)

    return jsonify(response)

# ---------- DIRECT INDEX MODE ----------
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

# ---------- RENDER ENTRY POINT ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)