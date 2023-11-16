# -*- coding: utf-8 -*-
"""37112025_Churning_Customers

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1av29zW5c3RbAa39MrurCkaXRypzxtGMP
"""

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import pandas as pd
import numpy as np
from google.colab import drive
drive.mount('/content/drive')

df =pd.read_csv('/content/drive/My Drive/Colab Notebooks/CustomerChurn_dataset.csv')

df.head()

df.info()

"""# Extracting the relevant features that can define a customer churn"""

df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df['TotalCharges'] = df['TotalCharges'].astype(float)
df = df.drop('customerID', axis=1)

categorical_cols = df.select_dtypes(exclude='number').columns
numeric_cols = df.select_dtypes(include='number').columns
numeric_cols = df[numeric_cols].fillna(method='ffill')
categorical_cols = df[categorical_cols].fillna(method='ffill')

for col in categorical_cols.columns:
    categorical_cols[col], _ = pd.factorize(categorical_cols[col])

# Concatenate the encoded categorical columns with the rest of the DataFrame
final_df = pd.concat([df.drop(columns=categorical_cols), categorical_cols], axis=1)
final_df = final_df.dropna()

# Target variable
X = final_df.drop('Churn', axis=1) # Features (exclude the target variable 'Churn')
column_names = final_df.drop('Churn', axis=1).columns
y = final_df['Churn']

X.head()

# Create and fit a Random Forest Classifier model
from sklearn.ensemble import RandomForestClassifier

rf_classifier = RandomForestClassifier(random_state=42)
# Split the data into training and testing sets
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf_classifier.fit(X, y)

feature_importance = pd.Series(rf_classifier.feature_importances_, index = X.columns)

feature_importance

#DataFrame to store feature names and their importances
feature_importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': feature_importance})

# Sort the DataFrame by importance in descending order
feature_importance_df = feature_importance.sort_values(ascending=False)

feature_importance_df

important_columns = ['TotalCharges', 'MonthlyCharges', 'tenure', 'Contract', 'PaymentMethod',
                'OnlineSecurity', 'TechSupport', 'gender', 'InternetService', 'OnlineBackup',
                'PaperlessBilling', 'MultipleLines', 'DeviceProtection']

final_df_selected = X[important_columns]
final_df_selected =pd.concat([final_df_selected,y], axis=1)

final_df_selected.info()

"""## Exploratory Data Analysis"""

import seaborn as sns
import matplotlib.pyplot as plt

# List of categoric features
features_to_analyze = ['SeniorCitizen', 'gender', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines',
                        'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport',
                        'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod']


for feature in features_to_analyze:
    plt.figure(figsize=(12, 8))
    sns.countplot(x=feature, hue='Churn', data=df)
    plt.title(f'Churn Distribution by {feature}')
    plt.show()

"""From the above barplot we realise that customers with longer-term contracts are less likely to churn.

Payment methods such as Mailed check, bank transfer, credit card are associated with lower churn, whIle those with electronic check are more likely to churn so promoting these methods could be beneficial.

Customers using online security and tech support services are less likely to churn.

Customers with fiber optic internet service may be more prone to churn, so understanding their needs is crucial.
Customers with device protection, streaming services,  are less likely to churn.
Customers with no dependents have high churn probability compared to those that have


Gender, Partner, and MultipleLines have a lower impact to customers likelyhood of churning from the graphs.
Senior Citizens, Dependents, and Phone Service:

Senior Citizens and Dependents: These features have lower churn thus less importance in predicting churn.

EDA for numeric features
"""

# Correlation heatmap to identify feature relationships
correlation_matrix = numeric_cols.corr()
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Correlation Heatmap of Numeric Features')
plt.show()

# Distribution of individual numeric features
for column in numeric_cols.columns:
    plt.figure(figsize=(8, 6))
    sns.histplot(data=df, x=column, kde=True, bins=30, color='skyblue')
    plt.title(f'Distribution of {column}')
    plt.show()

# Summary statistics for numerical features
print(final_df.describe())

# Frequency of categories in categorical features
for column in final_df.select_dtypes(include='object').columns:
    print(final_df[column].value_counts())

import matplotlib.pyplot as plt
plt.scatter(df['MonthlyCharges'], df['Churn'])
plt.xlabel('MonthlyCharges')
plt.ylabel('Churn')
plt.title('Scatter Plot: MonthlyCharges vs. Churn')

import seaborn as sns
import matplotlib.pyplot as plt

# Example: Bar plot for the relationship between 'Contract' and 'Churn'

sns.pairplot(df, hue='Churn')

