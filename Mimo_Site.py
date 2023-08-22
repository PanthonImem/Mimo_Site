import streamlit as st
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

def main():
    if 'df' not in st.session_state:
        st.session_state['df'] = pd.read_csv('data/mimo_dataset.csv')
    adf = st.session_state['df']
    
    st.title("Welcome to the Mimo Site!")

    st.write('This is an amateur website for hosting my personal projects on analysis tools/visualization on players data of the videogame Efootball series.')

    st.write("I am not a professional web developer so sorry if this website loads slowly or breaks sometimes/frequently.\
    This is currently hosted(for free) on Streamlit Cloud which is mostly for educational projects so it cannot handle any real traffic.")

    st.write('Features of the site are available on the sidebar to the left. \
    Currently the following functionalities are available:')

    
    st.write('- Suggest Skills to add to specific player')
    st.write('- List Players by Skill(s)')
    st.write('- 2D PCA Projection(Dimensionality Reduction) of Player Stats')

    st.write("I will add more functionality to the site if it's useful.")
    st.write('For contact please DM me on [Reddit](https://www.reddit.com/user/Mimobrok).')


if __name__ == "__main__":
    main()