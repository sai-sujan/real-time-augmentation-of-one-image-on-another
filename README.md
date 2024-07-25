# Real-Time Augmentation of Videos onto Physical Images

This project implements real-time augmentation of videos (or images) onto physical images.

## Usage

### Prerequisites

- Python 3.x
- OpenCV
- NumPy

### Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo-name/real-time-augmentation.git
    cd real-time-augmentation
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Create Folders:

    - Create two folders in the project directory:
        - `Imagesquery`: Upload the images that are physically available to you.
        - `Testvideos1`: Upload the same number of videos (or images) that correspond to the images in the `Imagesquery` folder.

4. Run the Program:

    - Execute the script:
        ```bash
        python augment.py
        ```

    - When you run the program, if you show the first image from the `Imagesquery` folder to your webcam, it will augment the first video from the `Testvideos1` folder onto the physical image.

    - If you upload images to the `Testvideos1` folder instead of videos, the program can be modified to handle image formats.
    """
