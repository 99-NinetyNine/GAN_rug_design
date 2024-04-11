from django.http import HttpResponse
from django.shortcuts import render
from .forms import ImageUploadForm,ImageUploadFileForm
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

def t2(r):
    return render(r,'f3.html',{})

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
            index   =   int(form.cleaned_data.get("index",0))
            print(index,"index was")
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
            filenames_400 =   get_2_nice_designs(saved_path,index)
                
            filenames=[]
            import random
            import string

            def generate_random_string(length):
                # Define the characters to choose from for the random string
                characters = string.ascii_letters + string.digits  # You can add other characters if needed
                
                # Generate the random string by choosing characters randomly from the defined set
                random_string = ''.join(random.choice(characters) for _ in range(length))
                
                return random_string

            # Example usage: Generate a random string of length 10
            random_string = generate_random_string(10)
            for index,stylized_image in enumerate(filenames_400):
                # Visualize input images and the generated stylized image.

                filename = f"style_+"+random_string+f"_{index}.jpg"
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
                "next_index":int(index)+5,
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





import os
from django.conf import settings





    
@csrf_exempt
def PaletteView(request, *args, **kwargs):
    if request.method == 'GET':
        # Return a JSON response with the form data
        form = ImageUploadFileForm()
        return JsonResponse({'image': "upload a image"}, safe=False)

    elif request.method == 'POST':
        # Handle form submission
        form = ImageUploadFileForm(request.POST, request.FILES)
        
        if form.is_valid():
            #/generated_files/filename all
            image_path_name = form.cleaned_data['filename_to_render_as_palette']
            #//
            from .palette import create_images_results
            
            full_save_path = os.path.join(settings.MEDIA_ROOT, image_path_name)
            print("full path", full_save_path, type(full_save_path))

            arg1=[full_save_path,]
            arge2=["pillow_median_cut",]
            filenames   =   create_images_results(arg1, arge2)
            urls = []
            for filename in filenames:
                x   =   'http://127.0.0.1:8000/media/'+filename
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


