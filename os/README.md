## Usage

### 1. Set Up Google Drive Folder

Specify the folder name you want to create. The script creates a new folder system in Google Drive with the following structure:

- `results.csv`: CSV file to store analysis results.
- `ADD_PHOTOS_HERE/`: Placeholder folder for your input photos.
- `color_correction/`: Folder for images after removing all colors except yellow.
- `choose_cell/`: Folder for images with connected yellow regions.
- `large_bound/`: Folder for images with convex hulls around the largest yellow region.
- `choose_cell2/`: Folder for images with connected yellow regions after the first analysis.
- `RESULTING_PHOTOS/`: Folder for images with convex hulls around smaller yellow regions.

### 2. Yellow Outline Detection

The `yellow_outline` function processes input photos, removes all colors except yellow, and saves the result in the `color_correction` folder.

### 3. Yellow Connected Regions

The `yellow_connected_regions` function identifies connected yellow regions in images, and the result is saved in the `choose_cell` and `choose_cell2` folders.

### 4. Yellow Convex Hulls

The `draw_yellow_convex_hull` function draws convex hulls around yellow regions and saves the result in the `large_bound` and `RESULTING_PHOTOS` folders. Adjust parameters such as blur, epsilon, and smooth_curve for desired results.

### 5. Image Analysis Loop

The script iterates through the photos in the `ADD_PHOTOS_HERE/` folder, applies the outlined processes, and updates the `results.csv` file with the analysis results.

**Note:** Add your photos to the `ADD_PHOTOS_HERE/` folder before running the script.

## Getting Started

1. Clone this repository:

    ```bash
    git clone https://github.com/your-username/your-repository.git
    ```

2. Upload your photos to the `ADD_PHOTOS_HERE/` folder.
3. Run the script in a Jupyter notebook or Google Colab environment.

## Structure

- `aggregate_analysis.ipynb`: Jupyter notebook containing the analysis script.
- `LICENSE`: Choose an open-source license for your project.
- `README.md`: Instructions and information about the project.
- `.gitignore`: Specify files and folders to be ignored by Git (e.g., `__pycache__/`, `.ipynb_checkpoints/`, etc.).
