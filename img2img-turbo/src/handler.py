import runpod
from pix2pix_turbo import Pix2Pix_Turbo
from image_prep import canny_from_pil
import torch
import base64
import io
import time
import os
import numpy as np
from PIL import Image
import torchvision.transforms.functional as F
from torchvision import transforms
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)


def handler(job):
    """Handler function that will be used to process jobs."""
    job_input = job["input"]
    prompt = job_input["prompt"]
    logging.info(f"Prompt: {prompt}")

    model_name = job_input["model_name"]
    logging.info(f"Model Name: {model_name}")

    model_path = job_input["model_path"]
    logging.info(f"Model Path: {model_path}")

    use_fp16 = job_input["use_fp16"]
    logging.info(f"Use FP16: {use_fp16}")

    low_threshold = job_input["low_threshold"]
    logging.info(f"Low Threshold: {low_threshold}")

    high_threshold = job_input["high_threshold"]
    logging.info(f"High Threshold: {high_threshold}")

    gamma = job_input["gamma"]
    logging.info(f"Gamma: {gamma}")

    seed = job_input["seed"]
    logging.info(f"Seed: {seed}")

    if model_path == None:
        model_path = ""

    # Initialize model
    time_start = time.time()
    model = Pix2Pix_Turbo(pretrained_name=model_name, pretrained_path=model_path)
    model.set_eval()
    if use_fp16:
        model.half()
    logging.info(f"Time taken to initialize model: {time.time() - time_start}")

    # Load and process input image
    image_base64 = job_input["input_image"]
    if image_base64.startswith("data:image"):
        image_base64 = image_base64.split(",")[1]
    logging.info(f"Input Image (first 20 chars): {image_base64[:20]}")
    image_bytes = base64.b64decode(image_base64)
    input_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # Ensure the image size is a multiple of 8
    new_width = input_image.width - input_image.width % 8
    new_height = input_image.height - input_image.height % 8
    input_image = input_image.resize((new_width, new_height), Image.LANCZOS)

    # Process image with the model
    time_start = time.time()
    with torch.no_grad():
        if model_name == "edge_to_image":
            canny = canny_from_pil(input_image, low_threshold, high_threshold)
            canny_viz_inv = Image.fromarray(255 - np.array(canny))
            buffer_canny = io.BytesIO()
            canny_viz_inv.save(buffer_canny, format="PNG")
            canny_bytes = buffer_canny.getvalue()
            c_t = F.to_tensor(canny).unsqueeze(0).cuda()
            if use_fp16:
                c_t = c_t.half()
            output_image = model(c_t, prompt)
        elif model_name == "sketch_to_image_stochastic":
            image_t = F.to_tensor(input_image) < 0.5
            c_t = image_t.unsqueeze(0).cuda().float()
            torch.manual_seed(seed)
            B, C, H, W = c_t.shape
            noise = torch.randn((1, 4, H // 8, W // 8), device=c_t.device)
            if use_fp16:
                c_t = c_t.half()
                noise = noise.half()
            output_image = model(
                c_t, prompt, deterministic=False, r=gamma, noise_map=noise
            )
        else:
            c_t = F.to_tensor(input_image).unsqueeze(0).cuda()
            if use_fp16:
                c_t = c_t.half()
            output_image = model(c_t, prompt)
        output_pil = transforms.ToPILImage()(output_image[0].cpu() * 0.5 + 0.5)
    logging.info(f"Time taken to process image: {time.time() - time_start}")

    # Save output image to buffer
    buffer = io.BytesIO()
    output_pil.save(buffer, format="PNG")
    output_bytes = buffer.getvalue()

    return base64.b64encode(output_bytes).decode("utf-8")


# Start the Runpod serverless function
runpod.serverless.start({"handler": handler})
