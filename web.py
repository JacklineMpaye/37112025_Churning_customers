import streamlit as st
import pandas as pd
import pickle



st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📉",
    layout="wide",
    initial_sidebar_state="expanded",
)
# Load the model and scaler
import os

model_path = 'model.pkl'

# Check if the file exists
if not os.path.isfile(model_path):
    print(f"Error: File '{model_path}' not found.")
else:
    try:
        # Open the file in binary mode and load the model
        with open(model_path, 'rb') as model_file:
            model = pickle.load(model_file)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading the model: {e}")



# Get the script directory
script_directory = os.path.dirname(os.path.abspath(__file__))

# Specify the full path to the scaler.pkl file
scaler_path = os.path.join(script_directory, 'scaler.pkl')

# Print debugging information
print("Script Directory:", script_directory)
print("Scaler Path:", scaler_path)

# Check if the file exists
if os.path.exists(scaler_path):
    # Load the scaler model
    with open(scaler_path, 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)
else:
    print(f"Error: File not found at path {scaler_path}")
    scaler = None  # Set scaler to None or handle the error as appropriate

# Now you can use the 'scaler' object as needed in the rest of your code


# Create a Streamlit app

st.title("Customer Churn Prediction App")
st.write("Enter customer attributes to predict the likelihood of churn.")
st.write("")

# Define input fields for user input
Total_charges = st.number_input("Total Charges", min_value=0.0, value=0.0, step=0.01)
Monthly_charges = st.number_input("Monthly Charges", min_value=0.0, value=0.0, step=0.01)
tenure = st.number_input("Tenure (Months)", min_value=0, value=0)
Contract = st.selectbox("Contract Type",["Month_to_month", "one year", "two year"])
payment_method = st.selectbox("Payment Method",["Electronic check", "Mailed check", "Bank transfer(automatic)", "Credit card(automatic)"])
online_backup = st.selectbox("online backup",["Yes", "No", "No Internet Service"])
gender = st.selectbox("gender", ["Male", "Female"])
online_security = st.selectbox("Online Security", ["Yes", "No", "No Internet Service"])
tech_support = st.selectbox("Tech Support", ["Yes", "No", "No Internet Service"])
internet_service = st.selectbox("Internet Service", ["DSL", "Fiber Optic", "No"])
device_protection = st.selectbox("Device Protection", ["Yes", "No", "No Internet Service"])
paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])
multiple_lines = st.selectbox("Multiple Lines", ["Yes", "No", "No Phone Service"])


button = st.button('Predict Churn')
reset = st.button('Reset')

if button:
    input_data = {
        "TotalCharges": Total_charges,
        "MonthlyCharges": Monthly_charges,
        "tenure": tenure,
        "Contract Type": Contract,
        "PaymentMethod": payment_method,
        "OnlineSecurity": online_security,
        "TechSupport": tech_support,
        "InternetService": internet_service,
        "gender": gender,
        "DeviceProtection": device_protection,
        "PaperlessBilling": paperless_billing,
        "MultipleLines": multiple_lines,
        "online backup": online_backup
    }

    input_df = pd.DataFrame([input_data])
    for col in ['Contract Type','gender', 'OnlineSecurity', 'TechSupport', 'InternetService', 'DeviceProtection', 'PaperlessBilling', 'MultipleLines', 'PaymentMethod','online backup']:
  
       input_data[col] = pd.factorize([input_data[col]])[0][0]

    input_df = pd.DataFrame([input_data])

# Extract the columns to be scaled
    columns_to_scale = ['TotalCharges', 'MonthlyCharges', 'tenure', 'Contract Type'] + ['gender', 'OnlineSecurity', 'TechSupport', 'InternetService', 'DeviceProtection', 'PaperlessBilling', 'MultipleLines', 'PaymentMethod','online backup']
    input_for_scaling = input_df[columns_to_scale]

    
    
    # Assuming col is the column name you want to factorize
    
    scaled_input = scaler.transform(input_for_scaling)
    

    

   #scaled_input = scaler.transform(input_df[col].values.reshape(1, -1))

    prediction = model.predict(scaled_input)
    if prediction.shape[1] > 1:
    # Assuming binary classification, extract the probability of class 1
        churn_probability = prediction[0][1]
    else:
    # If only one class, use the probability of that class
        churn_probability = prediction[0][0]
    

   
    
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    st.text("")
    confidence_factor = 82
    st.write(f"The predicted likelihood of churn is: {churn_probability*100:.2f}%", key="stText")
    st.write(f"The model predicts {'Churn' if churn_probability >= 0.5 else 'No Churn'}", key="stText")
    st.title("Model Confidence Viewer")
    st.write(f"Confidence Factor: {confidence_factor}%")
