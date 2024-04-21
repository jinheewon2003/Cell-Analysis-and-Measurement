## Usage Instructions

### 1. Download the Script

1. Download the script file [here](https://github.com/jinheewon2003/Cell-Analysis-and-Measurement/blob/main/os/image_analysis.py).

### 2. Prerequisites

Ensure you have the following libraries installed on your local machine:

- Pillow (PIL): `pip install pillow`
- NumPy: `pip install numpy`
- SciPy: `pip install scipy`
- OpenCV: `pip install opencv-python`

### 3. Configure File Paths

1. Open the downloaded script file in a text editor.

2. Locate the following variables at the beginning of the script:

    ```python
    # Specify the folder name you want to create
    folder_name = "aggregate_analysis"

    # Set the path of your photos that you analyze
    jpg_data = "./folder_location"

    # Set the local folder path for results
    folder_path = "./" + folder_name + "/"
    ```

3. Update `folder_name` to the name of the folder you want to be created.
4. Update `jpg_data` to the directory path where your photos are located.
5. Update `folder_path` to the local directory path where you want the folder of results to be created.

### 4. Run the Script

1. Open a terminal and navigate to the folder containing the downloaded script:

    ```bash
    cd /path/to/downloaded/script
    ```

2. Run the script:

    ```bash
    python script_name.py
    ```

Replace `script_name.py` with the actual name of your downloaded script file.

The script will process the photos, extract yellow regions, identify connected components, draw convex hulls, and save the results in the specified local folder.

## Structure

- `image_analysis.ipynb`: Python file containing the analysis script.
- `LICENSE`: Choose an open-source license for your project.
- `README.md`: Instructions and information about the project.
