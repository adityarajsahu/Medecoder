<!-- PROJECT LOGO AND NAME -->
<div align="center">
    <a href="https://github.com/adityarajsahu/Medecoder.git">
        <img src="images\logo.png" alt="Logo" width="300" height="100">
    </a>
    <h3 align="center"><strong>MEDECODER</strong></h3>
</div>


Drive [Link](https://drive.google.com/drive/folders/1DMAMYevGo-9VnQH9aWVw3m8p7rgYQTVx?usp=sharing) For all Detailed Demonstration Videos\

Detailed Drive [link](https://drive.google.com/drive/folders/1ERX8f61c84qE4wq6BxO0-LNwpX3V94T0?usp=sharing) for videos, sample dataset and custom labelled images

Colab File [Link](https://colab.research.google.com/drive/1IHl6lvJBVxV8_cZEMxpM1vfRlLyaoC0m?usp=sharing) for model inference and named entity recognition

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#our-solution">Our Solution</a></li>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#user-interface">User Interface</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Create virtual environment</a></li>
        <li><a href="#create-virtual-environment">Create virtual environment</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#contributors">Contributors</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

We have developed a web application that takes doctor's prescription image as input and provides important information such as medicines prescribed, dosage, frequency, diagnostic test and doctor's details. During, the process the user is asked to validate the predictions. The validated data is stored in the database and our prediction model is trained using the stored data in order to fine tune for doctor's prescriptions.

### Our Solution
* We considered employing two machine learning models to solve this issue. 
* The first model, which extracts text from the prescription image, is an optical character recognition model. 
* The required entities in the text that will be shown in the user interface of our web application are then located and classified by a named entity recognition model, which receives the extracted text as its input. 
* The client will have the option to validate our model's predictions if our models are confident about the predictions, or alternatively the same prescription image will be given to a network of clients who will annotate it. 
* Our models will be retrained after a predetermined time using the annotated data that will be saved in the database.

### Built With

* [![Django][Django-image]][Django-url]
* [![EasyOCR][easyocr-image]][easyocr-image]
* [![PyTorch][pytorch-image]][pytorch-url]
* [![PostgreSQL][postgresql-image]][postgresql-url]

### User Interface



<!-- PREREQUISITES AND INSTALLATIONS -->
## Getting Started
To test the web application, you need to create a virtual environment and install the dependencies.

### Prerequisites 
To test the web application, follow the instructions below and install the prerequisites.

Install Anaconda Distribution <br>
[![Anaconda][Anaconda-image]][Anaconda-url]

Open Anaconda Prompt and Update conda environment
```
conda update conda
```

### Create Virtual Environment
Set up a virtual environment
```
conda create -n venv python=3.8
```
### Installation

Install dependencies in the virtual environment
```
pip install -r requirements.txt
``` 

Migrate Database and Run Server

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
``` 
## Features

* Handwritten prescription Digitizer - All data points as follows  will be extracted from from handwritten prescriptions available in variety of formats and compiled into a digital prescription in a common format . Printed data such as doctor's details will be identified from the prescription pad.
* Prescription Review Network - When a user uploads a photo of a prescription, our model will predict the contents with a certain confidence. If the confidence falls below a threshold the prescription should be sent to a network of pharmacists. 
* Prescription Annotator - We intend to offer an interactive UI tool that will allow users to quickly and conveniently correct model predictions and prescription labels.
* Pharmacist Dashboard - A pharmacist profile containing statistics like number of patients  served and successful contributions made for the "PRESCRIPTION REVIEWER".  Along with that they can also view their overall performance. 

## User Interface
![image](https://user-images.githubusercontent.com/86679234/194603489-4844da61-c69c-4915-b864-0a3c9927ca10.png)
Users can upload a prescription
![image](https://user-images.githubusercontent.com/86679234/194603557-3ff2da97-7c45-422a-99d2-b1571eca82a8.png)
Can view and manage all the uploaded prescriptions
![image](https://user-images.githubusercontent.com/86679234/194603588-f79d7ce5-31ae-4b50-a3f2-0f3819175a2f.png)
![image](https://user-images.githubusercontent.com/86679234/194603686-3c5c0799-42eb-4cac-bc66-da4e64b7aa61.png)
Can edit the labels generated by the models and verify the accuracy

![image](https://user-images.githubusercontent.com/50160354/194611781-62919cb9-6d1d-4e78-b7c6-7d1f1b82415b.png)

Can use the integrated labelling tool for labelling the data or correct the output of the model.

![image](https://user-images.githubusercontent.com/50160354/194611819-5e48eba3-d747-42f8-a802-6e948d218254.png)\
Extraction of 
* Medicine
* Dosage
* Frequency

# CURRENT PIPELINE and KEY FEATURES

![image](https://user-images.githubusercontent.com/50160354/194613494-eda7958b-bdc9-44cf-bb64-325bb255dd80.png)\
A interactive cross platform application where a user can manage, edit, annotate the prescriptions, custom train the model to improvise the accuracy

![image](https://user-images.githubusercontent.com/50160354/194613996-ff77c67f-dde5-429d-8b93-672a2527ee59.png)\
Output 

![image](https://user-images.githubusercontent.com/50160354/194614677-770f7df9-fe7d-4898-a334-2407f1e41401.png)\
Text Detection (ROI-Region of Interest)

![image](https://user-images.githubusercontent.com/50160354/194614800-87df8758-f253-4364-9d53-d2d154f2cb51.png)\
Text Extraction

![image](https://user-images.githubusercontent.com/50160354/194615035-7198f3c3-dc0d-4b70-8aa4-5e9b02fa65eb.png)\
OUTPUT FORMAT -> Text, Bouding Box Coordinates, Confidence of each detection


# FUTURE ENHANCEMENTS
![image](https://user-images.githubusercontent.com/50160354/194613566-afa249a7-93a4-41e1-8cf4-a562a2fec86d.png)\



## Contributors
![image](https://user-images.githubusercontent.com/64356997/194586209-4085aa84-6e8a-4be8-b201-47cc9cfd5f6b.png)\

# DEMO VIDEOS


https://user-images.githubusercontent.com/50160354/194622544-78a38e79-a510-40a4-b27e-f90f45e866e1.mp4




Drive [Link](https://drive.google.com/drive/folders/1DMAMYevGo-9VnQH9aWVw3m8p7rgYQTVx?usp=sharing) For all Detailed Demonstration Videos\

Detailed Drive [link](https://drive.google.com/drive/folders/1ERX8f61c84qE4wq6BxO0-LNwpX3V94T0?usp=sharing) for videos, sample dataset and custom labelled images

Colab File [Link](https://colab.research.google.com/drive/1IHl6lvJBVxV8_cZEMxpM1vfRlLyaoC0m?usp=sharing) for model inference and named entity recognition

<!-- MARKDOWN LINKS & IMAGES -->
[Django-image]: https://img.shields.io/badge/django-000000?style=for-the-badge&logo=django&logoColor=white
[Django-url]: https://www.djangoproject.com/
[easyocr-image]: https://img.shields.io/badge/EasyOCR-20232A?style=for-the-badge&logo=easyocr&logoColor=61DAFB
[easyocr-url]: https://github.com/JaidedAI/EasyOCR
[pytorch-image]: https://img.shields.io/badge/PyTorch-35495E?style=for-the-badge&logo=pytorch&logoColor=4FC08D
[pytorch-url]: https://pytorch.org/
[postgresql-image]: https://img.shields.io/badge/PostgreSQL-4A4A55?style=for-the-badge&logo=postgresql&logoColor=white
[postgresql-url]: https://www.postgresql.org/
[Anaconda-image]: https://img.shields.io/badge/Anaconda-563D7C?style=for-the-badge&logo=anaconda&logoColor=white
[Anaconda-url]: https://repo.anaconda.com/archive/Anaconda3-2022.05-Windows-x86_64.exe
