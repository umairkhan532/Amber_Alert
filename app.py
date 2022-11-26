# Libraries imported
import os
import random
import streamlit as st
import pandas as pd
from PIL import Image
import requests
from pushnotifier import PushNotifier as pn

# Importing style sheet for designing
with open('style.css')as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Using pandas to cut down the data
df = pd.read_csv("toyota_cars.csv")
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
        with col2:
            suspect = st.text_input("Name of Suspect")
            make = st.text_input("Make of the Car involved in incident")
            model = st.text_input("Model of the Car invloved in incident")
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
        pn = pn.PushNotifier(username='umairkhan532', password='Mustanggtr#18', package_name='com.amberalert101.app',
                             api_key='E5MA6D4DD6C3VBV46V75B6C3VB5MA6E5MA6EMTTKFB')

        pn.login('Mustanggtr#18')

        # Victim Image
        if pic:
            p = "Victim_pictures/" + pic.name
            pn.send_image(p, devices=['BLWo', '9QKz'])
        else:
            pn.send_text("No Victim Image")

        pn.send_url('https://www.thecarconnection.com/',
                    silent=False, devices=['BLWo', '9QKz'])

        # Retrieving image from the dataset
        names = df[((df.Make == make) & (df.Model == model)
                    & (df.Year == year))].name.to_list()
        if len(names) > 0:
            name = random.choice(names)
            img = Image.open("dataset/"+name)
            img2 = img.resize((700, 400))
            with col2:
                st.image(image=img2)
            c = img.filename

            # Sending notification of car image
            pn.send_image(c, devices=['BLWo', '9QKz'])  # Car Image
        else:
            with col2:
                st.markdown("Car Image not found")
                pn.send_text("No car image")

        # Sending amber alert to phone
        pn.send_text("Amber Alert\n" + option + ". " + location + "\n" + "Victim: " + user_name + " " + age + " " +
                     description + " " + "\nSuspect: " + suspect + " " + "\nVehicle: " + make + " " + model + " " + str(year))

        with col1:
            st.markdown(
                "<h5 style='font-weight: bold'>Amber Alert</h5>", unsafe_allow_html=True)
            st.write(f"{option}. {location}")
            st.write(f"Victim: {user_name}, {age}, {description}")
            st.write(f"Suspect: {suspect}")
            st.write(f"Vehicle: {make} {model} {year}")
            st.write(
                "Link to Image Source\n[Link](https://www.thecarconnection.com/)")

        if pic is not None:
            with col3:
                st.image(image=pic)
        else:
            with col3:
                st.markdown("Victim image not available")
