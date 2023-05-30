# Heart Disease Data: Prediction and Visualization in AWS
Authors: Cindy Chen, Michelle Liu, Yifei Wang

Date: Spring 2023

Master of Science in Machine Learning and Data Science (formerly MS in Analytics)

Northwestern University

## Project Objective
With the data from the Centers for Disease Control and Prevention’s (CDC) annual survey of 400,000 adults, this project aims at building __a prediction portal and presenting visualizations for individuals with concerns for heart disease and medical practitioners__.

For individuals who may be too busy or unable to seek immediate medical resources, a prediction portal where users can input relevant information and receive an __estimation of individual's risk for heart disease__ will empower people to take proactive steps towards their health, even when professional medical assistance may not be readily available.

Additionally, the portal aims to provide a __preliminary estimation for heart disease for medical practitioners__ while they are waiting for the results of formal medical tests. This will allow medical practitioners to gain insights and provide timely and effective care to their patients.

Furthermore, the project seeks to spread __understanding and awareness__ of heart disease patients' characteristics through the use of visualizations. The graphs will enable both healthcare professionals and the general public to have a clearer understanding of heart disease, leading to improved prevention, diagnosis, and treatment strategies.

This project will use __Amazon Web Services (AWS)__, motivated by several characteristics of AWS. First, __reliability and availability__. This is crucial for a project that aims to provide continuous accessibility to the prediction portal, allowing individuals and medical practitioners to perform self-checks and obtain estimations at any time. Second, __flexibility and scalability__. This permits the project plenty of room to improve in the future by incorporating increasing data volume and complexity. Finally, __wide array of managed services__. This allows the project to streamline development efforts in a time-efficient and low-cost manner.

## Project AWS Architecture Diagram
![Cloud Project_diagram png 13-46-58-253](https://github.com/MSIA/423-project-group10/assets/78248018/56dafa1f-4de8-4a57-a2ce-11ec711b2ebc)

## Relevant Links
Visualizations: https://dzisgg772bofj.cloudfront.net

Prediction portal: http://team10-website.s3-website.us-east-2.amazonaws.com

## Repository Structure
<pre>
│  
├── data                            <- Folder for different versions of data used in this project
│   ├── balanced_data.csv           <- Preprocessed and upsampled data (used for model experiment and training)
│   ├── for_EDA.csv                 <- Preprocessed data (used for visualization generation)
│   └── heart_2020_cleaned.csv      <- Original data downloaded from Kaggle
│
├── EDA                             <- Folder for EDA and visualization
│   ├── med_data_html               <- Folder for presenting visualizations via AWS CloudFront
│   │   ├── Age.png                 <- Histograms for age distribution of individuals with and without heart disease
│   │   ├── BMI.png                 <- Histograms for BMI distribution of individuals with and without heart disease
│   │   ├── Diabetic.png            <- Histograms for diabetic distribution of individuals with and without heart disease
│   │   ├── KidneyDisease.png       <- Histograms for kidney disease distribution of individuals with and without heart disease
│   │   ├── PhysicalHealth.png      <- Histograms for physical health distribution of individuals with and without heart disease
│   │   ├── Sex.png                 <- Histograms for sex distribution of individuals with and without heart disease
│   │   ├── Smoking.png             <- Histograms for smoking distribution of individuals with and without heart disease
│   │   ├── Stroke.png              <- Histograms for stroke distribution of individuals with and without heart disease
│   │   ├── csi.min.js              <- JavaScript that defines the functionality and interactivity of the resulting web page
│   │   ├── index.html              <- HTML file that defines the structure and content of the resulting web page
│   │   └── style.css               <- CSS file that defines the visual appearance and layout of the resulting web page
│   │
│   ├── preprocess_container        <- Folder for preprocessing data via AWS ECR and Lambda
│   │   ├── Dockerfile              <- Docker file for preprocessing data
│   │   ├── main.py                 <- Python script for preprocessing data
│   │   └── requirements.txt        <- A list of the modules and packages required for preprocessing data
│   │
│   ├── visualization_container     <- Folder for generating visualizations via AWS ECR and Lambda
│   │   ├── .gitignore              <- A list of files and folders to ignore in this portion
│   │   ├── Dockerfile              <- Docker file for generating visualizations
│   │   ├── main.py                 <- Python script for generating visualizations
│   │   └── requirements.txt        <- A list of the modules and packages required for generating visualizations
│   │
│   └── EDA.ipynb                   <- Script for data preprocessing (including upsampling) and cross validation model experiment
│
├── Inference                       <- Folder for making inference via AWS Lambda and API Gateway
│   ├── index.html                  <- HTML file that defines the structure and content of the resulting web page
│   ├── lambda_inference_api.py     <- Python script for inference
│   ├── new.css                     <- CSS file that defines the visual appearance and layout of the resulting web page
│   └── script.js                   <- JavaScript that defines the functionality and interactivity of the resulting web page
│
├── Model                           <- Folder for training model via AWS Lambda
│   └── train_lambda_function.py    <- Python script for model training
│
└── README.md                       <- Documents project objective, relevant links, and repository structure
</pre>
