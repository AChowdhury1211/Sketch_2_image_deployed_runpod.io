from flask import Flask, request, jsonify, send_file
import os
import subprocess
import tempfile
from werkzeug.utils import secure_filename

app = Flask(__name__)

INPUT_DIR = "input"
OUTPUT_DIR = "output"
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.route("/inference_paired", methods=["POST"])
def process_image():
    file = request.files["file"]
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    elif file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    else:
        pass

    input_image_path = os.path.join(
        INPUT_DIR, secure_filename(os.path.basename(file.filename))
    )
    file.save(input_image_path)

    prompt = request.form.get("prompt")
    model_name = request.form.get("model_name", "")
    model_path = request.form.get("model_path", "")
    low_threshold = int(request.form.get("low_threshold", 100))
    high_threshold = int(request.form.get("high_threshold", 200))
    gamma = float(request.form.get("gamma", 0.4))
    seed = int(request.form.get("seed", 42))
    use_fp16 = "use_fp16" in request.form

    command = [
        "python",
        "src/inference_paired.py",
        "--input_image",
        input_image_path,
        "--prompt",
        prompt,
        "--model_name",
        model_name,
        "--model_path",
        model_path,
        "--output_dir",
        OUTPUT_DIR,
        "--low_threshold",
        low_threshold,
        "--high_threshold",
        high_threshold,
        "--gamma",
        gamma,
        "--seed",
        seed,
    ]
    if use_fp16:
        command.append("--use_fp16")

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        return jsonify({"error": result.stderr}), 500

    output_file = os.path.join(
        OUTPUT_DIR, secure_filename(os.path.basename(file.filename))
    )
    if not os.path.exists(output_file):
        return jsonify({"error": "Output file not found"}), 500

    return send_file(output_file, mimetype="image/png", as_attachment=True)


@app.route("/inference_unpaired", methods=["POST"])
def process_image():
    file = request.files["file"]
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    elif file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    else:
        pass

    input_image_path = os.path.join(
        INPUT_DIR, secure_filename(os.path.basename(file.filename))
    )
    file.save(input_image_path)

    prompt = request.form.get("prompt")
    model_name = request.form.get("model_name", "")
    model_path = request.form.get("model_path", "")
    image_prep = request.form.get("image_prep", "resize_512x512")
    direction = request.form.get("direction", "")
    use_fp16 = "use_fp16" in request.form

    command = [
        "python",
        "src/inference_unpaired.py",
        "--input_image",
        input_image_path,
        "--prompt",
        prompt,
        "--model_name",
        model_name,
        "--model_path",
        model_path,
        "--output_dir",
        OUTPUT_DIR,
        "--image_prep",
    ]
    if use_fp16:
        command.append("--use_fp16")

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        return jsonify({"error": result.stderr}), 500

    output_file = os.path.join(
        OUTPUT_DIR, secure_filename(os.path.basename(file.filename))
    )
    if not os.path.exists(output_file):
        return jsonify({"error": "Output file not found"}), 500

    return send_file(output_file, mimetype="image/png", as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
