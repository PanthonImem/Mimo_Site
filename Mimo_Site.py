import streamlit as st
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

def main():
    st.title("Welcome to the Mimo Site!")

    st.write('This is an amateur website for hosting my personal projects on analysis tools/visualization on players data of the videogame [Efootball](https://en.wikipedia.org/wiki/EFootball) series (also known as PES and Winning 11 previously).')

    st.write("This website is currently hosted (for free) on :blue[Streamlit Community Cloud] which is mostly for educational projects and on what is equivalent to a 1/16th\
     of a laptop which therefore cannot handle any real traffic. You are lucky to be seeing this page.\
     This website has :red[limited] functionality on mobile. Some features maybe unavailable. For your experience please use laptop.")
    
    st.write('I would like to hereby thank [PESDB](https://pesdb.net/efootball/) for the data behind this project. While not officially a data sponsor,\
     PESDB set their website up in a way that is very friendly for data enthusiasts to programmatically access their data and made this whole project possible. \
    Please visit [their website](https://pesdb.net/efootball/) and watch some ads if you have time.')

    st.write('Features of the site are available on the sidebar to the left. \
    Currently the following functionalities are available:')

    st.write('- Search Similar Player')
    st.write('- Suggest Skills to add to specific player')
    st.write('- List Players by Skill(s) Training')
    st.write('- 2D PCA Projection(Dimensionality Reduction) of Player Stats')
    st.write('- POTW Explorer')

    st.write("I will add more functionality to the site if it's useful.")
    st.write("Data is still manually updated by me so chill out. I need PESDB to update first before I can update.")
    st.write('For contact please DM me on [Reddit](https://www.reddit.com/user/Mimobrok).')

if __name__ == "__main__":
    main()