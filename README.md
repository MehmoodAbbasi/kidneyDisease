# Chronic Kidney Disease (CKD) Prediction System

## Overview
This is a Django-based web application for predicting Chronic Kidney Disease (CKD) using machine learning models. The system allows user management, patient data handling, diet recommendations, appointment scheduling, calorie tracking, and wellness guidance (yoga and workout plans).

## Features
- **User Authentication & Role Management**: Admin, Doctor, and Patient roles.
- **Patient Management**: Stores patient personal details and medical history.
- **CKD Prediction**: Uses machine learning models to predict CKD based on medical parameters.
- **Diet Recommendations**: Personalized meal plans for CKD patients.
- **Appointment Scheduling**: Book and manage consultations with doctors and health counselors.
- **Calorie Tracking**: Logs daily calorie intake and burnt calories.
- **Wellness Support**: Yoga, breathing exercises, and workout guidelines.

## Technologies Used
- **Backend**: Django, Python
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MySQL
- **Machine Learning**: SVM, Logistic Regression, KNN, Neural Network, Decision Tree, Random Forest
- **Deployment**: AWS (planned)

## Installation
### Prerequisites
- Python 3.x
- Django
- MySQL Workbench

### Setup Instructions
1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ckd-prediction-system.git
   cd ckd-prediction-system
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database settings** in `settings.py`

5. **Apply migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open `http://127.0.0.1:8000/` in your browser.
   - Login with the superuser credentials.
