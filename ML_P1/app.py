import streamlit as st
import numpy as np
import joblib

# Load the trained model
model = joblib.load('model.pkl')

# Streamlit app title
st.title("🏠 Boston House Price Prediction App")
st.write("Enter the details below to estimate the selling price of a house in Boston.")

# Sidebar info
st.sidebar.header("About")
st.sidebar.info(
    """
    This app uses a **Decision Tree Regressor** trained on the **Boston Housing Dataset**  
    to predict home prices based on:
    - Number of rooms  
    - Neighborhood poverty level (%)  
    - Student-teacher ratio
    """
)

# User inputs
st.subheader("Enter House Features")

rooms = st.number_input("Total number of rooms in home:", min_value=1, max_value=20, value=5)
poverty = st.number_input("Neighborhood poverty level (%):", min_value=0.0, max_value=100.0, value=10.0)
student_teacher_ratio = st.number_input("Student-teacher ratio:", min_value=1.0, max_value=50.0, value=15.0)

# Prediction button
if st.button("Predict Price 💰"):
    # Prepare input for prediction
    input_data = np.array([[rooms, poverty, student_teacher_ratio]])
    
    # Predict
    predicted_price = model.predict(input_data)[0]
    
    # Display result
    st.success(f"🏡 The estimated house price is: **${predicted_price:,.2f}**")

# Footer
st.markdown("---")
st.caption("Developed by **Data Pulse** Team")
