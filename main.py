from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route("/run", methods=["POST"])
def run_script():
    code = request.json.get("code")

    with open("temp_script.py", "w") as f:
        f.write(code)

    try:
        result = subprocess.check_output(["python", "temp_script.py"], stderr=subprocess.STDOUT, timeout=20)
        return jsonify({"output": result.decode()})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": e.output.decode()}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def status():
    return "✅ API is running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)