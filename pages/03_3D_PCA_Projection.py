import streamlit as st
import seaborn as sns

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import plotly.express as px

import warnings
warnings.filterwarnings('ignore')

@st.cache_data
def load_data():
	return pd.read_csv('data/mimo_dataset.csv')

activate_dict = {
    'Goal Poacher': ['CF'],
    'Fox in the Box': ['CF'],
    'Roaming Flank': ['RWF','LWF','RMF','LMF'],
    'Creative Playmaker':['SS','RWF','LWF','AMF','RMF','LMF'],
    'Deep-Lying Forward':['CF','SS'], 
    'Orchestrator':['CMF','DMF'], 
    'Prolific Winger':['RWF','LWF'],
    'Full-back Finisher':['RB','LB'], 
    'Defensive Goalkeeper':['GK'], 
    'Offensive Goalkeeper':['GK'], 
    'The Destroyer':['CMF','DMF','CB'], 
    'Build Up':['CB'],
    'Box-to-Box':['RMF','LMF','CMF','DMF'],
    'Anchor Man':['DMF'], 
    'Cross Specialist':['RWF','LWF','RMF','LMF'], 
    'Hole Player':['SS','AMF','RMF','LMF','CMF'],
    'Offensive Full-back':['RB','LB'], 
    'Dummy Runner':['CF','SS','AMF'],
    'Fox in the Box':['CF'],
    'Extra Frontman':['CB'], 
    'Target Man':['CF'], 
    'Classic No. 10':['SS','AMF','CMF'],
    'Defensive Full-back':['RB','LB'], 
    '---':[],
}
def get_unactivated(pos):
    ls = []
    for key,value in activate_dict.items():
        if(pos not in value):
            ls.append(key)
    return ls

def main():

    if 'show_graph' not in st.session_state:
        st.session_state['show_graph'] = False

    st.set_page_config(layout="wide")

    st.title("The World of Efootball Players")
    st.write("The plot below is a PCA projection of player stats onto 3D -- closer players are more similar")


    adf = load_data()    
    adf = adf[adf['max_ovr_rating']>=92]

    sc1, sc2 = st.columns((1,2))
    with sc1:
        pos = st.selectbox('Position Filter', ['All']+list((adf['Position'].unique())))
    with sc2:
        color_by = st.selectbox('Color by', ['Playstyle','Position2'], index = 1)
        
    with sc1:
        label_off = st.checkbox('Turn Off Text Label')
        show_strongest = st.checkbox('Show Only Highest Ovr Version of each Player', value = True)
        

    with sc2:
        ovr = st.select_slider('Overall Filter', [93,94,95,96,97,98], value = 96)

    #sc1, sc2 = st.columns((1,5))
    with sc1:
        name_filter = st.selectbox('Filter Different Versions of Player', [''] + list(adf['Player Name'].unique()),\
         disabled=show_strongest, help = "Uncheck Show Highest Ovr to enable this mode")
        
    #pack = st.selectbox('Highlight Pack', ['']+list((adf['pack'].unique()))[::-1])
    pack = 'None'
    ovr_col = 'max_ovr_rating' if pos == 'All' else 'or_'+pos
        
    df = adf[(adf[ovr_col]>=ovr)]
    if name_filter != '':
        df = df[df['Player Name']==name_filter]

    if pos!='All':
        df.loc[df['Playstyle'].isin(get_unactivated(pos)), 'Playstyle'] = 'Inactivated'


    if show_strongest:
        df = df.sort_values(ovr_col, ascending = False).drop_duplicates('Player Name', keep = 'first')
    
    df['Overall Rating2'] = np.clip(df['Overall Rating']-90, 1, 10)

    st.caption("The plot is hidden by default to save resource. Click the button below to generate the plot.")
    click = st.button('Generate Plot', type = 'primary')
    if click:
        st.session_state['show_graph'] = True
    if st.session_state['show_graph']:
        fig = px.scatter_3d(df, x="pca1", y="pca2", z="pca3", hover_data = ['Player Name','pack','Overall Rating','Playstyle','Position'],
                    width=1200, height=800, color = color_by,  
                    size = 'Overall Rating2', text = 'Player Name' if name_filter=='' else 'pack' if not label_off else None, hover_name = 'pack')
        st.plotly_chart(fig)
        


        
        



if __name__ == "__main__":
    main()