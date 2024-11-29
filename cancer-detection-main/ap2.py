import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

# Function to load data
def load_data():
    uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
    if uploaded_file is not None:
        # Read the uploaded CSV file
        cancer = pd.read_csv(uploaded_file)
        return cancer
    else:
        st.warning("Please upload a CSV file.")
        return None

# Load the data
cancer = load_data()

if cancer is not None:
    # Exploratory Data Analysis
    st.write("## Dataset Overview")
    st.write(cancer.head())
    
    # Visualize distribution of diagnosis
    d = cancer["diagnosis"].value_counts()
    keys = d.keys()
    values = d.values
    plt.bar(keys, values, label='Diagnosis Counts')
    plt.xlabel('Diagnosis')
    plt.ylabel('Count')
    plt.title('Count of different diagnoses')
    st.pyplot(plt)

    # Preprocessing steps
    cancer.drop("id", axis=1, inplace=True)
    LabelEncoder_y = LabelEncoder()
    cancer['diagnosis'] = LabelEncoder_y.fit_transform(cancer['diagnosis'].values)

    # Reducing to 5 features and renaming them with cancer-related terms
    cancer = cancer[['diagnosis', 'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean']]
    cancer.columns = ['Diagnosis', 'Tumor Size', 'Cell Texture', 'Cell Shape', 'Nucleus Size', 'Chromatin']

    # Splitting the dataset into features and labels
    x = cancer.loc[:, cancer.columns != 'Diagnosis'].values
    y = cancer['Diagnosis'].values

    # Train/Test split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0)

    # Feature Scaling
    sc = StandardScaler()
    x_train = sc.fit_transform(x_train)
    x_test = sc.transform(x_test)

    # Model training
    def models(x_train, y_train):
        log = LogisticRegression(random_state=0)
        log.fit(x_train, y_train)
        tree = DecisionTreeClassifier(criterion="entropy", random_state=0)
        tree.fit(x_train, y_train)
        forest = RandomForestClassifier(n_estimators=50, criterion="entropy", random_state=0)
        forest.fit(x_train, y_train)
        return [{'name': 'Logistic Regression', 'model': log},
                {'name': 'Decision Tree', 'model': tree},
                {'name': 'Random Forest', 'model': forest}]

    trained_models = models(x_train, y_train)

    # Test and evaluate the models
    for model in trained_models:
        st.write(f"Model: {model['name']}")
        predictions = model['model'].predict(x_test)
        st.write("Classification Report:")
        st.text(classification_report(y_test, predictions))
        st.write("Accuracy Score:", accuracy_score(y_test, predictions))
    
    # Sample input prediction
    st.write("## Make a Prediction")
    input_values = []
    feature_names = ['Tumor Size', 'Cell Texture', 'Cell Shape', 'Nucleus Size', 'Chromatin']
    
    for feature in feature_names:
        value = st.number_input(f'{feature}', min_value=0.0, format="%.2f")
        input_values.append(value)

    if st.button("Predict"):
        sample_input = np.array([input_values])
        for model in trained_models:
            model_name = model['name']
            prediction = model['model'].predict(sample_input)
            diagnosis = 'Malignant (Cancer Detected)' if prediction[0] == 1 else 'Benign (No Cancer Detected)'
            st.write(f"Model: {model_name}")
            st.write(f"Predicted Diagnosis: {diagnosis}")
