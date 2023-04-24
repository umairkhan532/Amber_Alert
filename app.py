# Libraries imported
import os
import random
import streamlit as st
import pandas as pd
from PIL import Image
from pushnotifier import PushNotifier as pn
import cv2
import os
from collections import Counter

#Register login
import pyrebase 
from datetime import datetime

# Register and Login for Officer

firebaseConfig = {
  'apiKey': "AIzaSyCbJ8mFSQTYhp6doRBLtUnJmPyO_6j3Kuc",
  'authDomain': "amber-alert-d16f9.firebaseapp.com",
  'projectId': "amber-alert-d16f9",
  'databaseURL':"https://amber-alert-d16f9-default-rtdb.firebaseio.com/",
  'storageBucket': "amber-alert-d16f9.appspot.com",
  'messagingSenderId': "198316058682",
  'appId': "1:198316058682:web:0d7196643cfa54338bad03",
  'measurementId': "G-NGYLYPFVPF"
}


#Firebase Authentication 

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

#Database 
db = firebase.database()
storage = firebase.storage()


image1 = Image.open('Amber_Alert.png')
image1 = image1.resize((391, 204))
st.sidebar.image(image1)

st.sidebar.title("Amber Alert")

choice = st.sidebar.selectbox('login/Signup', ['Login', 'Sign up'])
email = st.sidebar.text_input('Enter email')
batchid = st.sidebar.text_input('Enter batchid')
password = st.sidebar.text_input('Enter password', type = 'password')


if choice == 'Sign up':
    handle = st.sidebar.text_input('Please enter your name', value ='Default')
    submit = st.sidebar.button('Create my account')

    if submit: 
        user = auth.create_user_with_email_and_password(email,password)
        st.success('Your account is created successfully!')

        #Sign in 
        user = auth.sign_in_with_email_and_password(email,password)
        db.child(user['localId']).child("Handle").set(handle)
        db.child(user['localId']).child("ID").set(user['localId'])
        st.title('Welcome ' + handle)
        st.info('Login from the options')

