# Classic Rock-Paper-Scissors

## Intro:
This repo is for Semester VI. The project is a classic Rock-Paper-Scissors game.<br>
The custom built dataset consists of 3 classes : Rock, Paper, Scissors.

Find the guidelines to follow while playing the game <a href = "RULES.md" >here</a>.

## Model:
Please get the **dataset and the model** <a href = "https://drive.google.com/drive/folders/1UKfwxUPQPuvKVmwNQjX9cjEMJ5L1j_Z7?usp=sharing">here</a>. (access restricted to Somaiya Account)

The dataset is generated using **captureImage.py** . Please press 'a' for starting the capturing of images.
The dataset(train + validation) is ~1000 images. The 'test_images' folder contains the test images 600 images(200 * 3).
After building and testing custom models, the accuracy was low. We currently use the concept of <a href = "https://thebinarynotes.com/transfer-learning-keras-vgg16/">tranfer learning</a> for our use case. We train the vgg16 model with 3 <a href = "https://keras.io/api/layers/core_layers/dense/">dense layers</a>, <a href = "https://developers.google.com/machine-learning/crash-course/regularization-for-simplicity/l2-regularization">l2 regularizers</a> to avoid <a href = "https://www.coursera.org/lecture/machine-learning/the-problem-of-overfitting-ACpTQ">overfitting</a> problem.

The library used for backend processing is <a href = "https://keras.io/getting_started/">Keras</a>.

This is a snap of plot_model:<br><br>
<img src = "images-readme/1.png" alt="plot_model" width="400" height="700" >

This gives us ~98% accuracy on live testing with web camera.
The model predicts the probability of each of the 3 classes. We display the class with max probability.

The plot of accuracy, loss, precision and recall are as follows:<br><br>
<img src = "images-readme/accuracy.png" alt = "accuracy">.<br><br>
<img src = "images-readme/loss.png" alt = "loss">.<br><br>
<img src = "images-readme/precision.png" alt = "precision">.<br><br>
<img src = "images-readme/recall.png" alt = "recall">.<br><br>

## GUI:
To build the desktop application, we use <a href = "https://pypi.org/project/PyQt5/">PyQt</a>. You can find some useful tutorials <a href="https://www.youtube.com/playlist?list=PLzMcBGfZo4-lB8MZfHPLTEHO9zJDDLpYj"> here</a>.

<img src = "images-readme/mainwindow.PNG" alt="mainwindow" width="400" height="700" >
<img src = "images-readme/ruleswindow.PNG" alt="ruleswindow" width="400" height="700" >
<img src = "images-readme/inputwindow.PNG" alt="inputwindow" width="400" height="700" >
<img src = "images-readme/playwindow1.PNG" alt="playwindow1" width="400" height="700" >
<img src = "images-readme/playwindow2.PNG" alt="playwindow2" width="400" height="700" >
<img src = "images-readme/resultwindow.PNG" alt="resultwindow" width="400" height="700" >