# 37112025_Churning_customers
#video demo for the app
https://youtu.be/axf9ZA1Z7Ls
# Customer Churn Prediction App

## Overview

This web application is designed to predict the likelihood of customer churn based on various input features. It uses a machine learning model trained on historical customer data to provide predictions for new inputs.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Input Features](#input-features)
- [Deployment](#deployment)
- [Built With](#built-with)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Features

- Predicts the likelihood of customer churn.
- User-friendly web interface for inputting customer attributes.
- Provides insights into the model's prediction and probability.

## Getting Started

### Prerequisites

- Python 3.x
- [Streamlit](https://www.streamlit.io/)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/customer-churn-prediction-app.git
    ```

2. Install dependencies:

    ```bash
    cd customer-churn-prediction-app
    pip install -r requirements.txt
    ```

## Usage

1. Run the Streamlit app:

    ```bash
    streamlit run app.py
    ```

2. Open your web browser and go to [http://localhost:8501](http://localhost:8501) to use the app.

## Input Features

The app accepts the following input features:

- Total Charges
- Monthly Charges
- Tenure (Months)
- Customer ID
- Contract Type
- Payment Method
- Online Security
- Tech Support
- Internet Service
- Gender
- Device Protection
- Paperless Billing
- Multiple Lines

## Deployment

This app can be deployed on various hosting platforms such as Heroku, Streamlit Sharing, or others. Follow the hosting provider's documentation for deployment instructions.

## Built With

- [Streamlit](https://www.streamlit.io/) - The web framework used for building the app.
- [scikit-learn](https://scikit-learn.org/) - Machine learning library for the model.
- [Pandas](https://pandas.pydata.org/) - Data manipulation library.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Special thanks to [Any additional libraries or resources you used or people you want to acknowledge.]
