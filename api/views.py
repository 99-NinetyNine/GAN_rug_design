from django.http import HttpResponse
from django.shortcuts import render
from .forms import ImageUploadForm
#from .ai import generate_10_images

from PIL import Image
import numpy as np

import io
# Function to resize an image
# Function to resize an image
def resize_image(image_content, target_size=(256, 256, 3)):
    # Create an in-memory file-like object from the uploaded content
    image_in_memory = Image.open(io.BytesIO(image_content))

    # Resize the image
    resized_img = image_in_memory.resize(target_size[:2])

    # If the image has an alpha channel, remove it
    if target_size[2] == 3 and image_in_memory.mode == 'RGBA':
        resized_img = resized_img.convert('RGB')

    return resized_img


import matplotlib.pyplot as plt

import base64
import numpy as np



from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
import time
    
@csrf_exempt
def IndexView(request, *args, **kwargs):
    if request.method == 'GET':
        # Return a JSON response with the form data
        form = ImageUploadForm()
        return JsonResponse({'image': "upload a image"}, safe=False)

    elif request.method == 'POST':
        # Handle form submission
        form = ImageUploadForm(request.POST, request.FILES)
        
        print(form)
        if form.is_valid():
            # Process the image and generate output
            image_content = form.cleaned_data['image'].read()
            # Resize the image
            resized_image = resize_image(image_content, target_size=(256, 256, 3))

            # Convert the resized image to a NumPy array
            img_array=np.array(resized_image)
            resized_array = np.expand_dims(img_array/255., axis=0)

            # Generate output using the processed image
            outputs = generate_10_images(resized_array)

            # Get the current timestamp for filename uniqueness
            timestamp = int(time.time())

            # List to store the generated filenames
            filenames = []

            for i, img in enumerate(outputs):
                # Create a unique filename based on timestamp and index
                filename = f"media/gGen_{timestamp}_{i}.png"
                filenames.append(filename)

                # Convert the image to PIL Image (assuming 'img' is a NumPy array)
                pil_image = Image.fromarray((img * 255).astype(np.uint8))

                # Save the image
                pil_image.save(filename)


            json_response = {
                "status":True,
                "urls":['http://127.0.0.1:8000/'+ fName for fName in filenames],
            }
            
            # Return the URL of the saved image
            return JsonResponse(json_response, status=200, safe=False)
        
        else:
            print(form.errors)
            # Form is not valid, return an error response
            return JsonResponse({'error': 'Form is not valid'}, status=400)

    else:
        # Handle other HTTP methods (e.g., PUT, DELETE)
        return JsonResponse({'error': 'Method not allowed'}, status=405)
