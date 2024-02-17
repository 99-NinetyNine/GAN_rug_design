import functools
import os

from matplotlib import gridspec
import matplotlib.pylab as plt
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

print("TF Version: ", tf.__version__)
print("TF Hub version: ", hub.__version__)
print("Eager mode enabled: ", tf.executing_eagerly())
print("GPU available: ", tf.config.list_physical_devices('GPU'))


# @title Define image loading and visualization functions  { display-mode: "form" }

def crop_center(image):
  """Returns a cropped square image."""
  shape = image.shape
  new_shape = min(shape[1], shape[2])
  offset_y = max(shape[1] - shape[2], 0) // 2
  offset_x = max(shape[2] - shape[1], 0) // 2
  image = tf.image.crop_to_bounding_box(
      image, offset_y, offset_x, new_shape, new_shape)
  return image

@functools.lru_cache(maxsize=None)
def load_image(image_url, image_size=(256, 256), preserve_aspect_ratio=True):
  """Loads and preprocesses images."""
  # Cache image file locally.
  #image_path = tf.keras.utils.get_file(os.path.basename(image_url)[-128:], image_url)
  # Load and convert to float32 numpy array, add batch dimension, and normalize to range [0, 1].
  img = tf.io.decode_image(
      tf.io.read_file(image_url),
      channels=3, dtype=tf.float32)[tf.newaxis, ...]
  img = crop_center(img)
  img = tf.image.resize(img, image_size, preserve_aspect_ratio=True)
  return img

def show_n(images, titles=('',)):
  n = len(images)
  image_sizes = [image.shape[1] for image in images]
  w = (image_sizes[0] * 6) // 320
  plt.figure(figsize=(w * n, w))
  gs = gridspec.GridSpec(1, n, width_ratios=image_sizes)
  for i in range(n):
    plt.subplot(gs[i])
    plt.imshow(images[i][0], aspect='equal')
    plt.axis('off')
    plt.title(titles[i] if len(titles) > i else '')
  plt.show()


def get_some_random_designs(some=10):
    import glob
    import random

    directory_path = '../media/good_designs'
    files = glob.glob(os.path.join(directory_path, '*'))

    
    if not files:
        print(f"No files found in directory: {directory_path}")
        return None
    num_files = min(some, len(files))
    random_files = random.sample(files, num_files)

    return random_files


import time
# @title Load example images  { display-mode: "form" }
def get_2_nice_designs(image):
  ## we style the image randomly by selecting one of design of pinterst
  ## And user may like (S= his design, C= Pinterst ) or reverse
  ## these are two diffrent results as seen in Colab during experimentaion
    ##CONSTANTS
    style_img_size = (256, 256)  # Recommended to keep it at 256.
    output_image_size = 400  # @param {type:"integer"}
    content_img_size = (output_image_size, output_image_size)
    

    # Load TF Hub module.
    import os
    from django.conf import settings
    model_path = os.path.join(settings.BASE_DIR, 'api/model/')
    hub_module = hub.load(model_path)

    ##URL SPECIFICATIONS
    style_images = get_some_random_designs()

    if style_images is not None:
        imgs    = style_images
    else:
       imgs = [image,] ##just some fallback ##change later r,n. no better ideas in my mind
    
    pair_A  =   [(image, item) for item in imgs]
    pair_B  =   [(item, image) for item in imgs]
    
    image_pairs = pair_A + pair_B
    
    
    ###OUTPUT 
    output_filenames    =   []
    for content_image_url, style_image_url in image_pairs:
        content_image = load_image(content_image_url, content_img_size)
        style_image = load_image(style_image_url, style_img_size)
        style_image = tf.nn.avg_pool(style_image, ksize=[3,3], strides=[1,1], padding='SAME')
        
        # Stylize content image with given style image.
        # This is pretty fast within a few milliseconds on a GPU.

        outputs = hub_module(tf.constant(content_image), tf.constant(style_image))
        stylized_image = tf.squeeze(outputs[0], axis=0)


        # Visualize input images and the generated stylized image.
        timestamp = int(time.time())

        filename = f"stylized_{timestamp}.jpg"

        # Construct the full path including the base path
        filepath = os.path.join(settings.MEDIA_ROOT, 'generated_files', filename)

        # Ensure the folder exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Save the stylized image using tf.keras.preprocessing.image.save_img
        tf.keras.preprocessing.image.save_img(filepath, stylized_image)
        
        output_filenames.append(filepath)
        
    
    return output_filenames
        
