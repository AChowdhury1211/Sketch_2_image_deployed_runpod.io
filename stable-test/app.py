from flask import Flask, request, jsonify, render_template
import requests
import base64

app = Flask(__name__)

# Replace with your actual RunPod API Endpoint and Authorization Token
RUNPOD_API_URL = "https://api.runpod.ai/v2/dfasfsadf/runsync"
API_KEY = ""  # Add your actual Bearer token


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate_image", methods=["POST"])
def generate_image():
    data = request.json
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {API_KEY}",
    }

    payload = {
        "input": {
            prompt: prompt,
            num_inference_steps: 25,
            width: 1024,
            height: 1024,
            guidance_scale: 7.5,
            seed: None,
            num_images: 1,
        }
    }

    try:
        response = requests.post(RUNPOD_API_URL, json=payload, headers=headers)
        response.raise_for_status()

        result = response.json()
        if "output" in result:
            image_base64 = result["output"]
            return jsonify({"image": image_base64})
        else:
            return jsonify({"error": "Failed to generate image"}), 500
    except requests.RequestException as e:
        print("Error:", e)
        return jsonify({"error": "Error generating image"}), 500


if __name__ == "__main__":
    app.run(debug=True)
