import cv2
import streamlit as st
import numpy as np
from datetime import date
from streamlit_folium import folium_static
from PIL import Image, ImageEnhance
import pandas as pd
from st_aggrid import AgGrid
import folium

st.set_page_config(
   page_title="Image Editor",
   page_icon="./logo.png",
   layout="wide",
   initial_sidebar_state="expanded",
)

st.sidebar.title('Image Editor')
rad1 =st.sidebar.radio("Navigation",["Home","Profile", "About-Us"])

#Create two columns with different width
col1, col2 = st.columns( [0.8, 0.2])
with col1:               # To display the header text using css style
    st.markdown(""" <style> .font {
    font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Upload your photo here...</p>', unsafe_allow_html=True)


if rad1 == "Home":
    #Add a header and expander in side bar
    st.sidebar.markdown('<p class="font"> Image Editor </p>', unsafe_allow_html=True)
    with st.sidebar.expander("About the App"):
        st.write("""
            Use this simple app to convert your favorite photo to a pencil sketch, a grayscale image or an image with blurring effect.  \n  \nThis app was created by Sharone Li as a side project to learn Streamlit and computer vision. Hope you enjoy!
        """)

    #Add file uploader to allow users to upload photos
    uploaded_file = st.file_uploader("", type=['jpg','png','jpeg'])
    #Add 'before' and 'after' columns
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns( [0.5, 0.5])
        with col1:
            st.markdown('<p style="text-align: center;">Before</p>',unsafe_allow_html=True)
            st.image(image,width=300)  

        with col2:
            st.markdown('<p style="text-align: center;">After</p>',unsafe_allow_html=True)

        #Add conditional statements to take the user input values
        with col2:
            st.markdown('<p style="text-align: center;">After</p>',unsafe_allow_html=True)
            filter = st.sidebar.radio('Covert your photo to:', ['Original','Gray Image','Black and White', 'Pencil Sketch', 'Blur Effect'])
            if filter == 'Gray Image':
                    converted_img = np.array(image.convert('RGB'))
                    gray_scale = cv2.cvtColor(converted_img, cv2.COLOR_RGB2GRAY)
                    st.image(gray_scale, width=300)
            elif filter == 'Black and White':
                    converted_img = np.array(image.convert('RGB'))
                    gray_scale = cv2.cvtColor(converted_img, cv2.COLOR_RGB2GRAY)
                    slider = st.sidebar.slider('Adjust the intensity', 1, 255, 127, step=1)
                    (thresh, blackAndWhiteImage) = cv2.threshold(gray_scale, slider, 255, cv2.THRESH_BINARY)
                    st.image(blackAndWhiteImage, width=300)
            elif filter == 'Pencil Sketch':
                    converted_img = np.array(image.convert('RGB')) 
                    gray_scale = cv2.cvtColor(converted_img, cv2.COLOR_RGB2GRAY)
                    inv_gray = 255 - gray_scale
                    slider = st.sidebar.slider('Adjust the intensity', 25, 255, 125, step=2)
                    blur_image = cv2.GaussianBlur(inv_gray, (slider,slider), 0, 0)
                    sketch = cv2.divide(gray_scale, 255 - blur_image, scale=256)
                    st.image(sketch, width=300) 
            elif filter == 'Blur Effect':
                    converted_img = np.array(image.convert('RGB'))
                    slider = st.sidebar.slider('Adjust the intensity', 5, 81, 33, step=2)
                    converted_img = cv2.cvtColor(converted_img, cv2.COLOR_RGB2BGR)
                    blur_image = cv2.GaussianBlur(converted_img, (slider,slider), 0, 0)
                    st.image(blur_image, channels='BGR', width=300) 
            else: 
                    st.image(image, width=300)

if rad1 == "Profile":
    st.title("Your Profile")

    col1 , col2 = st.columns(2)

    rad2 =st.radio("Profile",["Sign-Up","Sign-In"])


    if rad2 == "Sign-Up":

        st.title("Registration Form")



        col1 , col2 = st.columns(2)

        fname = col1.text_input("First Name",value = "first name")

        lname = col2.text_input("Second Name")

        col3 , col4 = st.columns([3,1])

        email = col3.text_input("Email ID")

        phone = col4.text_input("Mob number")

        col5 ,col6 ,col7  = st.columns(3)

        username = col5.text_input("Username")

        password =col6.text_input("Password", type = "password")

        col7.text_input("Repeat Password" , type = "password")

        but1,but2,but3 = st.columns([1,4,1])

        agree  = but1.checkbox("I Agree")

        if but3.button("Submit"):
            if agree:  
                st.subheader("Additional Details")

                address = st.text_area("Tell Us Something About You")
                st.write(address)

                st.date_input("Enter your birth-date")

                v1 = st.radio("Gender",["Male","Female","Others"],index = 1)

                st.write(v1)

                st.slider("age",min_value = 18,max_value=60,value = 30,step = 2)

                img = st.file_uploader("Upload your profile picture")
                if img is not None:
                    st.image(img)

            else:
                st.warning("Please Check the T&C box")

    if rad2 == "Sign-In":
        col1 , col2 = st.columns(2)

        username = col1.text_input("Username")

        password =col2.text_input("Password", type = "password")

        but1,but2,but3 = st.columns([1,4,1])

        agree  = but1.checkbox("I Agree")

        if but3.button("Submit"):
            
            if agree:  
                st.subheader("Additional Details")

                address = st.text_area("Tell Us Something About You")
                st.write(address)

                st.date_input("Enter your birth-date")

                v1 = st.radio("Gender",["Male","Female","Others"],index = 1)

                st.write(v1)

                st.slider("age",min_value = 18,max_value=60,value = 30,step = 2)

                img = st.file_uploader("Upload your profile picture")
                if img is not None:
                    st.image(img)
            else:
                st.warning("Please Check the T&C box")

if rad1 == "About-Us": 
    st.title("Image Editor")

    st.subheader('Locate Us')
    m = folium.Map(location=[19.106790750000002, 72.8414303725908], zoom_start=16)

    # add marker for DJ Sanghvi College Of Engineering
    tooltip = "DJ Sanghvi College Of Engineering"
    folium.Marker(
        [19.106790750000002, 72.8414303725908], popup="DJ Sanghvi College Of Engineering", tooltip=tooltip
    ).add_to(m)

    # call to render Folium map in Streamlit
    folium_static(m)