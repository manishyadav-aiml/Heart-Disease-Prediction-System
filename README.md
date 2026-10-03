# ❤️ Heart Disease Prediction System

# 

# A Django-based web application that uses Machine Learning to estimate the probability of heart disease from 13 health-related parameters.

# 

# Users can create an account, enter health information, receive an estimated probability and project-defined risk level (LOW / MODERATE / HIGH), view prediction history, and download a PDF report.

# 

# ⚠️ Medical Disclaimer: This project is developed for educational and screening purposes only. It is not a medical diagnosis, and its predictions should not replace evaluation or advice from a qualified healthcare professional.

# 

# 📌 Project Overview

# 

# The Heart Disease Prediction System demonstrates how Machine Learning can be integrated into a Django web application for health-risk screening.

# 

# 🔄 How the system works

# 👤 User creates an account or logs in.

# 📝 User enters 13 health parameters.

# ✅ The application validates the input values.

# ⚙️ Input data is preprocessed using the trained scaler.

# 🤖 The trained Machine Learning model generates an estimated probability.

# 📊 The probability is converted into a project-defined risk level.

# 💾 The prediction is saved to the user's history.

# 📄 A downloadable PDF report can be generated.

# ✨ Key Features

# 👤 User registration and login

# 🔐 Django authentication

# 📝 Validated 13-parameter prediction form

# 🤖 Machine Learning-based prediction

# 📊 Probability displayed as a percentage

# 🟢 LOW / 🟡 MODERATE / 🔴 HIGH risk classification

# 📚 User-specific prediction history

# 📋 Detailed prediction result page

# 📄 Downloadable PDF report

# 🛠️ Django admin interface

# 📱 Responsive web interface

# ⚠️ Medical and educational disclaimer

# 📊 Dataset

# 

# This project uses the UCI Heart Disease — Cleveland dataset.

# 

# The original Cleveland dataset contains 303 records. Six records contain missing values in required attributes and are removed during preprocessing, leaving 297 usable records for this project.

# 

# 🎯 Target Variable

# 

# The original target values are converted into binary classification:

# 

# 0 → No presence of heart disease

# 1 → Presence of heart disease

# 📈 Dataset Distribution

# Target	Records

# 0	160

# 1	137

# Total	297

# 🧩 Input Features

# 

# The system uses 13 input features:

# 

# text

# age

# sex

# cp

# trestbps

# chol

# fbs

# restecg

# thalach

# exang

# oldpeak

# slope

# ca

# thal

# Feature	Description	Values (UCI coding)

# age	Age in years	1 – 120

# sex	Sex	0 = female, 1 = male

# cp	Chest pain type	1 = typical angina, 2 = atypical angina, 3 = non-anginal pain, 4 = asymptomatic

# trestbps	Resting blood pressure (mm Hg)	80 – 250

# chol	Serum cholesterol (mg/dl)	100 – 600

# fbs	Fasting blood sugar > 120 mg/dl	0 = no, 1 = yes

# restecg	Resting ECG result	0 = normal, 1 = ST-T wave abnormality, 2 = left ventricular hypertrophy

# thalach	Maximum heart rate achieved (bpm)	60 – 250

# exang	Exercise induced angina	0 = no, 1 = yes

# oldpeak	ST depression induced by exercise	0 – 10

# slope	Slope of the peak exercise ST segment	1 = upsloping, 2 = flat, 3 = downsloping

# ca	Major vessels coloured by fluoroscopy	0 – 3

# thal	Thal test result	3 = normal, 6 = fixed defect, 7 = reversible defect

# 🧹 Preprocessing

# Rows with missing values (?) in required attributes are removed (303 → 297 records)

# Duplicate rows are removed

# The original target (0 to 4) is converted to binary (0 = no disease, 1 = disease)

# Features are scaled with StandardScaler

# The data is split 80% training / 20% testing (stratified)

# 

# 📝 About the bundled dataset/heart.csv: if a file named dataset/DEMO\_DATA.txt exists, the CSV is synthetic demo data used only so that the project runs out of the box, and a "Demo mode" banner is shown in the app. To use the real dataset, replace dataset/heart.csv (header row: age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal,target; the raw UCI processed.cleveland.data file without a header also works), delete DEMO\_DATA.txt, and run python train\_model.py.

# 

# 🤖 Machine Learning Model

# 

# train\_model.py compares five classifiers using 5-fold cross-validation (ROC-AUC) on the training data:

# 

# Logistic Regression

# K-Nearest Neighbors

# Support Vector Machine

# Decision Tree

# Random Forest

# 

# The model with the best cross-validation score is trained on the full training set and saved:

# 

# File	Purpose

