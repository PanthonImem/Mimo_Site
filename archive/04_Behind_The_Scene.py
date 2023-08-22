import streamlit as st
import pandas as pd
def main():
    
    st.title("Behind the Scene of Mimo Projects")
    st.write("I often get DMs asking about the technical details behind the scene of my projects. So in this part I'll list pointers/\
    resources to help you get started in case you are attempting a similar project.")
    
    st.header("Coding")
    st.write("To make a system of some sort you will need to have a coding skill.\
    Personally I use Python as I come from Data background but you can definitely useother programming language.\
    This Website is made using Streamlit. Streamlit is possibly the simplest\
    way for Python coders to make a website. The barebone of this website took ~30 minutes to get up and running.")

    st.header("Data Acquisition")
    st.write("Most of the data here are scraped from [PESDB](https://pesdb.net/pes2022/?mode=max_level&featured=0).\
    Web Scraping pretty much means extracting data from a website. \
    Make sure to add sleep to your scraping to not burden the site/get rate limited.")
    
if __name__ == "__main__":
    main()