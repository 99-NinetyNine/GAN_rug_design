from collections import Counter
from typing import Callable, Tuple, Optional, Union, List, Type
from PIL import Image
import cv2
import numpy as np

MAX_SIZE = 500

import os
from django.conf import settings

def generate_random_string(length):
    import random
    import string
    # Define the characters to choose from for the random string
    characters = string.ascii_letters + string.digits  # You can add other characters if needed
    
    # Generate the random string by choosing characters randomly from the defined set
    random_string = ''.join(random.choice(characters) for _ in range(length))
    
    return random_string

# Example usage: Generate a random string of length 10
random_string = generate_random_string(10)


def test_pillow(
    img_input: Image.Image, method: int
) -> Tuple[Type[Image.Image], List[List[int]]]:
    img: Image.Image = img_input.copy()
    img.thumbnail((MAX_SIZE, MAX_SIZE), Image.NEAREST)

    threshold_pixel_percentage: float = 0.05
    nb_colours: int = 20
    nb_colours_under_threshold: int
    nb_pixels: int = img.width * img.height
    quantized_img: Image.Image

    while True:
        # method 0 = median cut 1 = maximum coverage 2 = fast octree
        quantized_img = img.quantize(colors=nb_colours, method=method, kmeans=0)
        nb_colours_under_threshold = 0
        colours_list: [Tuple[int, int]] = quantized_img.getcolors(nb_colours)
        for (count, pixel) in colours_list:
            if count / nb_pixels < threshold_pixel_percentage:
                nb_colours_under_threshold += 1
        if nb_colours_under_threshold == 0:
            break
        nb_colours -= -(-nb_colours_under_threshold // 2)  # ceil integer division
    palette: [int] = quantized_img.getpalette()
    colours_list: [[int]] = [palette[i : i + 3] for i in range(0, nb_colours * 3, 3)]
    return quantized_img, colours_list


def test_pillow_median_cut(
    img_input: Image.Image
) -> Tuple[Type[Image.Image], List[List[int]]]:
    return test_pillow(img_input, 0)


def get_img_data(
    img_input: Image.Image,
    mini: bool = False,
    conversion_method: int = cv2.COLOR_RGB2BGR,
) -> Tuple[np.ndarray, int, np.ndarray]:
    img: np.ndarray = cv2.cvtColor(np.array(img_input), conversion_method)
    ratio: float = min(
        MAX_SIZE / img.shape[0], MAX_SIZE / img.shape[1]
    )  # calculate ratio
    if mini:
        ratio /= 6
    img = cv2.resize(img, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_AREA)

    nb_pixels: int = img.size

    flat_img: np.ndarray = img.reshape((-1, 3))
    flat_img: np.ndarray = np.float32(flat_img)
    return img, nb_pixels, flat_img


def process_result(
    center: np.ndarray,
    label: np.ndarray,
    shape: Tuple[int, int, int],
    conversion_method: int = cv2.COLOR_BGR2RGB,
) -> Tuple[Type[Image.Image], np.ndarray]:
    center: np.ndarray = np.uint8(center)
    quantized_img: np.ndarray = center[label]
    quantized_img = quantized_img.reshape(shape)
    quantized_img = cv2.cvtColor(quantized_img, conversion_method)
    center = cv2.cvtColor(np.expand_dims(center, axis=0), conversion_method)[0]
    return Image.fromarray(quantized_img), center


def update_nb_colours(
    label: np.ndarray,
    nb_pixels: int,
    threshold_pixel_percentage: float,
    nb_colours: int,  # , flat_img: np.ndarray
) -> Tuple[int, int]:
    nb_colours_under_threshold: int = 0
    label = label.flatten()
    colour_count: Counter[int] = Counter(label)
    for (pixel, count) in colour_count.items():
        if count / nb_pixels < threshold_pixel_percentage:
            nb_colours_under_threshold += 1
    # silhouette = sklearn.metrics.silhouette_score(flat_img, label, metric='euclidean', sample_size=1000)
    # print(f'nb_colours = {nb_colours}, silhouette_score = {silhouette}')
    nb_colours -= -(-nb_colours_under_threshold // 2)  # ceil integer division
    return nb_colours, nb_colours_under_threshold


def create_colour_list_image(
    colours_list: List[Tuple[int]], img_name: str, quantize_function_name: str
) -> str:
    h, w = (25, 20)
    colour_img: Image.Image = Image.new("RGB", (w * len(colours_list), h))
    colours_list: List[Tuple[int, int, int]] = sum(
        [[tuple(colour)] * w for colour in colours_list] * h, []
    )
    colour_img.putdata(colours_list)
    
    # Construct the file path relative to the media directory
    r=generate_random_string(10)
    save_path = os.path.join('palette', f'test_colours_{r}_{quantize_function_name}.png')
    full_save_path = os.path.join(settings.MEDIA_ROOT, save_path)
    
    # Save the image
    colour_img.save(full_save_path)
    
    # Return the relative file path
    return save_path


def create_images_results(imgs: [str], quantize_functions: [str]) -> None:
    for img_name in imgs:
        _img: Image.Image = Image.open(img_name)
        for quantize_function_name in quantize_functions:
            func_name = "test_" + quantize_function_name
            quantized_img, colours_list = eval(f"{func_name}(_img)")
            r=generate_random_string(10)
            save_path = os.path.join('palette', f'test_img_{r}_{quantize_function_name}.png')
            full_save_path = os.path.join(settings.MEDIA_ROOT, save_path)        
    
            quantized_img.save(#save in /media/palltte folder. path upto media obtained from settings.
                full_save_path
            )
            f2=create_colour_list_image(colours_list, img_name, quantize_function_name)
            return (save_path, f2)



#given "/media/generated_files/style_1708224153_2.jpg'
#combine with media with base dir to get full path            
#create_images_results(["/home/s/p/GAN_rug_design"+"/media/generated_files/style_1708224153_2.jpg",], ["pillow_median_cut",])