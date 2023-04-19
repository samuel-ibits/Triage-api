import os 
from flask_cors import CORS
from flask import Flask,jsonify, request
import  json
# import numpy as np
import pickle as p
import joblib
import traceback
import pandas as pd
from sklearn.tree import DecisionTreeClassifier 
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
# from pytime 
import time


app = Flask(__name__)
CORS(app)

@app.route('/rank', methods=['GET'])
def rank():
    
    ds = joblib.load("model/model.pkl") # Load "model.pkl"
    print ('Model loaded')
    data= joblib.load("data/data.pkl") # Load "model_columns.pkl"
    print ('Model columns loaded')
    # Create a lookup table to map each symptom to a unique integer/category
    symptom_dict = {
        'Chest Pain': 1,
        'Headache': 2,
        'Stomach Pain': 3,
        'Back Pain': 4,
        'Toothache': 5,
        'Nausea': 6,
        'Flu': 7,
        'Dizziness': 8,
        'Shortness of breath': 9,
        'Fatigue': 10,
        'Ankle Pain': 11,
        'Leg Pain': 12,
        'Cough': 13,
        'Sneezing': 14,
        'Fever': 15,
        'Sore throat': 16,
        'Abdominal pain': 17,
        'Muscle pain': 18,
        'Head injury with unconsciousness': 19,
        'Sprained ankle': 20,
        'Laceration on hand': 21,
        'Vehicle accident with broken bones': 22,
        'Vehicle accident with internal bleeding': 23,
        'Vehicle accident with head injury': 24,
        'Vehicle accident with spinal injury': 25,
        'Vehicle accident with internal injuries': 26,
        'Vehicle accident with multiple injuries': 27,
        'Seizure': 28,
        'High fever': 29,
        'Blurred vision': 30,
        'Nausea and vomiting': 31,
        'Muscle weakness': 32,
        'Loss of appetite': 33,
        'Rash': 34,
        'Joint pain': 35,
        'Night sweats': 36,
        'Body aches': 37,
        'Malaria symptoms': 38,
        'Diarrhea': 39,
        'Fractured limb': 40,
        'Tuberculosis': 41,
        'Respiratory illness': 42,
        'Malnutrition': 43,
        'Dengue Fever': 44,
        'Cholera': 45,
        'Maternal care': 46,
        'Ear Pain': 47,
        'Vomiting': 48,
        'Limp': 49,
        'Breathing Difficulty': 50,
        'Runny Nose': 51,
        'Red Eye': 52,
        'Dizziness and weakness': 53,
        'Falls with multiple injuries': 54,
        'Severe abdominal pain': 55,
        'Chest tightness and shortness of breath': 56,
        'Fainting': 57,
        'Extreme fatigue and muscle weakness': 58,
        'Swelling in the legs and feet': 59,
        'Difficulty speaking and difficulty moving': 60,
        'Constipation and abdominal pain': 61,
        'Numbness in one hand and facial droop': 62,
        'Severe headache and blurred vision': 63,
        'Pain in the lower back and leg': 64,
        'Confusion and disorientation': 65,
        'Difficulty walking and joint pain': 66,
        'Arm Pain': 67,
        'Foot Pain': 68,
        'Wrist Pain': 69,
        'Elbow Pain': 70,
        'Shoulder Pain': 71,
        'Hip Pain': 72,
        'Knee Pain': 73,
        'Groin Pain': 74,
        'Neck Pain': 75,
        'Weak Pulse': 76,
        'Unconsciousness': 77,
        'Seizures': 78,
    'Severe headache': 79,
    'Paralysis': 80,
    'Heavy bleeding': 81,
    'Loss of vision': 82,
    'Loss of speech': 83,
    'Severe burns': 84,
    'Choking': 85,
    'Cardiac arrest': 86,
    'Coma': 87,
    'Severe back pain': 88,
    'Loss of feeling in limbs': 89,
    'Unconscious': 90,
    'Difficult Speech': 91,
    'Head injury': 92,
    'Rapid Heartbeat': 93,
    'Unresponsive': 94,
    'Convulsions': 95,
    'Dehydration': 96,
    'Uncontrolled movements': 97,
    'Acute Pain': 98,
    'Loss of Consciousness': 99,
    'Hypertension': 100
    }

    data.dropna(inplace=True)
    # Extract hour and minute values from Arrival Time column
    data['Hour'] = pd.to_datetime(data['Arrival Time']).dt.hour
    data['Minute'] = pd.to_datetime(data['Arrival Time']).dt.minute
    # Drop original Arrival Time column
    data.drop('Arrival Time', axis=1, inplace=True)
        # Encoding the Primary-Symptom column using the lookup table
    data['Encoded-Symptom'] = data['Primary-Symptom'].fillna(101).map(symptom_dict)

    # Replace NaN values with 101 in the Encoded-Symptom column
    data['Encoded-Symptom'].fillna(value=101, inplace=True)

    # Drop original Arrival Time column
    data.drop('Primary-Symptom', axis=1, inplace=True)
    # Split the Vital Signs column into two separate columns
    data[['BP_Systolic', 'BP_Diastolic']] = data['Vital Signs'].str.split('/', expand=True)
    data['BP_Systolic'] = data['BP_Systolic'].str.replace('BP:', '')

    # Rename the new columns
    data.rename(columns={'BP_Systolic': 'Systolic BP', 'BP_Diastolic': 'Diastolic BP'}, inplace=True)

    # Drop the original Vital Signs column
    data.drop(['Vital Signs'], axis=1, inplace=True)
    ## Replace empty strings with False
    data['Medical History'] = data['Medical History'].replace('', False)

    # Replace 'None' with False
    data['Medical History'] = data['Medical History'].replace('None', False)

    # Replace all other values with True
    data['Medical History'] = data['Medical History'].apply(lambda x: True if x else x)

    data.drop('Level of Urgency', axis=1, inplace=True)



    prediction = list(ds.predict(data))

    return jsonify({"Message":"Ranked succesfully",
                   'Data': prediction})


