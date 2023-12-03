# BACKEND FUNCTIONS
# Need to make a csv with important columns

import os
#import warnings
import numpy as np
import pandas as pd
from joblib import load
from keras.layers import Dense
from keras.models import Sequential
from sklearn.decomposition import PCA
from sklearn.linear_model import Perceptron
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
from pdb import set_trace as bp

#warnings.filterwarnings('ignore')

data_filepath = ''
saved_models_path = r'C:\Documents\Kivy_App\PHA_App_Final\MATLS_4ML3_PROJECT\saved_models'

def send_csv(filepath):
    global data_filepath
    data_filepath = filepath
    print(f"Recieved data: {filepath}")
    return 0

def compute_prediction():
    prediction = get_prediction()
    return prediction

def encode_features(df):
    orbit_id_classes = ['10','11','12','13','14','15','16','17','18','19','2','20','21','22','23','24','25','26','27','28','29','3','30','31','32','33','34','35','36','37','38','39','4','40','41','5','6','7','8','9','JPL 1','JPL 10','JPL 11','JPL 12','JPL 13','JPL 14','JPL 15','JPL 16','JPL 17','JPL 18','JPL 19','JPL 2','JPL 20','JPL 21','JPL 22','JPL 23','JPL 24','JPL 25','JPL 26','JPL 27','JPL 28','JPL 29','JPL 3','JPL 30','JPL 31','JPL 32','JPL 33','JPL 34','JPL 35','JPL 36','JPL 37','JPL 38','JPL 39','JPL 4','JPL 40','JPL 41','JPL 5','JPL 6','JPL 7','JPL 8','JPL 9','Other']
    class_classes = ['APO','AST','ATE','CEN','HYA','IEO','IMB','MBA','MCA','OMB','TJN','TNO']

    # Loading the label encoder from the saved file
    loaded_label_encoder = load(os.path.join(saved_models_path, 'label_encoder.joblib'))

    df['neo'] = loaded_label_encoder.transform(df['neo'])

    df['orbit_id'] = pd.Categorical(df['orbit_id'], categories=orbit_id_classes)

    df = pd.get_dummies(df, columns=['orbit_id'], prefix=['orbit_id'], prefix_sep='_', sparse=False, dtype = np.uint8)

    df['class'] = pd.Categorical(df['class'], categories=class_classes)

    df = pd.get_dummies(df, columns=['class'], prefix=['class'], prefix_sep='_', sparse=False, dtype = np.uint8)

    return df

def standardize_features(df, numerical_features):
    # Loading the standard scalar from the saved file
    loaded_standard_scalar = load(os.path.join(saved_models_path, 'scaler_model.joblib'))

    df[numerical_features] = loaded_standard_scalar.transform(df[numerical_features])

    return df

def pca_transform(df):
    # Loading the pca transform from the saved file
    loaded_pca_transform = load(os.path.join(saved_models_path, 'pca_model.joblib'))

    df_pca = loaded_pca_transform.transform(df)

    return df_pca

def perceptron(df):
    # Loading the perceptron model from the saved file
    loaded_perceptron = load(os.path.join(saved_models_path, 'perceptron_model.joblib'))

    prediction = loaded_perceptron.predict(df)

    return prediction[0]

def logistic_regression(df):
    # Loading the logistic regression model from the saved file
    loaded_logistic_regression = load(os.path.join(saved_models_path, 'logistic_regression_model.joblib'))

    prediction = loaded_logistic_regression.predict(df)

    return prediction[0]

def ANN(df):
    # Loading the ANN model from the saved file
    loaded_ANN = load_model(os.path.join(saved_models_path, 'ANN_model.h5'))

    prediction = (loaded_ANN.predict(df) > 0.5).astype(np.uint8)

    return prediction[0][0]


def get_prediction():
    df = pd.read_excel(data_filepath, sheet_name='Data')

    numerical_features = df.select_dtypes(exclude=['object'])

    df_encoded = encode_features(df)

    df_standardized = standardize_features(df_encoded, numerical_features.columns)

    test_pca = pca_transform(df_standardized)

    predictions = []

    percepetron_prediction = predictions.append(perceptron(test_pca))


    logistic_regression_prediction = predictions.append(logistic_regression(test_pca))


    ANN_prediction = predictions.append(ANN(test_pca))

    print("Predictions:", predictions)

    prediction = max(set(predictions), key=lambda x: predictions.count(x))

    print("Final Prediction:",prediction)

    final_prediction = 'HAZARDOUS' if prediction == 1 else 'NON-HAZARDOUS'

    return final_prediction
