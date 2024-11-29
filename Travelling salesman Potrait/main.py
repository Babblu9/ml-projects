import os
import math
import matplotlib.pyplot as plt
import numpy as np
import urllib.request
from PIL import Image
from tsp_solver.greedy_numpy import solve_tsp 
from scipy.spatial.distance import pdist, squareform

# Image URL and local path
image_url = 'https://github.com/aschinchon/travelling-salesman-portrait'
image_path = 'C:/Users/Sai Kumar/Downloads/franklin.jpeg'

# Download the image if it doesn't exist
if not os.path.exists(image_path):
    urllib.request.urlretrieve(image_url, image_path)

# Load and process the image
original_image = Image.open(image_path)
bw_image = original_image.convert('1', dither=Image.NONE)

# Convert to a NumPy array and find black pixel indices
bw_image_array = np.array(bw_image, dtype=int)  # Changed from np.int to int
black_indices = np.argwhere(bw_image_array == 0)

# Randomly sample 10,000 black pixels
chosen_black_indices = black_indices[np.random.choice(black_indices.shape[0], replace=False, size=5000)]

# Compute pairwise distances and solve the Traveling Salesman Problem
distances = pdist(chosen_black_indices)
distance_matrix = squareform(distances)
optimized_path = solve_tsp(distance_matrix)

# Extract optimized path points
optimized_path_points = [chosen_black_indices[x] for x in optimized_path]

# Plot the Traveling Salesman Portrait
plt.figure(figsize=(8, 10), dpi=100)
plt.plot([x[1] for x in optimized_path_points], [x[0] for x in optimized_path_points], color='black', lw=1)
plt.xlim(0, 600)
plt.ylim(0, 800)
plt.gca().invert_yaxis()
plt.xticks([])
plt.yticks([])
plt.savefig('traveling-salesman-portrait.png', bbox_inches='tight')
plt.show()
