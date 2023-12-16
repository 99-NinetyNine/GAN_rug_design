import numpy as np
from PIL import Image

from ai import generator
import  matplotlib.pyplot as plt

# Load the sketch and real images
real_path = '/home/sailesh/Documents/8th/api/api/real_11.png'
sketch_path= '/home/sailesh/Documents/8th/api/api/sketch.png'

sketch_image = Image.open(sketch_path)
real_image = Image.open(real_path).convert("RGB")

# Resize the images to the model's input size (256x256)
sketch_image = sketch_image.resize((256, 256))
real_image = real_image.resize((256, 256))

# Normalize the images to the range [-1, 1]

sketch_array = np.array(sketch_image) / 255.0
real_array = np.array(real_image) / 127.5 - 1.0

# # Add batch dimension to the images
sketch_array = np.expand_dims(sketch_array, axis=0)
# real_array = np.expand_dims(real_array, axis=0)

# # Generate the predicted image using the generator
predicted_image = generator(sketch_array,training=True)
normalized_prediction = (predicted_image * 0.5) + 0.5
squeezed_prediction = np.squeeze(normalized_prediction, axis=0)



# # Display the images
plt.figure(figsize=(15, 5))

# # Original Sketch
plt.subplot(1, 3, 1)
plt.title("Sketch")
plt.imshow(sketch_array[0] * 0.5 + 0.5)

plt.axis("off")

# # Ground Truth (Real Image)
# plt.subplot(1, 3, 2)
# plt.title("Ground Truth (Real)")
# plt.imshow(real_array[0] * 0.5 + 0.5)
# plt.axis("off")

# # Predicted Image
plt.subplot(1, 3, 3)
plt.title("Predicted Image")
plt.imshow(squeezed_prediction)
plt.axis("off")

# plt.savefig("f.png")
plt.savefig("wtf.png")
