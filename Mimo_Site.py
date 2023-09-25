import streamlit as st
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

import sys
sys.path.append("code")
from utility import hide_github



def main():
    st.title("Welcome to the Mimo Site!")

    st.write('This is an amateur website for hosting my personal projects on analysis tools/visualization on players data of the videogame [Efootball](https://en.wikipedia.org/wiki/EFootball) series (also known as PES and Winning 11 previously).')

    st.write('Features of the site are available on the sidebar to the left. \
    Currently the following functionalities are available:')


    st.write('- [Player Analysis](https://mimo-site.streamlit.app/Player_Analysis)')
    st.write('- [Search Similar Player](https://mimo-site.streamlit.app/Similar_Player_Search)')
    st.write('- [Suggest Skills to add to specific player](https://mimo-site.streamlit.app/Player_Skill_Suggest)')
    st.write('- [List Players by Skill(s) Training](https://mimo-site.streamlit.app/List_Player_By_Skill_Training)')
    st.write('- [2D PCA Projection(Dimensionality Reduction) of Player Stats](https://mimo-site.streamlit.app/3D_PCA_Projection)')
    st.write('- [POTW Explorer](https://mimo-site.streamlit.app/POTW_Explorer)')
    
    st.write("This website is currently hosted (for free) on :blue[Streamlit Community Cloud].\
     This website has :red[limited] functionality on mobile. Some features maybe unavailable. For your experience please use laptop if possible.")
    
    st.subheader('Recent Changelog:')
    st.write('24/09/23 - Revamp Player ID/Name Input Function')
    st.write('24/09/23 - Monday data update')
    st.write('23/09/23 - Add Version Comparison section to Player Analysis Tool')
    st.write('22/09/23 - Add Player Analysis Tool v1')
    st.write('22/09/23 - Add a few legacy carryover IMs that were previously excluded because of wrong max level')
    st.write('21/09/23 - Thursday data update')
    st.write('19/09/23 - Add players to database. 1000+ Base players now available.')

    st.subheader('Data Note:')
    st.write("This website relies on [PESDB](https://pesdb.net/efootball/) for data. I need PESDB to update first before I can update.")

    st.write('I would like to hereby thank [PESDB](https://pesdb.net/efootball/) for the data behind this project. While not officially a data sponsor,\
     PESDB set their website up in a way that is very friendly for data enthusiasts to programmatically access their data and made this whole project possible. \
    Please visit [their website](https://pesdb.net/efootball/) and watch some ads if you have time.')

    st.write('For contact please DM me on [Reddit](https://www.reddit.com/user/Mimobrok).')
    hide_github()

if __name__ == "__main__":
    main()