# face_recog_monitoring_system
The application is built on raspbery pi 4

# Intro
The project is based on face recognition using OpenCV and pre trained 128-D Deep Learning facial embedding (face_recognition python package). The project has two parts 
- The front end with vidoe stream and captures the frames from camera feed
- The backend Deep Learning based facial recognition system

# Architecture
![Capture](https://user-images.githubusercontent.com/47440070/89106342-c8ce8b80-d446-11ea-91e2-e3d7f8039599.PNG)

- A socket connection is establised between face recognition server and raspberry pi
- The face capture program captures the frames from the camera on rasbperry pi
- The frame is send to the server for face recognition
- The server processes the frame and sends it back to rasperry pi to display on webpage

Face recognition program uses pre trained CNN model to perform the recognition. Raspberry pi cannot run the CNN model due to resource limitations.

# Usage
The code is written on python3.

## Install required packages
```
pip intstall -r requirements.txt
```
## Run the face recognition server
Run the program on a machine with resources capable of runnign CNN model
```
python image_proc_socket.py
```
The program starts opens the port 8002 for clients to connect
## Run the webapp program
Execute the webapp on raspberry pi.
```
python webapp.py [--serverIP X.X.X.X]
```
While executing the webapp the IP address of the face recognition server can be provided. The server ip defaults to 127.0.0.1.<br>
**Note**: The program can be run on any host, not just Raspberry Pi. It is possible to run both the face recognition server and webapp on same machine without modifying the code.<br>
If running both the programs on same machine the serverIP need not be provided as it defaults to localhost<br>

To connect to webpage feed login to "http://\<raspberry-pi ip\>:8001/video_feed_page". <br>

If the image recognition server is not running or the connection is broken the webpage will still show live feed without face recognition

# Face Recognition module
Face recognition works on a technique called deep metric learning. Unlike conventional deep learning methods whcich output a single label the technique creates a real-valued feature vector. 
## Training the model
Follow the steps to train the model for custom images.
### Create training data
Run the webapp.py. server side code is not required
```
python webapp.py
```
The image can be captured using the "capture" button on the webpage.
- Provide a name in the text box
- Click on "Capture"
The images will be saved to path "utils/images/\<name in text box\>" folder on the host running "webapp.py". (Training may take some time if running on raspbeery pi)

### Training model
Run the program train_model.py to train the face recognition
```
python train_model.py
```
- Training creates 128-D encoding for each face in the folder
- The encodings are stored in encoding file "utils/encoding.pkl"
- Transfer the file to utils folder on system where "image_proc_socket.py" would be executed

## Working
- For each face captured in camera feed a 128-D encoding is created by the face recognition program
- The encoding is compared against known encodings which is stored in "utils/encodings.pkl"
- Based on voting system the face is identified
