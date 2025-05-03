import streamlit as st
import pandas as pd
import numpy as np
import pickle
import requests  # For calling the LLM API (like Hugging Face)

# Load your model and scaler
model_path = 'model/diabetes_model.pkl'
scaler_path = 'model/scaler.pkl'

with open(model_path, 'rb') as file:
    model = pickle.load(file)

with open(scaler_path, 'rb') as file:
    scaler = pickle.load(file)

# Function to take user input
def user_input_features():
    pregnancies = st.number_input('Pregnancies', 0, 20, 1)
    glucose = st.number_input('Glucose', 0, 300, 100)
    blood_pressure = st.number_input('Blood Pressure', 0, 150, 70)
    skin_thickness = st.number_input('Skin Thickness', 0, 99, 20)
    insulin = st.number_input('Insulin', 0, 900, 79)
    bmi = st.number_input('BMI', 0.0, 70.0, 32.0)
    diabetes_pedigree_function = st.number_input('Diabetes Pedigree Function', 0.0, 3.0, 0.5)
    age = st.number_input('Age', 21, 100, 33)

    data = {
        'Pregnancies': pregnancies,
        'Glucose': glucose,
        'BloodPressure': blood_pressure,
        'SkinThickness': skin_thickness,
        'Insulin': insulin,
        'BMI': bmi,
        'DiabetesPedigreeFunction': diabetes_pedigree_function,
        'Age': age
    }
    features = pd.DataFrame(data, index=[0])
    return features

# Function to generate an explanation (simulated as if it comes from LLM)
def generate_llm_explanation(prediction, features):
    # You can replace this with an actual LLM API call (e.g., Hugging Face, OpenAI) for production
    if prediction == 1:  # Diabetic
        explanation = (
            "The model predicts diabetic based on the following factors:\n"
            "- High glucose level: A higher glucose level can be an indicator of insulin resistance.\n"
            "- BMI: A higher BMI suggests a higher risk of diabetes.\n"
            "- Age: Older individuals tend to have a higher risk.\n"
            "- Family history of diabetes (Diabetes Pedigree Function): A higher score indicates a family history.\n"
        )
    else:  # Non-Diabetic
        explanation = (
            "The model predicts non-diabetic based on the following factors:\n"
            "- Normal glucose level: Indicates a healthy level of insulin sensitivity.\n"
            "- BMI: A normal BMI reduces the risk of developing diabetes.\n"
            "- Age: A younger individual with no significant risk factors.\n"
        )
    
    # Here we simulate the response as if it came from an LLM (e.g., Hugging Face API)
    simulated_llm_response = f"LLM Response: {explanation}"
    
    return simulated_llm_response

# Streamlit app UI
st.title('🩺 Diabetes Prediction App')

# Take user input
df = user_input_features()

st.subheader('🔎 User Input Parameters')
st.write(df)

# Button to predict
if st.button('Predict'):
    # Scale the input data
    df_scaled = scaler.transform(df)

    # Make the prediction
    prediction = model.predict(df_scaled)

    # Show prediction
    st.subheader('🧬 Prediction Result')
    diabetes = np.array(['Non-diabetic', 'Diabetic'])
    st.success(f'The model predicts: **{diabetes[prediction][0]}**')

    # Generate and show the explanation as if it came from the LLM
    explanation = generate_llm_explanation(prediction[0], df.iloc[0])
    st.subheader('💬 Explanation (from LLM)')
    st.write(explanation)
