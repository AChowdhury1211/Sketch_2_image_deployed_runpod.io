async function generateImage() {
    const prompt = document.getElementById("promptInput").value;
    if (!prompt) {
        alert("Please enter a prompt!");
        return;
    }

    const imageUrl = document.getElementById("imageUrlInput").value;
    if (!imageUrl) {
        alert("Please enter an image URL!");
        return;
    }

    const modelName = document.getElementById("modelnameInput").value;
    if (!modelName) {
        alert("Please enter model name!");
        return;
    }

    try {
        // Fetch the image
        const response = await fetch(imageUrl);
        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.statusText}`);
        }

        // Convert to a Blob
        const blob = await response.blob();
        const reader = new FileReader();

        const base64Data = await new Promise((resolve, reject) => {
            reader.onloadend = () => {
                try {
                    // Extract Base64 string
                    const base64String = reader.result.split(',')[1];
                    resolve(base64String);
                } catch (err) {
                    reject(new Error("Error while converting image to Base64."));
                }
            };
            reader.onerror = () => reject(new Error("Error reading image Blob."));
            reader.readAsDataURL(blob);
        });

        const options = {
            method: "POST",
            headers: {
                accept: "application/json",
                "content-type": "application/json",
                authorization: "Bearer",
            },
            body: JSON.stringify({
                input: {
                    prompt: prompt,
                    model_name: modelName,
                    model_path: "",
                    low_threshold: 100,
                    high_threshold: 200,
                    gamma: 0.4,
                    seed: 42,
                    use_fp16: false,
                    input_image: base64Data
                },
            }),
        };

        const apiResponse = await fetch(
            "https://api.runpod.ai/v2/59cajha73o3p0s/runsync",
            options
        );

        if (!apiResponse.ok) {
            throw new Error(`API request failed: ${apiResponse.statusText}`);
        }

        const data = await apiResponse.json();
        if (data && data.output) {
            const imageBase64 = data.output[0];
            const generatedImageUrl = `data:image/png;base64,${imageBase64}`;

            // Display the generated image
            document.getElementById("imageResult").innerHTML =
                `<img src="${generatedImageUrl}" alt="Generated Image" />`;
        } else {
            throw new Error("API response is missing the 'output' field.");
        }

    } catch (error) {
        console.error('Error:', error);
        alert(`Error: ${error.message}`);
    }
}
