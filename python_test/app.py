from flask import Flask, request, render_template, jsonify
import requests
import base64
from io import BytesIO

app = Flask(__name__)

# Replace this with your actual Runpod API key
API_KEY = ""
RUNPOD_API_URL = "https://api.runpod.ai/v2/y0w7gzrcq90ju5/runsync"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate_image", methods=["POST"])
def generate_image():
    try:
        prompt = request.form.get("prompt")
        image_url = request.form.get("imageUrl")
        model_name = request.form.get("modelName")

        if not prompt or not image_url or not model_name:
            return jsonify({"error": "Missing required fields"}), 400

        # Fetch the image from the provided URL
        response = requests.get(image_url)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch the image."}), 400

        # Convert image to Base64
        image_data = base64.b64encode(response.content).decode("utf-8")

        # Prepare the payload for Runpod API
        payload = {
            "input": {
                "prompt": prompt,
                "model_name": model_name,
                "model_path": "",
                "low_threshold": 100,
                "high_threshold": 200,
                "gamma": 0.4,
                "seed": 42,
                "use_fp16": False,
                "input_image": image_data,
            }
        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {API_KEY}",
        }

        # Make the API request
        api_response = requests.post(RUNPOD_API_URL, json=payload, headers=headers)

        if api_response.status_code != 200:
            return jsonify({"error": "Runpod API request failed"}), 500

        data = api_response.json()
        print(f"data: {data}")
        if "output" in data:
            # Decode the output image from base64
            generated_image_base64 = data["output"]
            return jsonify({"image_base64": generated_image_base64})

        return jsonify({"error": "Invalid API response format"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
