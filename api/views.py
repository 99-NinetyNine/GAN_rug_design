from django.http import HttpResponse
from django.shortcuts import render
from .forms import ImageUploadForm
from .ai import generate_images

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
def ApiView(request, *args, **kwargs):
    if request.method == 'GET':
        # Display the form
        form = ImageUploadForm()
        return render(request, 'index.html', {'form': form})

    elif request.method == 'POST':
        # Handle form submission
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the image and generate output
            image_content = form.cleaned_data['image'].read()

            # Resize the image
            resized_image = resize_image(image_content, target_size=(256, 256, 3))

            # Convert the resized image to a NumPy array
            
            resized_array = np.expand_dims(np.array(resized_image), axis=0)


            
            output = generate_images(resized_array)

            import base64

            plt.figure()
            plt.imshow(output[0])  # Assuming output[0] is a NumPy array representing the image
            plt.axis('off')
            
            # Save the Matplotlib plot to a BytesIO object
            output_image_bytesio = io.BytesIO()
            plt.savefig(output_image_bytesio, format='png', bbox_inches='tight')
            plt.close()

            # Convert the BytesIO object to a base64 string
            output_image_base64 = base64.b64encode(output_image_bytesio.getvalue()).decode('utf-8')

            input_image_base64 = base64.b64encode(resized_image.tobytes()).decode('utf-8')
            #output_image_base64 = base64.b64encode(output[0].numpy().tobytes()).decode('utf-8')
    

            # Pass input and output images to the template
            return render(request, 'output.html', {'input_image': input_image_base64, 'output_image': output_image_base64})
        else:
            # Form is not valid, handle the error
            return HttpResponse("Form is not valid", status=400)

    else:
        # Handle other HTTP methods (e.g., PUT, DELETE)
        return HttpResponse("Method not allowed", status=405)







import base64
import numpy as np



from django.http import JsonResponse

def IndexView(request, *args, **kwargs):
    if request.method == 'GET':
        # Return a JSON response with the form data
        form = ImageUploadForm()
        return JsonResponse({'form': form.fields}, safe=False)

    elif request.method == 'POST':
        # Handle form submission
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the image and generate output
            image_content = form.cleaned_data['image'].read()

            # Resize the image
            resized_image = resize_image(image_content, target_size=(256, 256, 3))

            # Convert the resized image to a NumPy array
            resized_array = np.expand_dims(np.array(resized_image), axis=0)

            # Generate output using the processed image
            output = generate_images(resized_array)

            # Convert the output image to a base64 string
            output_image_base64 = base64.b64encode(output.numpy().tobytes()).decode('utf-8')

            input_image_base64 = base64.b64encode(resized_image.tobytes()).decode('utf-8')

            # Return a JSON response with the input and output images
            return JsonResponse({'input_image': input_image_base64, 'output_image': output_image_base64})

        else:
            # Form is not valid, return an error response
            return JsonResponse({'error': 'Form is not valid'}, status=400)

    else:
        # Handle other HTTP methods (e.g., PUT, DELETE)
        return JsonResponse({'error': 'Method not allowed'}, status=405)
