# RealTimeScanner
This is a real time document Scanner. 
It is based on the blogs from Adrian Rosenbrock at www.pymagesearch.com


The performance for this code is not too great for two reasons. 1) OCR's capabilities for tesseract don't work well out of the box. You need to pre-process the image before tesseract can read it. Altough grayscale and thresholding help out, further and more fine tuned preprocessing is most likely required for your specific problem. It may be the case that is better to train a neural network using OpenCV than tesseract. 2) Tesseract needs to open a file to work (i.e. it doesnt receive information directly from other variables). The reason for this is because the python binaries for tesseract are more of an interface than an actual binary. 

An important thing to note is that the library "imutils" was built by Adrian Rosenbrock. It can be installed using the pip command. 

This library is boilerplate code that uses OpenCV in order to configure the video stream initialization (for the camera to work) and to perform some basic image transforms. 

The code is relatively simple. Below are the steps of how it works 

1) It initializes the video stream. 

2) Run a loop that will take each frame captured by the video stream and resize it to make it bigger. 

3) Draw a blue rectangle in said frame an place it in the center of the image.  Note!: The coordinates for the rectangle were hardcoded, I understand that this is bad practice, my (lame) excuse is that this code is not meant for production but as practice. The solution is not difficult though. Applying the shape command to the frame you can then get the dimensions and use those to place the rectangle in the center. 

4) Take the area inside the rectangle and run it through a transform that will modify it to ensure that it is top view. (this step might be unnecessary but it was the quickest way to isolate the area in the rectangle I found. The true use of this transform command is to warp photos that have a weird angle into a top view).

5) Make warped image into grayscale and apply thresholding. Note: the threshold function currently in use is the one from scikit-image, if the code is run as is, a warning message that this function is deprecated will constantly appear in the command line. A solution is to use the adaptive threshold function from OpenCV. The best configuration I found was to use the adaptive gaussian threshold. Said function is commented in the code. 

6) Save the file in the computer and open it again for tesseract (the python binaries for tesseract are more of an interface than an actual binary, therefore for tesseract to work it needs to read a file from the computer, hence the need for this saving/reading operation). Note: This makes the code INCREDIBLY slow, take into account that all these steps are being performed over an over for each frame so expect a lot of lag. 

7) run the image to string command and print the text read. 

8) If the user presses the "q" key stop the program and close windows.  


