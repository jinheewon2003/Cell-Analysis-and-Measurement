from PIL import Image, ImageFilter, ImageDraw
import numpy as np
from scipy.interpolate import splprep, splev
import cv2
import os
import csv

# Specify the folder name you want to create
folder_name = "aggregate_analysis"

# Set the path of your photos that you analyze
jpg_data = "./folder location"

# Create a new local folder system
folder_path = "./" + folder_name + "/"
result = folder_path + "results.csv"
color_correction = folder_path + "color_correction/"
choose_cell = folder_path + "choose_cell/"
large_bound = folder_path + "large_bound/"
choose_cell2 = folder_path + "choose_cell2/"
small_bound = folder_path + "RESULTING_PHOTOS/"

# Check if the folders exist, and create them if not
if not os.path.exists(folder_path):
    os.makedirs(jpg_data)
    os.makedirs(color_correction)
    os.makedirs(choose_cell)
    os.makedirs(large_bound)
    os.makedirs(choose_cell2)
    os.makedirs(small_bound)

    with open(result, 'w', newline='') as csvfile:
        fieldnames = ['File Name', 'Small Area (pixel)', 'Large Area (pixel)', 'Pixel Scale', 'Micron Scale', 'Small Area (micron)', 'Large Area (micron)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
else:
    print(f"Folder '{folder_name}' already exists locally, please choose another folder name unless it has already been set up")

def yellow_outline(input_path, output_path, threshold=5):
    # Open the image using PIL
    image = Image.open(input_path)

    # Convert the image to a NumPy array
    image_array = np.array(image)

    # Convert RGB to Lab color space for better color representation
    lab_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2Lab)

    # Extract the 'b' channel (yellow-blue) from Lab color space
    yellow_channel = lab_image[:, :, 2]

    # Compute the gradient magnitude using the Sobel operator
    grad_x = cv2.Sobel(yellow_channel, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(yellow_channel, cv2.CV_64F, 0, 1, ksize=3)
    gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)

    # Threshold the gradient magnitude to identify edges
    edge_mask = gradient_magnitude > threshold

    # Create an empty image
    output_image = np.zeros_like(image_array)

    # Copy pixels from the original image where the gradient is above the threshold
    output_image[edge_mask] = image_array[edge_mask]

    # Convert the NumPy array back to a PIL Image
    output_image_pil = Image.fromarray(output_image)

    # Save the result
    output_image_pil.save(output_path)

def yellow_connected_regions(input_path, output_path, threshold=8, connectivity=8):
    # Open the image using PIL
    image = Image.open(input_path)

    # Convert the image to a NumPy array
    image_array = np.array(image)

    # Convert RGB to Lab color space for better color representation
    lab_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2Lab)

    # Extract the 'b' channel (yellow-blue) from Lab color space
    yellow_channel = lab_image[:, :, 2]

    # Compute the gradient magnitude using the Sobel operator
    grad_x = cv2.Sobel(yellow_channel, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(yellow_channel, cv2.CV_64F, 0, 1, ksize=3)
    gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)

    # Threshold the gradient magnitude to identify edges
    edge_mask = gradient_magnitude > threshold

    # Use connected component analysis to label connected regions
    _, labels, stats, _ = cv2.connectedComponentsWithStats(edge_mask.astype(np.uint8), connectivity)

    # Sort the regions by area in descending order, only keeping regions with an area greater than min_area
    sorted_regions = sorted((x for x in range(1, stats.shape[0]) if stats[x, cv2.CC_STAT_AREA] > 15000), key=lambda x: stats[x, cv2.CC_STAT_AREA], reverse=True)

    # Find the label corresponding to the region with the average point closest to the center
    closest_to_center_label = min(sorted_regions, key=lambda x: np.linalg.norm(stats[x, :2] + stats[x, 2:4] // 2 - np.array(image_array.shape[:2]) // 2))

    # Create a mask for the region with the average point closest to the center
    closest_to_center_mask = labels == closest_to_center_label

    # Create an empty image
    output_image = np.zeros_like(image_array)

    # Copy pixels from the original image where the region is true
    output_image[closest_to_center_mask] = image_array[closest_to_center_mask]

    # Convert the NumPy array back to a PIL Image
    output_image_pil = Image.fromarray(output_image)

    # Save the result
    output_image_pil.save(output_path)

def draw_yellow_convex_hull(process, input_path, output_path, blur=(501,501), smooth_curve=0.8, threshold=0, epsilon0=0.005, hull_color=(0, 255, 0)):
    # Open the image using PIL
    image = Image.open(input_path)

    white_image = Image.new("RGB", image.size, (0, 0, 255))
    black_image = Image.new("RGB", image.size, (255, 255, 255))
    draw = ImageDraw.Draw(white_image)

    # Convert the image to a NumPy array
    image_array = np.array(image)

    # Compute the sum of RGB values for each pixel
    rgb_sum = np.sum(image_array, axis=-1)

    # Create a mask for pixels containing a trace of non-black
    non_black_mask = rgb_sum > 0

    # Draw the black pixels on the new image
    white_image_array = np.array(white_image)
    black_image_array = np.array(black_image)
    white_image_array[non_black_mask] = black_image_array[non_black_mask]
    white_image = Image.fromarray(white_image_array)

    # Convert the image to a NumPy array
    image_array = cv2.GaussianBlur(white_image_array, blur, 0)

    # Convert RGB to Lab color space for better color representation
    lab_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2Lab)

    # Extract the 'b' channel (yellow-blue) from Lab color space
    yellow_channel = lab_image[:, :, 2]

    # Compute the gradient magnitude using the Sobel operator
    grad_x = cv2.Sobel(yellow_channel, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(yellow_channel, cv2.CV_64F, 0, 1, ksize=3)
    gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)

    # Threshold the gradient magnitude to identify edges
    edge_mask = gradient_magnitude > threshold

    # Use connected component analysis to label connected regions
    _, labels, stats, _ = cv2.connectedComponentsWithStats(edge_mask.astype(np.uint8), connectivity=8)

    # Find the label corresponding to the largest connected region (excluding background)
    largest_region_label = np.argmax(stats[1:, cv2.CC_STAT_AREA]) + 1

    # Find the contour of the largest connected region
    largest_region_contour, _ = cv2.findContours((labels == largest_region_label).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Approximate the contour with a convex hull using a fixed number of points
    epsilon = epsilon0 * cv2.arcLength(largest_region_contour[0], True)
    convex_hull = cv2.approxPolyDP(largest_region_contour[0], epsilon, True)

    points = convex_hull.squeeze()

    # Use scipy to interpolate a smooth curve
    tck, _ = splprep(points.T, s=smooth_curve)
    smoothed_points = splev(np.linspace(0, 1, 100), tck)


    # Create a contour from the smoothed points
    smoothed_contour = np.array(list(zip(smoothed_points[0], smoothed_points[1])), dtype=np.int32)

    # Calculate the area of the smoothed contour
    smoothed_area = cv2.contourArea(smoothed_contour)

    # Open Image
    process = Image.open(process)

    # Draw the smoothed curve on the image using PIL
    draw = ImageDraw.Draw(process)
    draw.line(list(zip(smoothed_points[0], smoothed_points[1])), fill=hull_color, width=5)

    # Save the result
    process.save(output_path)
    return smoothed_area