import seaborn as sns
import matplotlib.pyplot as plt

# Calculate correlations between all numerical features and 'Churn'
correlation_matrix = df.corr()

plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()

"""In general, the customer profile generated from our Exploratory data Analysis is that Long-tenured customers with higher total charges, committed to longer contracts, and using stable payment methods are less likely to churn.

Customers with higher monthly charges, shorter tenures, and potentially using certain internet services or lacking additional protections might be more prone to churn.
Also offering additional services like online security, tech support, and various streaming options can positively influence customer retention.
Features like gender, partnership status, and having multiple lines have some impact but are less significant in predicting churn.

## defining and training of the model
"""

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

Y = final_df_selected['Churn']  # Target variable
x = final_df_selected.drop('Churn', axis=1).values
scaler = StandardScaler()
scaler.fit(x)
X_scaled = scaler.transform(x)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=42)

import pickle

with open('scaler.pkl', 'wb') as scaler_file:
    pickle.dump(scaler, scaler_file)

!pip install scikeras

import tensorflow as tf
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.metrics import accuracy_score, make_scorer, roc_auc_score
from scikeras.wrappers import KerasClassifier

# Function to create the MLP model
def create_model(optimizer='adam', hidden_layer1_units=64, hidden_layer2_units=32):
    input_layer = Input(shape=(X_train.shape[1],))
    hidden_layer1 = Dense(hidden_layer1_units, activation='relu')(input_layer)
    hidden_layer2 = Dense(hidden_layer2_units, activation='relu')(hidden_layer1)
    output_layer = Dense(1, activation='sigmoid')(hidden_layer2)
    model = Model(inputs=input_layer, outputs=output_layer)
    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Create KerasClassifier for use with GridSearchCV
model = KerasClassifier(model=create_model, epochs=10, batch_size=32, verbose=0, hidden_layer1_units=32, hidden_layer2_units=16)

param_grid = {
    'optimizer': ['adam', 'sgd', 'rmsprop'],
    'hidden_layer1_units': [32, 64, 128],
    'hidden_layer2_units': [16, 32, 64]
}

# Define custom scorer for GridSearchCV based on AUC score
auc_scorer = make_scorer(roc_auc_score, greater_is_better=True)

# Perform GridSearchCV with cross-validation
grid_search = GridSearchCV(estimator=model, param_grid=param_grid, scoring=auc_scorer, cv=StratifiedKFold(n_splits=5), verbose=1)
grid_result = grid_search.fit(X_train, y_train)

print(f'Best Parameters: {grid_result.best_params_}')
print(f'Best AUC Score: {grid_result.best_score_}')

# Evaluate the best model on the test set
best_model = grid_result.best_estimator_
y_pred = best_model.predict(X_test)
y_pred_binary = (y_pred > 0.5).astype(int)
accuracy_best = accuracy_score(y_test, y_pred_binary)
auc_score_best = roc_auc_score(y_test, y_pred)
print(f'Test Accuracy (Best Model): {accuracy_best}')
print(f'AUC Score (Best Model): {auc_score_best}')

"""Model optimisation"""

from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import SGD


# Define the model using the optimized hyperparameters
input_layer = Input(shape=(X_train.shape[1],))
hidden_layer1 = Dense(128, activation='relu')(input_layer)
hidden_layer2 = Dense(32, activation='relu')(hidden_layer1)
output_layer = Dense(1, activation='sigmoid')(hidden_layer2)
optimized_model = Model(inputs=input_layer, outputs=output_layer)

# Compile the model with the SGD optimizer
optimized_model.compile(optimizer=SGD(), loss='binary_crossentropy', metrics=['accuracy'])

# Train the model on the entire training set
optimized_model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=1)

# Evaluate the optimized model on the test set
y_pred_optimized = optimized_model.predict(X_test)
y_pred_optimized_binary = (y_pred_optimized > 0.5).astype(int)

accuracy_optimized = accuracy_score(y_test, y_pred_optimized_binary)
auc_score_optimized = roc_auc_score(y_test, y_pred_optimized)

print(f'Test Accuracy (Optimized Model): {accuracy_optimized}')
print(f'AUC Score (Optimized Model): {auc_score_optimized}')

import pickle
# Define the file path where you want to save the model
model = optimized_model



with open('model.pkl', 'wb') as file:
    pickle.dump(model, file)

with open('scaler.pkl', 'wb') as scaler_file:
    pickle.dump(scaler, scaler_file)


with open('model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

with open('scaler.pkl', 'rb') as scaler_file:
    loaded_scaler = pickle.load(scaler_file)