if choice == 'Login':
    login = st.sidebar.checkbox('Login')
    
    if login: 
        user = auth.sign_in_with_email_and_password(email,password)

        signout = st.sidebar.button('Signout')
        if signout: 
            exit
        else:
         if user:
            # Importing style sheet for designing
            with open('style.css')as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

            # Using pandas to cut down the data
            df = pd.read_csv("all_cars.csv")
            mapper = dict([(i, j) for i, j in zip(
                df.Model.unique(), range(len(df.Model.unique())))])

            # STARTING APPLICATION INTERFACE
            st.markdown("<h1 style='text-align: center; color: #BA0000;text-shadow:2px 2px 10px white'>Report for Amber Alert</h1>", unsafe_allow_html=True)

            page_bg_img = """
            <style> 
            [data-testid="stAppViewContainer"]{
            background-image: url("https://cv4a.org/wp-content/uploads/2022/08/Purple-Heart-Day-1423x800.jpg");
            background-size: cover; 
            background-color: transparent;
            }
            </style>
            """
            st.markdown(page_bg_img, unsafe_allow_html=True)

            image1 = Image.open('Amber_Alert.png')
            image1 = image1.resize((587, 306))
            st.image(image1)

            # Report for the police officer
            col1, col2 = st.columns(2)

            with st.form("car_pic", clear_on_submit=False):

                with col1:
                    option = st.selectbox(
                        'Incident occured?',
                        ('Select from the below incidents', 'Child Abduction', 'Missing Child', 'Car Stolen'))
                    user_name = st.text_input("Name of Victim")
                    age = st.text_input("Victim age")
                    description = st.text_input("Description of Victim")
                    location = st.text_input("Location of incident")
                    suspect = st.text_input("Name of Suspect")
                    with col2:
                        suspect_description = st.text_input("Suspect Description")
                        make = st.text_input("Make of the Car involved in incident")
                        model = st.text_input("Model of the Car invloved in incident")
                        color2 = st.text_input("Color of the car")
                        year = st.number_input(
                            "Make Year of the Car", min_value=1900, max_value=2200)
                        pic = st.file_uploader(
                            "Upload the image of the Victim", type=['png', 'jpg'], )

                # Output

                submit = st.form_submit_button("Load Report")
                if submit:
                    st.markdown("<h3 style='text-align: center  ; color: black; background-color: rgba(0,0,0,.8); color: #fff;border-radius: 10px 10px 0px 0px; border-bottom: 1px solid white;'>   ⚠︎ EMERGENCY ALERTS</h3>", unsafe_allow_html=True)
                    col1, col2, col3 = st.columns(3)

                    # Used PushNotifier for sending notifications to phone
                    pn = pn.PushNotifier(username='mohammedkhan', password='AmberAlert123', package_name='com.amberalert.app',
                                        api_key='B5OH6575BD4DDV2VB6C3VEV46BV46575BBBTTFFBKF')

                    pn.login('AmberAlert123')       

                    # Victim Image
                    if pic:
                        p = "Victim_pictures/" + pic.name
                        pn.send_image(p, devices=['oQ3X'])
                    else:
                        pn.send_text("No Victim Image")

                    pn.send_url('https://www.thecarconnection.com/',
                                silent=False, devices=['oQ3X'])

                    # Retrieving image from the dataset
                    names = df[((df.Make == make) & (df.Model == model)
                                & (df.Year == year))].name.to_list()
                    
                    images_folder = "dataset/"
                    
                    if len(names) > 0:
                        name = random.choice(names)
                        img = Image.open("dataset/"+name)
                        img2 = img.resize((700, 400))

                        # Define the color thresholds for the car colors you want to search for
                        color_thresholds = {
                            "red": ((0, 70, 50), (10, 255, 255)),
                            "blue": ((100, 50, 50), (140, 255, 255)),
                            "gray": ((0, 0, 150), (180, 35, 200)),
                            "white": ((0, 0, 200), (180, 30, 255)),
                            "black": ((0, 0, 0), (180, 255, 50)),
                            "green": ((36, 25, 25),(70, 255, 255)), 
                            "silver": ((0, 0, 50),(180, 50, 220)), 
                            "yellow": ((20, 25, 25),(36, 255, 255))
                        }

                            
                        # Loop through all the files in the images folder
                     
                        for filename1 in os.listdir(images_folder):
                            # Check if the file is an image file
                            if filename1.endswith(".jpg") or filename1.endswith(".png"):
                                # Load the image
                             if filename1 in names:
                                image = cv2.imread(os.path.join(images_folder, filename1))
                                # Convert the image to HSV color space
                                hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                                # Initialize a dictionary to store the counts of each color
                                color_counts = {color: 0 for color in color_thresholds.keys()}
                                # Loop through the color thresholds and detect cars of that color
                                for color, thresholds in color_thresholds.items():
                                    mask = cv2.inRange(hsv, *thresholds)
                                    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                                    for contour in contours:
                                        # Draw a bounding box around the car
                                        x, y, w, h = cv2.boundingRect(contour)
                                        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                        # Increment the count for the detected color
                                        color_counts[color] += 1
                                # Find the most common color
                                most_common_color = max(color_counts, key=color_counts.get)
                                # Print the most common color and the counts of all colors
                                print(f"Most common color in {filename1}: {most_common_color}")
                                # Show the image with the detected cars
                                if most_common_color == color2:      
                                    img = Image.open("dataset/"+filename1)
                                   
                                    img2 = img.resize((700, 400))
                                
                        #name = random.choice(names)
                        
                        with col2:
                            st.image(image=img2)
                        c = img.filename

                        # Sending notification of car image
                        pn.send_image(c, devices=['oQ3X'])  # Car Image
                    else:
                        with col2:
                            st.markdown("Car Image not found")
                            pn.send_text("No car image")

                    # Sending amber alert to phone
                    pn.send_text("Amber Alert\n" + option + ". " + location + "\n" + "Victim: " + user_name + " " + age + " " +
                                description + " " + "\nSuspect: " + suspect + " " + "\nSuspect Description: " + suspect_description + " " + "\nVehicle: " + make + " " + model + " " + color2 + " " + str(year) )

                    with col1:
                        st.markdown(
                            "<h5 style='font-weight: bold'>Amber Alert</h5>", unsafe_allow_html=True)
                        st.write(f"{option}. {location}")
                        st.write(f"Victim: {user_name}, {age}, {description}")
                        st.write(f"Suspect: {suspect} {suspect_description}")
                        st.write(f"Vehicle: {make} {model} {color2} {year}")
                        st.write(
                            "Link to Image Source\n[Link](https://www.thecarconnection.com/)")

                    if pic is not None:
                        with col3:
                            st.image(image=pic)
                    else:
                        with col3:
                            st.markdown("Victim image not available")
