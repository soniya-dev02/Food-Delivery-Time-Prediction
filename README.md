## Food Delivery Time Prediction

A machine learning-based web application that predicts the estimated food delivery time based on delivery-related information.

### Project Overview

This project uses a Random Forest regression model to predict food delivery time. The trained model is integrated with a Flask web application where users can enter delivery details and receive an estimated delivery time.

The application also uses MySQL for user registration and login management.

### Technologies Used

- Python
- Flask
- Pandas
- NumPy
- Scikit-learn
- Joblib
- MySQL
- MySQL Connector
- HTML
- CSS

### Features

- Food delivery time prediction
- Random Forest regression model
- Flask-based web application
- MySQL database integration
- User registration and login
- Session-based access to prediction
- Delivery time estimation based on:
  - Distance
  - Traffic Level
  - Preparation Time
  - Courier Experience
  - Weather
  - Time of Day
  - Vehicle Type

### Machine Learning

The project uses a Random Forest regression model to predict estimated food delivery time.

The input features include:

- Distance (km)
- Traffic Level
- Preparation Time (minutes)
- Courier Experience (years)
- Weather
- Time of Day
- Vehicle Type

The workflow includes:

- Data preprocessing
- Feature encoding
- Model training
- Model evaluation
- Prediction

### Web Application

The Flask application provides the following pages:

- Home
- About
- Methodology
- Prediction
- Login
- Registration
- Logout

Users need to log in before accessing the prediction page.

### Project Structure

```text
Food-Delivery-Time-Prediction/
│
├── static/
├── templates/
├── app.py
├── Food_Delivery_Times.csv
├── rf_model_delivery_time.pkl
└── README.md
