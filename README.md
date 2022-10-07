<!-- PROJECT LOGO AND NAME -->
<div align="center">
    <a href="https://github.com/adityarajsahu/Medecoder.git">
        <img src="images\logo.png" alt="Logo" width="300" height="100">
    </a>
    <h3 align="center"><strong>MEDECODER</strong></h3>
</div>

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
    <li><a href="#usage">Usage</a></li>
    <li><a href="#further-improvement">Further Improvement</a></li>
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
conda create -n venv python=3.7
```
### Installation

Install dependencies in the virtual environment
```
pip install -r requirements.txt
``` 

## Features

* Handwritten prescription Digitizer - All data points as follows  will be extracted from from handwritten prescriptions available in variety of formats and compiled into a digital prescription in a common format . Printed data such as doctor's details will be identified from the prescription pad.
* Prescription Review Network - When a user uploads a photo of a prescription, our model will predict the contents with a certain confidence. If the confidence falls below a threshold the prescription should be sent to a network of pharmacists. 
* Prescription Annotator - We intend to offer an interactive UI tool that will allow users to quickly and conveniently correct model predictions and prescription labels.
* Pharmacist Dashboard - A pharmacist profile containing statistics like number of patients  served and successful contributions made for the "PRESCRIPTION REVIEWER".  Along with that they can also view their overall performance. 

## Contributors
![image](https://user-images.githubusercontent.com/64356997/194586209-4085aa84-6e8a-4be8-b201-47cc9cfd5f6b.png)
