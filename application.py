# pip install streamlit
import random
import streamlit as st
import pandas as pd
from PIL import Image


df = pd.read_csv("toyota_cars.csv")
mapper = dict([(i, j) for i, j in zip(df.Model.unique(), range(len(df.Model.unique())))])

# STARTING APPLICATION INTERFACE
st.title("Get your Favourite Car")

with st.form("car_pic", clear_on_submit=False):
    models = df.Model.unique().tolist()
    models.insert(0, "Select Option")

    years = df.Year.unique().tolist()
    years.insert(0, "Select Option")

    make = st.selectbox("Make", ["Select Option", "Toyota"])
    model = st.selectbox("Model", models)
    year = st.selectbox("Model", years)

    submit = st.form_submit_button("Load Image")
    if submit:
        names = df[((df.Make == make) & (df.Model == model) & (df.Year == year))].name.to_list()
        if len(names)>0:
            name = random.choice(names)
            img = Image.open("dataset/"+name)
            img = img.resize((700, 400))
            st.image(image=img, caption="Car Image")
        else:
            st.subheader("SORRY! No Picture available")