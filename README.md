# \# ❤️ Heart Disease Prediction System

# 

# A Django-based web application that uses \*\*Machine Learning\*\* to estimate the probability of heart disease from 13 health-related parameters.

# 

# Users can create an account, enter health information, receive an estimated probability and project-defined risk level (\*\*LOW / MODERATE / HIGH\*\*), view prediction history, and download a PDF report.

# 

# > ⚠️ \*\*Medical Disclaimer:\*\* This project is developed for educational and screening purposes only. It is not a medical diagnosis, and its predictions should not replace evaluation or advice from a qualified healthcare professional.

# 

# \---

# 

# \## 📌 Project Overview

# 

# The \*\*Heart Disease Prediction System\*\* demonstrates how Machine Learning can be integrated into a Django web application for health-risk screening.

# 

# \### 🔄 How the system works

# 

# 1\. 👤 User creates an account or logs in.

# 2\. 📝 User enters 13 health parameters.

# 3\. ✅ The application validates the input values.

# 4\. ⚙️ Input data is preprocessed using the trained scaler.

# 5\. 🤖 The Random Forest model generates an estimated probability.

# 6\. 📊 The probability is converted into a project-defined risk level.

# 7\. 💾 The prediction is saved to the user's history.

# 8\. 📄 A downloadable PDF report can be generated.

# 

# \---

# 

# \## ✨ Key Features

# 

# \- 👤 User registration and login

# \- 🔐 Django authentication

# \- 📝 Validated 13-parameter prediction form

# \- 🤖 Machine Learning-based prediction

# \- 📊 Probability displayed as a percentage

# \- 🟢 LOW / 🟡 MODERATE / 🔴 HIGH risk classification

# \- 📚 User-specific prediction history

# \- 📋 Detailed prediction result page

# \- 📄 Downloadable PDF report

# \- 🛠️ Django admin interface

# \- 📱 Responsive web interface

# \- ⚠️ Medical and educational disclaimer

# 

# \---

# 

# \## 📊 Dataset

# 

# This project uses the \*\*UCI Heart Disease — Cleveland dataset\*\*.

# 

# The original Cleveland dataset contains \*\*303 records\*\*. Six records contain missing values in required attributes and are removed during preprocessing, leaving \*\*297 usable records\*\* for this project.

# 

# \### 🎯 Target Variable

# 

# The original target values are converted into binary classification:

# 

# \- `0` → No presence of heart disease

# \- `1` → Presence of heart disease

# 

# \### 📈 Dataset Distribution

# 

# | Target | Records |

# |---|---:|

# | 0 | 160 |

# | 1 | 137 |

# | \*\*Total\*\* | \*\*297\*\* |

# 

# \### 🧩 Input Features

# 

# The system uses 13 input features:

# 

# ```text

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