@app.route('/search', methods=['GET'])
def search():
    patient = request.args.get('patient')
    
    return jsonify({'Error': 'not working properly yet'})
      
  

@app.route('/uploadpatients', methods=['POST'])
def uploadPatients():
    uploaded_file = request.files['file']
    filename = uploaded_file.filename
    file_path = os.path.join('data', filename)
    timestamp = str(int(time.time()))
    df=pd.read_csv(uploaded_file)


    if os.path.exists('model/model.pkl'):
        # generate a new filename by appending a timestamp
        new_filename2 = f"{os.path.splitext(filename)[0]}_{timestamp}{os.path.splitext(filename)[1]}"
        new_filename = f"{os.path.splitext('data.pkl')[0]}{os.path.splitext('data.pkl')[1]}"

        response= df.to_pickle('data/'+ new_filename)
        response2= df.to_pickle('data/'+ new_filename2)
    else:

        new_filename = f"{os.path.splitext('data.pkl')[0]}{os.path.splitext('data.pkl')[1]}"

        response= df.to_pickle( 'data/'+new_filename)
    
    if response != 'null':
          return jsonify({
            "Message": "uploaded sucesefully!",
            # Add this option to distinct the POST request
            "METHOD": "POST",
            "Data":df.to_json()

        })
    else:
          return jsonify({
            "ERROR": "not uploaded"
        })

@app.route('/uploadmodel', methods=['POST'])
def upload_model():
    uploaded_file = request.files['file']
    filename = uploaded_file.filename
    file_path = os.path.join('model', filename)
    timestamp = str(int(time.time()))
      
    if os.path.exists('model/model.pkl'):
        # generate a new filename by appending a timestamp
        new_filename2 = f"{os.path.splitext(filename)[0]}_{timestamp}{os.path.splitext(filename)[1]}"
        new_filename = f"{os.path.splitext('model.pkl')[0]}{os.path.splitext('model.pkl')[1]}"

        response= uploaded_file.save('model/'+ new_filename)
        response2= uploaded_file.save('model/'+ new_filename2)
    else:

        new_filename = f"{os.path.splitext('model.pkl')[0]}{os.path.splitext('model.pkl')[1]}"

        response= uploaded_file.save( 'model/'+new_filename)
    
    if response != 'null':
          return jsonify({
            "Message": "uploaded sucesefully!",
            # Add this option to distinct the POST request
            "METHOD": "POST"
        })
    else:
          return jsonify({
            "ERROR": "not uploaded"
        })


@app.route('/')
def index():
    # A welcome message to test our server
    return "<h1>Welcome To TRIAGE API!</h1>"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    
    
    port = 5000
    # If you don't provide any port the port will be set to 12345
    app.run(threaded=True,port=port, debug= True)
