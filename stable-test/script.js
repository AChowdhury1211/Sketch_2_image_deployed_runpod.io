// script.js
async function generateImage() {
    const prompt = document.getElementById("promptInput").value;
    if (!prompt) {
        alert("Please enter a prompt!");
        return;
    }

    const options = {
        method: "POST",
        headers: {
            accept: "application/json",
            "content-type": "application/json",
            // Replace with your actual API key
            authorization: "Bearer SWMB2SJN9C3RXZF31M6HOA6DN1AXHVA9KK4I04Q0",
        },
        body: JSON.stringify({
            input: {
                prompt: prompt,
                num_inference_steps: 25,
                width: 1024,
                height: 1024,
                guidance_scale: 7.5,
                seed: null,
                num_images: 1,
            },
        }),
    };

    try {
        const response = await fetch(
            // Replace with your actual Endpoint Id
            "https://api.runpod.ai/v2/k35kmnahqikfle/runsync",
            options,
        );
        const data = await response.json();
        console.log("data", data);
        if (data && data.output) {
            const imageBase64 = data.output;
            const imageUrl = `data:image/jpeg;base64,${imageBase64}`;
            document.getElementById("imageResult").innerHTML =
                `<img src="${imageUrl}" alt="Generated Image" />`;
        } else {
            alert("Failed to generate image");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Error generating image");
    }
}