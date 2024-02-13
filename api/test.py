import numpy as np
from PIL import Image

from ai import generate_10_images
import  matplotlib.pyplot as plt

# Load the sketch and real images

sketch_path= 'api/sketch.png'

sketch_image = Image.open(sketch_path)

# Resize the images to the model's input size (256x256)
sketch_image = sketch_image.resize((256, 256))

# Normalize the images to the range [-1, 1]
sketch_array = np.array(sketch_image) / 127.5 - 1.0

# Add batch dimension to the images
sketch_array = np.expand_dims(sketch_array, axis=0)


def test_1():
    # Create an array to store predictions
    predictions = generate_10_images(sketch_array)

    # Create a subplot grid
    fig, axes = plt.subplots(4, 3, figsize=(9, 12))

    # Iterate through predictions and plot each image
    for i in range(10):
        row = i // 3
        col = i % 3
        img = (predictions[i] * 255).astype(np.uint8)
        
        axes[row, col].imshow(img)
        axes[row, col].axis('off')

    plt.tight_layout()
    plt.show()
    # Save the combined image
    plt.savefig("combined_predictions.jpg")

def test2():
    import time
    import json
    from PIL import Image

    # Assuming generate_10_images returns a list of images

    def save_images_and_return_filenames(images):
        # Get the current timestamp for filename uniqueness
        timestamp = int(time.time())

        # List to store the generated filenames
        filenames = []

        for i, img in enumerate(images):
            # Create a unique filename based on timestamp and index
            filename = f"gGen_{timestamp}_{i}.png"
            filenames.append(filename)

            # Convert the image to PIL Image (assuming 'img' is a NumPy array)
            pil_image = Image.fromarray((img * 255).astype(np.uint8))

            # Save the image
            pil_image.save(filename)

        # Convert the list of filenames to JSON
        response_json = json.dumps({"filenames": filenames})

        return response_json

    # Example usage
    outputs = generate_10_images(sketch_array)
    json_response = save_images_and_return_filenames(outputs)

    print(json_response)

test_1()