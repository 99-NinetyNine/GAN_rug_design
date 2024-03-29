from django.http import HttpResponse
from django.shortcuts import render
from .forms import ImageUploadForm
from .ai import generate_10_images
from .ai_falgun import get_2_nice_designs

from PIL import Image
import numpy as np


import matplotlib.pyplot as plt

import base64
import numpy as np



from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
import time
from django.conf import settings

import io
import os
# Function to resize an image
# Function to resize an image
def t(r):
    return render(r,'f.html',{})

def resize_image(image_content, target_size=(256, 256, 3)):
    # Create an in-memory file-like object from the uploaded content
    image_in_memory = Image.open(io.BytesIO(image_content))

    # Resize the image
    resized_img = image_in_memory.resize(target_size[:2])

    # If the image has an alpha channel, remove it
    if target_size[2] == 3 and image_in_memory.mode == 'RGBA':
        resized_img = resized_img.convert('RGB')
    
    # Use current timestamp as a unique filename
    timestamp = int(time.time())
    filename = f'{timestamp}.jpg'

    # Construct the full path using Django's settings
    save_path = os.path.join(settings.MEDIA_ROOT, 'user_uploads', filename)

    # Save the resized image to the full path
    resized_img.save(save_path)

    return resized_img, save_path



    
@csrf_exempt
def IndexView(request, *args, **kwargs):
    if request.method == 'GET':
        # Return a JSON response with the form data
        form = ImageUploadForm()
        return JsonResponse({'image': "upload a image"}, safe=False)

    elif request.method == 'POST':
        # Handle form submission
        form = ImageUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            print("ok")
            # Process the image and generate output
            image_content = form.cleaned_data['image'].read()
            # Resize the image
            resized_image, saved_path = resize_image(image_content, target_size=(256, 256, 3))

            # Convert the resized image to a NumPy array
            img_array=np.array(resized_image)
            resized_array = np.expand_dims(img_array/255., axis=0)

            # Generate output using the processed image
            
            #return JsonResponse({'image': "upload a image"}, safe=False)
            print(saved_path)
            ##DCGAN
            #filenames_100    = generate_10_images(resized_array)
            

            ##pix2pix model
            filenames_400 =   get_2_nice_designs(saved_path)
                
            filenames=[]
            timestamp = int(time.time())
            for index,stylized_image in enumerate(filenames_400):
                # Visualize input images and the generated stylized image.

                filename = f"style_{timestamp}_{index}.jpg"
                filenames.append(filename)
                
                

                # Construct the full path including the base path
                filepath = os.path.join(settings.MEDIA_ROOT, 'generated_files', filename)

                # Ensure the folder exists
                os.makedirs(os.path.dirname(filepath), exist_ok=True)

                # Save the stylized image using tf.keras.preprocessing.image.save_img
                from tensorflow.keras.preprocessing.image import save_img
                save_img(filepath, stylized_image)
            
            urls = []
            for filename in filenames:
                x   =   'http://127.0.0.1:8000/media/generated_files/'+filename
                urls.append(x)
                
            json_response = {
                "status":True,
                "urls":urls,
            }
            
            
            # Return the URL of the saved image
            return JsonResponse(json_response, status=200, safe=False)
        
        else:
            print(form.errors, "not ok")
            # Form is not valid, return an error response
            return JsonResponse({'error': 'Form is not valid'}, status=400)

    else:
        # Handle other HTTP methods (e.g., PUT, DELETE)
        return JsonResponse({'error': 'Method not allowed'}, status=405)



@csrf_exempt
def IndexFunnyView(request, *args, **kwargs):
    if request.method == 'GET':
        # Return a JSON response with the form data
        form = ImageUploadForm()
        return JsonResponse({'image': "upload a image"}, safe=False)

    elif request.method == 'POST':
        from .forms import FunImageUploadForm
        from .fun import get_fun_designs
        # Handle form submission
        form = FunImageUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            print("ok")
            # Process the image and generate output
            image_content = form.cleaned_data['image'].read()
            image_content_2=form.cleaned_data['image_2'].read()
            # Resize the image
            resized_image, saved_path = resize_image(image_content, target_size=(256, 256, 3))
            resized_image2, saved_path2 = resize_image(image_content_2, target_size=(256, 256, 3))
            filenames_400 =   get_fun_designs(saved_path,saved_path2)
                
            filenames=[]
            timestamp = int(time.time())
            for index,stylized_image in enumerate(filenames_400):
                # Visualize input images and the generated stylized image.

                filename = f"style_{timestamp}_{index}.jpg"
                filenames.append(filename)
                
                

                # Construct the full path including the base path
                filepath = os.path.join(settings.MEDIA_ROOT, 'generated_files', filename)

                # Ensure the folder exists
                os.makedirs(os.path.dirname(filepath), exist_ok=True)

                # Save the stylized image using tf.keras.preprocessing.image.save_img
                from tensorflow.keras.preprocessing.image import save_img
                save_img(filepath, stylized_image)
            
            urls = []
            for filename in filenames:
                x   =   'http://127.0.0.1:8000/media/generated_files/'+filename
                urls.append(x)
                
            json_response = {
                "status":True,
                "urls":urls,
            }
            
            
            # Return the URL of the saved image
            return JsonResponse(json_response, status=200, safe=False)
        
        else:
            print(form.errors, "not ok")
            # Form is not valid, return an error response
            return JsonResponse({'error': 'Form is not valid'}, status=400)

    else:
        # Handle other HTTP methods (e.g., PUT, DELETE)
        return JsonResponse({'error': 'Method not allowed'}, status=405)
