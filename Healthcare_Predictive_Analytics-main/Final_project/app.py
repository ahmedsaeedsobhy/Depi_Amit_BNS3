import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

# Setup page
st.set_page_config(page_title="Heart Attack Prediction", page_icon="❤️", layout="wide")

st.title("Heart Attack Prediction System")
st.markdown("---")

# Sidebar for controls
st.sidebar.title("Settings & Controls")

# Load data function
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('Medicaldataset.csv')
        return df
    except FileNotFoundError:
        st.error("Data file not found. Please ensure 'Medicaldataset.csv' is in the same directory.")
        return None

df = load_data()

if df is not None:
    # Data preprocessing pipeline
    st.sidebar.subheader("Data Preprocessing")
    
    # Show raw data
    if st.sidebar.checkbox("Show Raw Data"):
        st.subheader("Raw Data")
        st.dataframe(df)
    
    # Data cleaning steps
    st.subheader("Data Preprocessing Pipeline")
    
    # Step 1: Convert Result to numeric
    st.write("**Step 1: Encoding Target Variable**")
    df['Result_Encoded'] = df['Result'].map({'positive': 1, 'negative': 0})
    df_cleaned = df.drop(columns=['Result'])
    st.write(f"✅ Target variable encoded. Shape: {df_cleaned.shape}")
    
    # Step 2: Remove outliers (Heart rate = 1111)
    st.write("**Step 2: Removing Outliers**")
    heart_rate_col = 'Heart rate'
    rows_to_remove = df_cleaned[df_cleaned[heart_rate_col].astype(str).str.contains('1111', na=False)]
    df_cleaned = df_cleaned[~df_cleaned[heart_rate_col].astype(str).str.contains('1111', na=False)]
    st.write(f"✅ Removed {len(rows_to_remove)} outliers. New shape: {df_cleaned.shape}")
    
    # Step 3: Convert to numeric
    st.write("**Step 3: Converting to Numeric Types**")
    numeric_cols = df_cleaned.columns
    for col in numeric_cols:
        df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')
    st.write("✅ All columns converted to numeric")
    
    # Show cleaned data
    if st.sidebar.checkbox("Show Cleaned Data"):
        st.subheader("Cleaned Data")
        st.dataframe(df_cleaned)

    # Data Visualization
    st.sidebar.subheader("Data Visualization")
    
    if st.sidebar.checkbox("Show Target Distribution"):
        st.subheader("Target Variable Distribution")
        
        target_distribution = df_cleaned['Result_Encoded'].value_counts()
        
        dist_df = pd.DataFrame({
            'Result': ['Positive (Disease)', 'Negative (Normal)'],
            'Count': target_distribution.values
        })
        
        fig = px.bar(
            dist_df, 
            x='Result', 
            y='Count', 
            title='Target Variable Distribution',
            color='Result',
            text='Count'
        )
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        st.plotly_chart(fig)

    # Feature distributions
    if st.sidebar.checkbox("Show Feature Distributions"):
        st.subheader("Feature Distributions")
        
        # Select feature to visualize
        features = ['Age', 'Heart rate', 'Systolic blood pressure', 
                   'Diastolic blood pressure', 'Blood sugar', 'CK-MB', 'Troponin']
        selected_feature = st.selectbox("Select Feature to Visualize", features)
        
        # Create distribution plot
        fig = px.histogram(df_cleaned, x=selected_feature, color='Result_Encoded',
                          title=f'Distribution of {selected_feature} by Result',
                          nbins=30, barmode='overlay')
        st.plotly_chart(fig)

    # Machine Learning Pipeline
    st.sidebar.subheader("Machine Learning")
    
    if st.sidebar.checkbox("Run ML Pipeline"):
        st.subheader("Machine Learning Pipeline")
        
        # Prepare features and target
        features = ['Age', 'Gender', 'Heart rate', 'Systolic blood pressure', 
                   'Diastolic blood pressure', 'Blood sugar', 'CK-MB', 'Troponin']
        X = df_cleaned[features]
        y = df_cleaned['Result_Encoded']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        st.write("**Step 4: Data Splitting and Scaling**")
        st.write(f"Training set: {X_train.shape[0]} samples")
        st.write(f"Test set: {X_test.shape[0]} samples")
        st.write("✅ Features scaled using StandardScaler")
        
        # Model selection
        st.write("**Step 5: Model Training**")
        model_option = st.selectbox("Select Model", 
                                   ["Random Forest", "Logistic Regression", "SVM"])
        
        if model_option == "Random Forest":
            model = RandomForestClassifier(n_estimators=100, random_state=42)
        elif model_option == "Logistic Regression":
            model = LogisticRegression(random_state=42)
        else:  # SVM
            model = SVC(random_state=42)
        
        # Train model
        if model_option == "SVM":
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
        
        # Calculate accuracy
        accuracy = accuracy_score(y_test, y_pred)
        
        st.write(f"**Step 6: Model Evaluation - {model_option}**")
        st.write(f"✅ Model trained successfully")
        st.metric("Accuracy", f"{accuracy:.3f}")

        # Confusion Matrix
        st.write("**Confusion Matrix**")
        cm = confusion_matrix(y_test, y_pred)
        
        fig, ax = plt.subplots()
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)
        ax.set_xlabel('Predicted')
        ax.set_ylabel('Actual')
        ax.set_title('Confusion Matrix')
        st.pyplot(fig, use_container_width=False)
        
        # Classification Report
        st.write("**Classification Report**")
        report = classification_report(y_test, y_pred, output_dict=True)
        report_df = pd.DataFrame(report).transpose()
        st.dataframe(report_df)

    # Prediction Interface
    st.sidebar.subheader("Prediction")
    
    if st.sidebar.checkbox("Make Prediction"):
        st.subheader("Make New Prediction")
        
        # Input fields for prediction
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age", min_value=0, max_value=120, value=50)
            gender = st.selectbox("Gender", ["Male", "Female"])
            heart_rate = st.number_input("Heart Rate", min_value=0, max_value=200, value=70)
            systolic_bp = st.number_input("Systolic BP", min_value=0, max_value=300, value=120)
        
        with col2:
            diastolic_bp = st.number_input("Diastolic BP", min_value=0, max_value=200, value=80)
            blood_sugar = st.number_input("Blood Sugar", min_value=0.0, max_value=500.0, value=100.0)
            ck_mb = st.number_input("CK-MB", min_value=0.0, max_value=100.0, value=2.0)
            troponin = st.number_input('Troponin (ng/mL)', min_value=0.0, max_value=10.0, value=0.003, step=0.001, format='%.3f')
        
        # Prepare input for prediction
        gender_encoded = 1 if gender == "Male" else 0
        input_data = np.array([[age, gender_encoded, heart_rate, systolic_bp, 
                              diastolic_bp, blood_sugar, ck_mb, troponin]])
        
        # Train a model for prediction (using all data for simplicity)
        features = ['Age', 'Gender', 'Heart rate', 'Systolic blood pressure', 
                   'Diastolic blood pressure', 'Blood sugar', 'CK-MB', 'Troponin']
        X = df_cleaned[features]
        y = df_cleaned['Result_Encoded']
        
        # Use Random Forest for prediction
        rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_model.fit(X, y)
        
        # Make prediction
        if st.button("Predict Heart Attack Risk"):
            prediction = rf_model.predict(input_data)[0]
            probability = rf_model.predict_proba(input_data)[0]
            
            if prediction == 1:
                st.error(f"🚨 High Risk of Heart Attack (Probability: {probability[1]:.2%})")
            else:
                st.success(f"✅ Low Risk of Heart Attack (Probability: {probability[0]:.2%})")
            
            # Show probability breakdown
            prob_df = pd.DataFrame({
                'Risk Level': ['Low Risk', 'High Risk'],
                'Probability': [probability[0], probability[1]]
            })
            
            # fig = px.bar(prob_df, x='Risk Level', y='Probability', 
            #             color='Risk Level', text='Probability')
            # fig.update_traces(texttemplate='%{text:.2%}', textposition='outside')
            # st.plotly_chart(fig)