# model/heart\_disease\_model.pkl	Selected classifier

# model/scaler.pkl	Fitted StandardScaler

# model/model\_info.json	Selected model name and test-set metrics (shown on the home page)

# 

# The script prints accuracy, precision, recall, F1-score and ROC-AUC on the held-out test set. Run it yourself to get the exact figures for your copy of the dataset.

# 

# 🚦 Risk levels

# 

# The model's probability is converted into a level using fixed limits chosen for this project (they are not clinical thresholds):

# 

# Probability	Risk level

# below 30%	🟢 LOW

# 30% to below 60%	🟡 MODERATE

# 60% and above	🔴 HIGH

# 🛠️ Technologies Used

# Area	Technology

# Language	Python 3

# Web framework	Django

# Machine Learning	scikit-learn, pandas, NumPy, joblib

# PDF reports	ReportLab

# Database	SQLite

# Frontend	HTML, CSS, JavaScript

# 📁 Project Structure

# text

# Heart-Disease-Prediction-System/

# │

# ├── manage.py

# ├── requirements.txt

# ├── train\_model.py              # trains and saves the model files

# ├── README.md

# ├── .gitignore

# │

# ├── heart\_disease/              # Django project settings

# │   ├── settings.py

# │   ├── urls.py

# │   ├── asgi.py

# │   └── wsgi.py

# │

# ├── prediction/                 # Main application

# │   ├── migrations/

# │   ├── templates/prediction/   # base, home, login, register, prediction, result

# │   ├── static/prediction/      # css, js, images

# │   ├── admin.py

# │   ├── apps.py

# │   ├── forms.py

# │   ├── ml.py                   # model loading and prediction

# │   ├── models.py

# │   ├── report.py               # PDF report generation

# │   ├── urls.py

# │   └── views.py

# │

# ├── model/

# │   ├── heart\_disease\_model.pkl

# │   ├── scaler.pkl

# │   └── model\_info.json

# │

# └── dataset/

# &#x20;   ├── heart.csv

# &#x20;   └── generate\_demo\_dataset.py

# 🚀 Installation and Setup

# 

# Requirements: Python 3.9 or newer and pip.

# 

# 1️⃣ Clone the repository

# bash

# git clone https://github.com/<your-username>/Heart-Disease-Prediction-System.git

# cd Heart-Disease-Prediction-System

# 2️⃣ Create and activate a virtual environment

# 

# Windows

# 

# bash

# python -m venv venv

# venv\\Scripts\\activate

# 

# Linux / macOS

# 

# bash

# python3 -m venv venv

# source venv/bin/activate

# 3️⃣ Install dependencies

# bash

# pip install -r requirements.txt

# 4️⃣ Apply database migrations

# bash

# python manage.py migrate

# 5️⃣ Train the model

# bash

# python train\_model.py

# 

# This recreates model/heart\_disease\_model.pkl and model/scaler.pkl for your installed scikit-learn version.

# 

# 6️⃣ (Optional) Create an admin user

# bash

# python manage.py createsuperuser

# 7️⃣ Run the development server

# bash

# python manage.py runserver

# 

# Open http://127.0.0.1:8000/ in your browser. The admin panel is at http://127.0.0.1:8000/admin/.

# 

# 🧭 How to Use

# Click Register and create an account.

# Open New Prediction and fill in the 13 health parameters.

# Click Predict Risk to see the probability and risk level.

# Click Download PDF report on the result page to save the report.

# Your last predictions are listed on the Home page.

# 🧯 Troubleshooting

# Problem	Solution

# No module named django	Activate the virtual environment and run pip install -r requirements.txt

# no such table	Run python manage.py migrate

# "The prediction model could not be loaded"	Run python train\_model.py, then restart the server

# Port 8000 already in use	python manage.py runserver 8080

# Model changes not visible	Stop and restart runserver (the model is cached in memory)

# ⚠️ Limitations

# The model is trained on a small dataset (297 records), so it may not generalise to all populations

# Only 13 attributes are used; factors such as smoking, family history and lifestyle are not included

# Some inputs (for example fluoroscopy results) require clinical tests

# Risk levels use fixed limits chosen for this project and are not clinical thresholds

# The output is a statistical estimate, not a diagnosis

# 🔮 Future Improvements

# Larger and more varied training data

# Additional attributes (smoking, family history, BMI, physical activity)

# Hyper-parameter tuning and model explanation (feature importance per prediction)

# Batch prediction from CSV files

# Deployment with a production database and DEBUG turned off



# 📜 Disclaimer

# 

# This software is provided for educational purposes. It does not provide medical advice, diagnosis or treatment. Always consult a qualified healthcare professional about any health concern.

