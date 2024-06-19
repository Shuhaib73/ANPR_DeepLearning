# Importing necessary libraries and modules
import os
import sys 
import time
from datetime import datetime
import numpy as np
import ultralytics
from ultralytics import YOLO
import math
import cv2 as cv
import easyocr
from IPython.display import Image, display

# Importing Flask-related modules for web application development
from flask import Flask, render_template, redirect, request, url_for, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
import psycopg2

# Importing custom module or class for number plate detection/recognition
from detect_recog import NumberPlateDetector

# Creating a Flask application instance
app = Flask(__name__)

# Configuring Flask application settings, Secret key for session security 

app.config['SECRET_KEY'] = 'abcd1234'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:7862480@localhost:5432/anpr_db'

# Disabling permanent sessions (sessions expire when browser is closed) & Setting session type to store session data on the filesystem
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'

# Initializing Flask Session with configured settings
Session(app)

# Initialize an instance of SQLAlchemy with the flask application
db = SQLAlchemy(app) 


class AppData(db.Model):
    __tablename__ = 'anpr_data'

    # Table columns definition
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time_details = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    license_plate = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    confidence = db.Column(db.Float, nullable=True)
    file_name = db.Column(db.String, nullable=False)

    # Constructor method that initializes a AppData instance with attributes defined
    def __init__(self, license_plate, state, confidence, file_name):
        self.license_plate = license_plate
        self.state = state
        self.confidence = confidence
        self.file_name = file_name


# Create table, note: In flask, certain operation, like database interaction require an application context to be active
with app.app_context():
    db.create_all()


# Route decorator to map the URL '/' to the home() function
@app.route('/')
def home():
    try: 
        return render_template('base.html')
    except Exception as e:
        return f"An Error Occurred: {str(e)}"
        

@app.route('/Num_Detection_Page', methods=['GET', 'POST'])
def Num_Detection_Page():

    # Initialize variables for error and success messages, and country code
    error_message = None
    success_message = None
    country = ''

    # Dictionary mapping Indian state codes to state names
    indian_state_codes = {
    "AN": "Andaman & Nicobar Islands", "AP": "Andhra Pradesh", "AR": "Arunachal Pradesh", "AS": "Assam", "BR": "Bihar", "CH": "Chandigarh", "CG": "Chhattisgarh", "DD": "Daman & Diu", "DL": "Delhi", "DN": "Dadra & Nagar Haveli",  "GA": "Goa", "GJ": "Gujarat", "HP": "Himachal Pradesh", "HR": "Haryana", "JK": "Jammu & Kashmir", "JH": "Jharkhand", "KA": "Karnataka", "KL": "Kerala", "LA": "Ladakh", "LP": "Lakshadweep", "MH": "Maharashtra",
    "MN": "Manipur", "MP": "Madhya Pradesh", "MZ": "Mizoram", "NL": "Nagaland", "OR": "Odisha", "PB": "Punjab", "PY": "Puducherry",
    "RJ": "Rajasthan", "SK": "Sikkim", "TN": "Tamil Nadu", "TR": "Tripura", "TS": "Telangana", "UK": "Uttarakhand",
    "UP": "Uttar Pradesh", "WB": "West Bengal"
    }

    # handling GET and POST requests
    if request.method == 'GET':
        session.clear()
        return render_template('anpr_dash.html') 

    elif request.method == 'POST':

        if 'image' in request.files:
            try:
                image = request.files['image']
                timestamp = int(time.time())
                image_path = f"static/images/{timestamp}_{image.filename}"
                image.save(image_path)

                detected_plates = detector.detect_plate_img(image_path=image_path)

                if detected_plates:
                    for plate_num in detected_plates:
                        license_plate, conf = plate_num
                        conf = round(conf * 100, 5)
                        
                        if license_plate[:2] in indian_state_codes:
                            state_detected = indian_state_codes[license_plate[:2]]
                        
                            new_plate_data = AppData(license_plate=license_plate, state=state_detected, confidence=conf, file_name=image.filename)

                            db.session.add(new_plate_data)
                        else:
                            new_plate_data = AppData(license_plate=license_plate, state='International', confidence=conf, file_name=image.filename)

                            db.session.add(new_plate_data)

                    db.session.commit()
                    success_message = "License Plate Data Uploaded Successfully!"

                    session.clear()
                    return render_template('anpr_dash.html', success_message=success_message)
                else:
                    error_message = "No plates detected"
                    return render_template('anpr_dash.html', error_message=error_message)
                
            except Exception as e:
                print(f"Error: {e}")
                return render_template('anpr_dash.html', error_message=error_message)

        if 'video' in request.files:
            try:
                video = request.files['video']
                video_filename = video.filename
                video_path = os.path.join(r"static\videos", video_filename)
            
                # Save the video file
                video.save(video_path)

                country = request.form.get('country')
                country = country.lower()
                print(f"Selected country: {country}")

                detected_plates = detector.detect_plate_video(video_path=video_path, country=country)
     
                if detected_plates:
                    for plate_num in detected_plates:
                        license_plate, conf = plate_num
                        conf = round(conf * 100, 5)
                        if license_plate[:2] in indian_state_codes:
                            state_detected = indian_state_codes[license_plate[:2]]
                        
                            new_plate_data = AppData(license_plate=license_plate, state=state_detected, confidence=conf, file_name=video.filename)

                            db.session.add(new_plate_data)
                        else:
                            new_plate_data = AppData(license_plate=license_plate, state='International', confidence=conf, file_name=video.filename)

                            db.session.add(new_plate_data)

                    db.session.commit()
                    success_message = "License Plate Data Uploaded Successfully!"

                    return render_template('anpr_dash.html', success_message=success_message)
                else:
                    error_message = "No plates detected"
                    return render_template('anpr_dash.html', error_message=error_message)
                
        
            except Exception as e:
                print(f"Error: {e}")
                return render_template('anpr_dash.html', error_message=error_message)

            


if __name__ == "__main__":
    # Path to the pretrained model
    model_path = 'best.pt'

    # Initialize the NumberPlateDetector with the pretrained model path
    detector = NumberPlateDetector(model_path=model_path)

    # Run the Flask application
    app.run(debug=True)

