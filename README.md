
# Red_Detector_App

This project is designed to provide a GUI application that uses a webcam to detect and highlight red regions in real-time. The implementation utilizes OpenCV for image processing and PyQt5 for the graphical user interface.

## Features

- Stream video from a webcam
- Toggle the camera on and off
- Switch between different camera modes:
  - Default
  - Gray (Grayscale)
  - Red (Highlight red regions)
  - Mask (Show masked red areas)

## Requirements

- Python 3.x
- OpenCV
- PyQt5

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/SindorimBear/Red_Detector_App.git
   cd Red_Detector_App
   
2. Install the required packages:
   ```sh  pip install opencv-python PyQt5 numpy



## Usage

1. Run the 'init.py' script to initiate the application.
   ```sh
   python init.py
   ```
## Project Structure
  ```shgraphql
  .
├── gui.py                # Contains the GUI application code
├── switch.py             # Contains the camera processing code
├── init.py               # Entry point for the application
└── README.md             # This file
```


## Explanation of Files
gui.py
This file contains the App class, which defines the GUI of the application using PyQt5. It includes buttons to toggle the camera and radio buttons to switch between different camera modes.

switch.py
This file contains the cam_switch class, which handles the video streaming and image processing using OpenCV. It includes methods to set the camera mode, process the video frames, and highlight red regions.

init.py
This is the entry point for the application. It initializes the PyQt5 application and starts the GUI.

## Example
An example of running the application:

1. Make sure your webcam is connected.
2. Run the init.py script:
```sh
python init.py
```
The GUI window will appear. Use the "Turn Camera On" button to start the webcam and select the desired mode using the radio buttons.
## Contributing
Contributions are welcome! Please open an issue or submit a pull request on GitHub.


