# Camera Capture Tool
This is a simple, multi-language Python application that allows you to capture photos from your webcam quickly. It features a user-friendly graphical interface (GUI) built with tkinter, enabling you to select an output folder, choose your camera by index, and capture images with a single key press.

## Features

- Live Camera Preview: Displays a real-time video feed from your selected camera.
- Multi-Language Interface: Supports both English and Chinese, selectable at startup.
- Custom Output Folder: Choose any directory on your system to save your captured photos.
- Camera Index Selection: Easily switch between multiple connected cameras by entering their numerical index (e.g., 0, 1, 2...).
- Quick Capture: Press the Spacebar to take a photo of the current frame instantly.
- Automatic File Naming: Photos are automatically named with a timestamp and sequence number to prevent overwrites (e.g., photo_YYYYMMDD_HHMMSS_0001.jpg).
- Exit Shortcut: Press the ESC key to quickly close the application.

## Prerequisites

Before running the application, ensure you have the following installed:
- Python 3.x
- pip (Python package installer, usually comes with Python)

## Installation

1. Save the Source Code:
Create a new file named `main.py` (or any other .py name you prefer) and paste the entire source code provided below into this file.
2. Install Required Libraries:
Open your terminal or command prompt and run the following command to install `OpenCV` and `Pillow`:
```
pip install opencv-python Pillow
```

## Usage

1. Run the Application:
Navigate to the directory where you saved `main.py` in your terminal or command prompt, then execute the script:
```
python main.py
```
2. Language Selection:
Upon launching, a dialog box will appear asking for your preferred interface language.
- Click "Yes" for `English`.
- Click "No" for `Chinese`.
3. Select Output Folder:
Click the "Select Folder" (或 "選擇資料夾") button at the top. Choose the directory where you want your captured photos to be saved. The application will create a default folder (e.g., captured_photos_en or captured_photos_cn) if you don't select one.
4. Select Camera Index:
In the "Camera Index (0, 1, ...):" (或 "攝影機編號 (0, 1, ...):") field, enter the numerical index of the camera you wish to use.
- `0` typically refers to your primary or built-in webcam.
- External USB cameras usually start from `1`, `2`, and so on.
- After entering the number, click the "Apply Camera" (或 "應用攝影機") button to switch the camera feed.
5. Capture Photos:
With the application window active and the camera feed visible, simply press the Spacebar key on your keyboard. Each press will capture the current frame and save it as a new `.jpg` file in your selected output folder. A status message at the bottom will confirm the save location.
6. Exit the Application:
To close the application, press the ESC key on your keyboard, or click the standard 'X' (close) button in the top corner of the window.
