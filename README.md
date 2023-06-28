## Image Segmentation Web Service

Version 0.2 - 05/06/2023

### Overview

This project implements a web service with Flask that performs image segmentation using the DeepLabV3 model. It allows users to upload one or more images and receive segmented images as output.

### Usage

1. Extract the folder "projectSeg" to your local machine.
2. Double click: start.cmd.
3. Access the web service by opening the provided URL: "http://http://127.0.0.1:5000/" in your web browser.
4. Choose one or more images for segmentation by clicking the "Select" button and selecting the desired image files.
5. By pressing segment, the images will be uploaded to the server and will be processed.
6. The segmented images will be displayed in a graphical window.
7. To return to the initial state, close the current image and refresh.

### Files

- **seg.py**: The main Python file that contains the Flask application and the routing logic.
- **start.cmd**: The batch file that runs the service.
- **templates/index.html**: The HTML template file for the web service user interface.

### Functions

#### `process_image_and_predict(file_path: str) -> Image.Image`

This function takes the file path of an image as input and uses the DeepLabV3 model to perform image segmentation. It returns the segmented image as a PIL Image object.

#### `upload_file()`

This function is the route handler for the '/uploader' URL. It handles the file upload and segmentation process. It receives the uploaded files, validates them, performs segmentation, saves the segmented images, and displays them in a graphical window. Finally, it redirects back to the home page.

#### `index()`

This function is the route handler for the root URL '/'. It renders the 'index.html' template, which contains the user interface for the web service.

#### `main()`

This function is the entry point of the application. It starts the Flask web server and calculates the total running time of the program.

### Web Sources

- [Guide to FLASK](https://pythonbasics.org/#Flask-Tutorial)

### Future Feature

While the current version of the project provides basic image segmentation functionality, there are several potential features that could be implemented in the future:

- Dockerize the application

### Known Issues

- The segmented images are only displayed in a local graphical window and not in the web interface.
