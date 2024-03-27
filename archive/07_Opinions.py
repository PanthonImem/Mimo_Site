import streamlit as st
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

import sys
sys.path.append("code")
from utility import hide_github



def main():
    st.title("Opinions on F2P Team-building")

    st.write('Standard Players worth Checking Out')
    st.write('- Saliba 93 CB')
    st.write('- Posch 89 RB(Equivalent to 96 CB)')
    st.write('- Barrios 92 DMF')

    hide_github()

if __name__ == "__main__":
    main()