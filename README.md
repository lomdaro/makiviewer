# MakiViewer

[![GitHub release](https://img.shields.io/github/release/lomdaro/makiviewer.svg)](https://github.com/lomdaro/makiviewer/releases)

A simple python script that will display an image in the bottom right corner of your screen. Multiple images will cycle at a set interval (default is 60 seconds). Display your favorite images in the corner at all times!
## Prerequisites 
Before running the script, ensure that you have the following: 
- Python 3.x installed on your system. You can download Python from the official website: [python.org](https://www.python.org) 
- PyQt5 library installed. You can install it using pip (make sure you install pip first):
  ```
  pip install PyQt5
  ```
## Setup

1. Download the latest release or clone the repository.

2. Place your desired image files in a folder within the project directory. By default, the script looks for images in the `sprites` folder, but you can change this in the configuration file.

3. Open the `config.ini` file in a text editor and customize the settings according to your preferences. The available settings are:
 - `folder`: Specifies the folder where the image files are located. Default is `sprites`.
 - `randomize`: Specifies whether the images should be displayed in a random order. Default is `true`.
 - `scale`: Specifies the scaling factor for the images. Default is `0.75`.
 - `interval`: Specifies the interval (in seconds) between image switches. Default is `60`.
 - `enable_hover_transparency`: Specifies whether the hover transparency effect is enabled. Default is `true`.

4. Save the `config.ini` file after making any changes.

## Usage

To run MakiViewer, double-click on the `main.pyw` file. The script will then display the widget on the screen.

The widget will cycle through the images in the specified folder at the configured interval. If `randomize` is set to `true`, the images will be displayed in a random order. If `enable_hover_transparency` is set to `true`, the image will become semi-transparent when you hover over it.

You can left click the image to cycle to the next image.

To close the widget, right-click on the image.

## License

This project is licensed under the [GPL-3.0 license](LICENSE).