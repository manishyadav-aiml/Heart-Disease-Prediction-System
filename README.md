# Heart Disease Prediction System

A Django web application that estimates the risk of heart disease from 13 health
parameters using a Machine Learning model (scikit-learn). Users register, log in,
enter the values, and get a **probability (%)** and a **risk level (LOW / MODERATE / HIGH)**.
Every prediction is saved in the user's history.

> **Screening aid only.** This project is for learning. It is not a medical diagnosis
> and does not replace a doctor.

---

## IMPORTANT: demo data

The `dataset/heart.csv` in this zip is **synthetic demo data** (random values with the
same columns as the real dataset), so that the project runs immediately.
The bundled model is trained on it, so **its predictions are not meaningful**
and a yellow "Demo mode" banner is shown on every page.

To use the real dataset (UCI / Cleveland heart disease data, 303 rows, 13 attributes + `target`):

1. Replace `dataset/heart.csv` with the real file (columns: `age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, target`).
2. Delete `dataset/DEMO_DATA.txt`.
3. Run `python train_model.py` and restart the server.

The training script compares five models with 5-fold cross-validation, saves the best one
as `model/heart_disease_model.pkl` and the scaler as `model/scaler.pkl`, and prints the test-set metrics
(use these numbers in your report). The code columns (`cp`, `slope`, `thal`, `target`) must use the same
numeric coding as the form on the prediction page; check your copy of the dataset.

---

## Features

- User registration, login and logout (Django authentication)
- Prediction form with 13 validated inputs, grouped in sections
- Result page with risk level, probability, colour gauge and a short note
- Prediction history (last 5 on the home page, stored in SQLite)
- Django admin to view all users and predictions
- Separate `ml.py` module for loading the model and predicting

## Project structure

```
Heart-Disease-Prediction-System/
├── manage.py
├── requirements.txt
├── train_model.py            # trains and saves the model files
├── README.md
├── .gitignore
├── heart_disease/            # project settings, urls, asgi, wsgi
├── prediction/               # the app
│   ├── migrations/
│   ├── templates/prediction/ # base, home, login, register, prediction, result
│   ├── static/prediction/    # css, js, images
│   ├── admin.py  apps.py  models.py  views.py  urls.py  forms.py
│   ├── ml.py                 # model loading + prediction
│   └── context_processors.py
├── model/                    # heart_disease_model.pkl, scaler.pkl, model_info.json
└── dataset/                  # heart.csv (+ generate_demo_dataset.py)
```

`db.sqlite3` is created when you run `migrate` (step 4 below).
`templates/prediction/base.html` is the shared layout used by the five pages.

---

## Run on localhost

Requirements: **Python 3.9 or newer** and pip.

### 1. Open a terminal in the project folder
```
cd Heart-Disease-Prediction-System
```

### 2. Create and activate a virtual environment

Windows:
```
python -m venv venv
venv\Scripts\activate
```
Linux / macOS:
```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the requirements
```
pip install -r requirements.txt
```

### 4. Create the database
```
python manage.py migrate
```

### 5. Re-create the model files for your installed scikit-learn (recommended)
```
python train_model.py
```
(The bundled `.pkl` files were saved with another scikit-learn version. Retraining takes a few seconds
and avoids version warnings.)

### 6. (Optional) Create an admin user
```
python manage.py createsuperuser
```

### 7. Start the server
```
python manage.py runserver
```
Open **http://127.0.0.1:8000/** in your browser. Admin: http://127.0.0.1:8000/admin/

---

## How to use

1. Click **Register**, create an account (you are logged in automatically).
2. Open **New Prediction**, fill in the 13 values and click **Predict Risk**.
3. Read the risk level and probability on the result page.
4. Use **Predict for another patient** or return to **Home** to see your history.

## Input attributes

| Field | Meaning | Allowed values |
|---|---|---|
| age | Age in years | 1 - 120 |
| sex | Sex | 0 = female, 1 = male |
| cp | Chest pain type | 0 - 3 |
| trestbps | Resting blood pressure (mm Hg) | 80 - 250 |
| chol | Serum cholesterol (mg/dl) | 100 - 600 |
| fbs | Fasting blood sugar > 120 mg/dl | 0 = no, 1 = yes |
| restecg | Resting ECG result | 0 - 2 |
| thalach | Maximum heart rate achieved | 60 - 250 |
| exang | Exercise induced angina | 0 = no, 1 = yes |
| oldpeak | ST depression induced by exercise | 0 - 10 |
| slope | Slope of the peak exercise ST segment | 0 - 2 |
| ca | Major vessels coloured by fluoroscopy | 0 - 4 |
| thal | Thal test result | 0 - 3 (coding as in your heart.csv) |

Risk levels (fixed limits chosen for this project, not clinical thresholds):
below 30% = LOW, 30% to below 60% = MODERATE, 60% and above = HIGH.

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'django'` | Activate the virtual environment and run `pip install -r requirements.txt` |
| "The prediction model could not be loaded" | Run `python train_model.py`, then restart the server |
| `no such table` error | Run `python manage.py migrate` |
| Port 8000 already in use | `python manage.py runserver 8080` |
| Changes to the model not visible | Stop and restart `runserver` (the model is cached in memory) |

## Technologies

Python, Django, SQLite, scikit-learn, pandas, NumPy, joblib, HTML, CSS, JavaScript.
