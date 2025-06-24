import os
import uuid
from io import BytesIO

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image
import numpy as np

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()



# Serve frontend static files
# app.mount("/", StaticFiles(directory="static", html=True), name="static")

# Stylize endpoint and all other logic...


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify your frontend: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the TF Hub model once
hub_module = hub.load('./ai')

# Mount the output folder for public access
os.makedirs("outputs", exist_ok=True)
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

# Load all style images from the folder
STYLE_FOLDER = "good_designs"
OUTPUT_FOLDER = "outputs"

def load_and_process_image(file_bytes_or_path, image_size=(256, 256)):
    if isinstance(file_bytes_or_path, (bytes, bytearray)):
        img = Image.open(BytesIO(file_bytes_or_path)).convert('RGB')
    else:
        img = Image.open(file_bytes_or_path).convert('RGB')
    
    img = img.resize(image_size)
    img = np.array(img) / 255.0
    img = tf.convert_to_tensor(img, dtype=tf.float32)
    img = img[tf.newaxis, ...]
    return img

def stylize_and_save(content_img, style_img, prefix):
    stylized_output = hub_module(tf.constant(content_img), tf.constant(style_img))[0]
    stylized_np = tf.squeeze(stylized_output).numpy()
    stylized_img = Image.fromarray((stylized_np * 255).astype(np.uint8))
    filename = f"{prefix}_{uuid.uuid4().hex[:8]}.jpg"
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    stylized_img.save(filepath)
    return f"/outputs/{filename}"

@app.post("/send_here")
async def stylize_image(image: UploadFile = File(...)):
    # Read uploaded content image
    content_data = await image.read()
    content_img = load_and_process_image(content_data, image_size=(384, 384))


    result_urls = []
    i = 3
    for style_name in os.listdir(STYLE_FOLDER):
        style_path = os.path.join(STYLE_FOLDER, style_name)
        try:
            style_img = load_and_process_image(style_path, image_size=(256, 256))
            i-=1
            if i <= 0: 
                break

            p= "http://localhost:8000"
            # [content, style]
            url1 = stylize_and_save(content_img, style_img, "cs")
            result_urls.append(p+url1)

            # [style, content] (reversed)
            url2 = stylize_and_save(style_img, content_img, "sc")
            result_urls.append(p+url2)

        except Exception as e:
            print(f"Skipping {style_path} due to error: {e}")
    print(result_urls)
    return JSONResponse(content = {"urls": result_urls}, status_code=200)
