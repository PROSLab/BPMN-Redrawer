# BPMN Redrawer

BPMN Redrawer is a web application that allows to upload images representing BPMN models to convert them in actual BPMN models stored in *.bpmn* format.

## Table of contents
<!--ts-->
   * [Functionalities](#functionalities)
   * [Quickstart](#quickstart)
   * [How to run](#how-to-run)
   * [Backend](#backend)
   * [Frontend](#frontend)
<!--te-->

## Functionalities

The user, through the simple and intuitive GUI, can load an image from the local storage in different formats (PNG, JPEG, BMP). The image is then displayed and is ready to be converted. After that, the backend receives the loaded image, extracts the elements and link them togheter in order to obtain the final *.bpmn* file. At this pont the result comes back to the frontend and, using the GUI, can be downloaded or can be shown and edited thanks to the integration of the [*bpmn-js*](https://bpmn.io/toolkit/bpmn-js/) library.

Overall, the application is able to provide the following functionalities:
- Convert an image into the corresponding *.bpmn* model;
- Download the converted model;
- Visualize the converted model and, next to it, the starting image;
- Edit the converted model;
- Open, edit and download an existing *.bpmn* model;
- Create a BPMN model from scratch and download it as *.bpmn* file or *.svg* image;
- Load an image next to the BPMN editor.

At present the application is able to detect the following BPMN elements with a fair average precision:

<table>
<tr><td>

| BPMN Nodes                            | AP
|---------------------------------------|-----
| Start Event                           | 96.923
| Start Message Event                   | 98.796
| Start Timer Event                     | 100.0
| Start Conditional Event               | 99.901
| Start Signal Event                    | 98.713
| Intermediate Catch Message Event      | 94.489
| Intermediate Catch Timer Event        | 98.811
| Intermediate Catch Conditional Event  | 99.010
| Intermediate Catch Signal Event       | 99.010
| Intermediate Catch Link Event         | 100.0
| Intermediate Throw Event              | 86.139
| Intermediate Throw Message Event      | 88.355
| Intermediate Throw Escalation Event   | 99.622
| Intermediate Throw Compensation Event | 100.0
| Intermediate Throw Signal Event       | 99.586 
| Intermediate Throw Link Event         | 100.0


</td><td>

| BPMN Nodes              | AP
|-------------------------|-----
| End Event               | 96.406
| End Message Event       | 80.499
| End Escalation Event    | 99.802
| End Compensation Event  | 100.0
| End Signal Event        | 99.218
| End Error Event         | 100.0
| End Terminate Event     | 98.803
| Esclusive Gateway       | 96.512
| Parallel Gateway        | 96.427
| Inclusive Gateway       | 93.915
| Event-Based Gateway     | 89.109
| Task                    | 97.653
| Data Object             | 96.819
| Data Store              | 100.0
| Text Annotation         | 72.670
| Pool                    | 95.870

</td><td>

| BPMN Connecting Objects | AP-box | AP-keypoints|
|-------------------------|--------|-------------|
| Sequence Flow           | 82.988 | 96.865      |
| Message Flow            | 73.678 | 88.316      | 
| Data Association        | 65.154 | 84.546      |


</td></tr> </table>


## Quickstart

Our web application is available and ready to use at the following link:
**[BPMN Redrawer](https://pros.unicam.it/bpmn-redrawer-tool/)**.

A tutorial on its usage is available by clicking the image below:
[![Watch the video](https://img.youtube.com/vi/0e2qnbSp9XY/maxresdefault.jpg)](https://youtu.be/0e2qnbSp9XY)

The user can perform very simple steps to obtain a *.bpmn* file starting from an image:
- In the *HOME* page, the user can load an image from local storage with the corresponding button or one of the sample images by clicking on them;
<p align="center">
<img src="extra/images/home.png" width="90%" />
</p>

- If correctly loaded, the image will be displayed;
- Different options can be enabled to be performed by the backend, such as:
    - object detection for the BPMN elements;
    - keypoint detection for the BPMN flows;
    - OCR for the BPMN labels;
- Then the *CONVERT* button can be clicked to start the conversion (it takes a few seconds to complete the process);
- Once the conversion is done, the user can either download or view and edit the resulting model;
- By selecting the *VIEW IN EDITOR* button, the *EDITOR* page will allow the user to see the converted model and, if needed, to edit and correct it. The starting image is displayed next to the model and simplifies the revising process (a vertical splitter can be moved to resize the BPMN editor and the image viewer);
<p align="center">
<img src="extra/images/editor.png" width="90%" />
</p>

- If the user is happy with the result, the final model can be downloaded either as *.bpmn* file or as *.svg* image.

The user can also use the *EDITOR* page to open, edit and download an existing *.bpmn* model or to create a BPMN model from scratch, as well as loading an image in the image viewer.

## How to run

BPMN Redrawer is available as a Docker image by creating it from this folder or pulling it from [DockerHub](https://hub.docker.com/r/proslab/bpmn-redrawer).

First of all, download the trained detectron2 models from [Hugging Face](https://huggingface.co/PROSLab/BPMN-Redrawer-Models/tree/main) and move them in the [detectron_model](backend/bpmn_redrawer_backend/detectron_model) folder.

In particular these two models are:
- <b>final_model.pth</b>: the Object Detection model;
- <b>kp_final_model.pth</b>: the KeyPoint Prediction model.

This is needed when working with the application without using containers. When using the containers, the models will be downloaded automatically.

To build the image, from the root folder it is sufficient to launch the command:
```bash
docker build -t bpmn-redrawer-image .
```

Once the image has been built, it is possible to run it with the command:
```bash
docker run -d -p 5000:5000 -e BACKEND_PORT=5000 -e BACKEND_MODE=production --name bpmn-redrawer-container bpmn-redrawer-image
```

Otherwise the application can be run with a single command, using the latest image available on DockerHub:

```bash
docker run -d -p 5000:5000 -e BACKEND_PORT=5000 -e BACKEND_MODE=production --name bpmn-redrawer-container proslab/bpmn-redrawer
```

Two variables are available when running the container:
- BACKEND_MODE: <b>development</b> or <b>production</b> (default=<b>production</b>)
- BACKEND_PORT: which port the container will use internally to run the app (default=<b>5000</b>). This is the containerPort in the command:
    ```bash
    -p hostPort:containerPort
    ```

Once launched, the application will be available at [http://localhost:5000](http://localhost:5000).

## Backend

The [Backend README](backend/README.md) contains more instructions on how to launch/develop the backend.

## Frontend

The [Frontend README](frontend/README.md) contains more instructions on how to launch/develop the frontend.
