<!-- # 🩺 MediScan: Multimodal AI Diagnostic Engine  
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/) 
[![TensorFlow](https://img.shields.io/badge/TensorFlow-VGG19-orange.svg)](https://www.tensorflow.org/) 
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Random%20Forest-yellow.svg)](https://scikit-learn.org/) 
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)  

---

## 📖 Overview  
**MediScan** is an end-to-end clinical decision support system designed for the early detection of **Asthma, Dengue, and Pneumonia**. Built to tackle the complexity of multimodal medical data, it bridges the gap between raw clinical inputs (blood reports, X-rays, spirometry) and actionable diagnostic insights.  

The project focuses on moving beyond single-disease silos to provide a unified, explainable framework for patient diagnostics.  

---

## ✨ Key Features  

- **Multimodal Diagnostics:** Processes tabular clinical data, imaging, and PDF lab reports  
- **Automated Data Extraction:** OCR-based CBC report parser with median imputation  
- **Explainable AI Integration:** Feature importance ranking for transparency  
- **Secure Architecture:** Role-based access (Patients, Doctors, Admins)  
- **Automated Reporting:** Downloadable PDF/CSV diagnostic summaries  

---

## 🧠 Machine Learning Pipelines  

### 1. Pneumonia Detection (Computer Vision)  
- **Architecture:** CNN with VGG19 (Transfer Learning)  
- **Data:** Chest X-ray images  
- **Preprocessing:** OpenCV normalization + Keras augmentation  
- **Performance:** **92.15% test accuracy**, up to **99.9% confidence**  

### 2. Dengue Prediction (Tabular + OCR)  
- **Architecture:** Random Forest Classifier  
- **Data:** CBC parameters (platelets, WBC, lymphocytes, hematocrit)  
- **Performance:**  
  - **91.80% test accuracy**  
  - **93.77% cross-validation score**  
  - Outperformed SVM & XGBoost  

### 3. Asthma Risk Assessment  
- **Architecture:** Random Forest Pipeline  
- **Data:** Spirometry + clinical data (FEV1, FeNO, Peak Flow, BMI, environment)  
- **Insights:**  
  - FEV1 → **32% importance**  
  - FeNO → **28% importance**  
- **Performance:** **>90% accuracy**  

---


## 🛠️ System Architecture  
![1](public/systemarchitecture.png)

---

## 🖼️ Screenshots  



![1](public/1.png)
![1](public/01.png)
![1](public/02.png)
![1](public/03.png)
![1](public/04.png)
![2](public/2.png)
![3](public/3.png)
![4](public/4.png)
![5](public/5.png) 

---

## 🛠️ Tech Stack  

- **Machine Learning:** Python, TensorFlow, Keras, Scikit-Learn  
- **Data Processing:** Pandas, NumPy, OpenCV  
- **Frontend:** Streamlit / React  
- **Backend:** FastAPI / Flask  

---

## 🚀 Installation & Local Setup  

```bash
# 1. Clone the repository
git clone https://github.com/Hussain-Tinwala/MediScan.git

# 2. Navigate to the project directory
cd Multiple-Disease-Prediction-Webapp

# 3. Create a virtual environment (Recommended)
python -m venv venv

# Activate environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the application
streamlit run Multiple-Disease-Prediction-Webapp/Frontend/app.py -->


# 🩺 MediScan — AI-Powered Healthcare Screening Platform

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![Keras](https://img.shields.io/badge/Keras-D00000?style=for-the-badge&logo=keras&logoColor=white)
![Scikit Learn](https://img.shields.io/badge/Scikit_Learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)

---

## 🚀 Why MediScan?

Access to healthcare is often delayed due to:

* Limited availability of doctors in rural areas
* Long waiting times for consultations
* Difficulty understanding medical reports
* Delayed diagnosis due to ignored symptoms

MediScan was built to explore how AI can assist in the **early screening of diseases** by analyzing multimodal medical data and providing preliminary diagnostic insights.

Rather than replacing doctors, the system acts as an intelligent screening assistant that helps users better understand their health data and encourages timely medical consultation.

By open-sourcing this architecture, MediScan provides a foundational, highly accurate diagnostic baseline for independent researchers and developers to fork, study, and expand without needing massive computational budgets.

---

## ✨ Core Features

### 🫁 Pneumonia Detection

Upload a chest X-ray and receive an AI-powered prediction using a VGG19-based deep learning model.

### 🦟 Dengue Prediction

Analyze CBC blood report parameters such as platelet count, WBC count, and hematocrit to assess dengue risk.

### 🌬️ Asthma Risk Assessment

Evaluate asthma likelihood using spirometry and clinical indicators such as FEV1, FeNO, BMI, and environmental factors.

### 📄 OCR-Based Report Processing

Extract clinical parameters directly from uploaded laboratory reports.

### 📊 Explainable Predictions

View feature importance and model insights to understand how predictions are generated.

### 📑 Automated Reports

Generate downloadable PDF and CSV diagnostic summaries.

---

## 🏗️ System Architecture

![1](public/systemarchitecture.png)

The platform follows a modular architecture where uploaded medical data passes through preprocessing pipelines before being routed to disease-specific machine learning models.

The prediction results are then combined with explainability insights and presented through an intuitive healthcare dashboard.

---

## 🔄 Workflow

```text
Medical Input
      │
      ▼
Data Processing & OCR
      │
      ▼
Disease-Specific AI Models
      │
      ▼
Prediction Engine
      │
      ▼
Explainability Layer
      │
      ▼
Diagnostic Report
```

---

## 🧠 AI Models

| Disease   | Model         | Performance     |
| --------- | ------------- | --------------- |
| Pneumonia | CNN + VGG19   | 92.15% Accuracy |
| Dengue    | Random Forest | 91.80% Accuracy |
| Asthma    | Random Forest | >90% Accuracy   |

---

## 📈 Model Highlights

### Pneumonia Detection

* Transfer Learning using VGG19
* Chest X-Ray Classification
* OpenCV Image Processing
* Data Augmentation with Keras

### Dengue Prediction

* CBC Parameter Analysis
* OCR-Integrated Workflow
* Random Forest Classifier
* 93.77% Cross Validation Score

### Asthma Assessment

* Spirometry-Based Prediction
* Feature Importance Analysis
* Clinical Risk Assessment Pipeline

---

## 💡 What Makes This Project Unique?

Unlike traditional disease prediction systems that focus on a single condition, MediScan integrates multiple diagnostic pipelines into a unified platform.

The project demonstrates how:

* Computer Vision
* Machine Learning
* OCR
* Explainable AI

can work together to create an end-to-end healthcare screening solution.

---

## 📸 Screenshots

### Dashboard

![1](public/1.png)

### Pneumonia Module

![1](public/01.png)


![1](public/02.png)


![1](public/03.png)


![1](public/04.png)

### Asthma Module
![2](public/2.png)

![3](public/3.png)

### Dengue Module
![4](public/4.png)

![5](public/5.png)

---

## 🛠️ Tech Stack

### AI & Machine Learning

* Python
* TensorFlow
* Keras
* Scikit-Learn

### Data Processing

* Pandas
* NumPy
* OpenCV

### Frontend

* Streamlit
* React

### Utilities

* OCR Processing
* PDF Parsing
* Report Generation

---

## 📊 Dataset

The models were trained using publicly available datasets from Kaggle and educational research resources.

Synthetic medical reports were generated to evaluate OCR extraction and report-processing workflows.

This project should be considered an AI healthcare proof-of-concept rather than a clinically validated medical system.

---

## 🚀 Future Roadmap

### 🤖 AI Healthcare Assistant

One planned enhancement is a conversational healthcare assistant capable of:

* Talking with users through voice or chat
* Collecting symptoms interactively
* Identifying probable disease categories
* Automatically routing users to the appropriate screening workflow

This would transform MediScan into a unified AI-driven healthcare assistant rather than requiring users to manually select disease modules.

### 📈 Expansion

Future disease modules may include:

* Diabetes
* Heart Disease
* Kidney Disease
* Liver Disease

---

## ⚙️ Installation

```bash
# Clone repository
git clone https://github.com/Hussain-Tinwala/MediScan.git

# Navigate to project
cd Multiple-Disease-Prediction-Webapp

# Create virtual environment
python -m venv venv

# Activate environment

# Linux / Mac
source venv/bin/activate

# Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run Multiple-Disease-Prediction-Webapp/Frontend/app.py
```

---

## 🤝 Contributing & Community Roadmap (Open Source Initiative)
MediScan is transitioning into a community-driven open-science tool. We are currently building out automated maintainer infrastructure to make contributing seamless. 

**Where we need help (Current focus areas):**
* **🩺 Diagnostic Expansion:** Adding new modules (e.g., Diabetes, Liver Disease) following the existing pipeline architecture.
* **UI/UX Refinement:** Optimizing the Streamlit frontend for mobile responsiveness.
* **Documentation:** Expanding our ML pipeline documentation and unit tests.

We are actively tagging `good first issue` and `help wanted` tickets in the repository. Please check the Issues tab to get started!

---

## ⚠️ Disclaimer

This project was developed for educational, research, and demonstration purposes.

Predictions generated by MediScan should not be considered medical advice. Always consult qualified healthcare professionals for diagnosis and treatment decisions.
