import streamlit as st
import seaborn as sns

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')

def main():
    st.set_page_config(layout="wide")
    st.title("Efootball Players in 2D")
    st.write("The plot below is a PCA projection of player stats onto 2D -- closer players are more similar")
    if 'df' not in st.session_state:
        st.session_state['df'] = pd.read_csv('data/mimo_dataset.csv')
    adf = st.session_state['df']

    ps = np.sort(adf['Playstyle'].unique())
    colors = sns.color_palette("tab10",25)
    cdict = dict(zip(ps, colors))
    adf['color'] = [cdict[i] if i in ps else cdict['Unactivated'] for i in adf['Playstyle'].values]

    ovr = st.select_slider('Overall Filter', [92,93,94,95,96,97,98], value = 98)

    sc1, sc2 = st.columns((1,2))
    with sc1:
        pos = st.selectbox('Position Filter', ['All']+list((adf['Position'].unique())))
    with sc2:
        pack = st.selectbox('Highlight Pack', ['All']+list((adf['pack'].unique()))[::-1])
    #x_axis = st.selectbox('X axis', ['pca1','pca2','pca3'])
    #y_axis = st.selectbox('y axis', ['pca2','pca1','pca3'])

    x_axis = 'pca1'
    y_axis = 'pca2'
    with sc1:
        show_pack = st.checkbox('Show Pack in Label')
    with sc2:
        show_strongest = st.checkbox('Show Only Highest Ovr Version of each Player')
        
    
    ovr_col = 'max_ovr_rating' if pos == 'All' else 'or_'+pos
    fig = plt.figure(figsize = (15,12))

    df = adf[(adf[ovr_col]>=92)]
    if(show_strongest):
        df = df.sort_values(ovr_col, ascending = False).drop_duplicates('Player Name', keep = 'first')
    plt.scatter(df[x_axis], df[y_axis], s = 4, c = df['color'], alpha = 0.33)

    df = adf[(adf[ovr_col]>=ovr)|(df['pack']==pack)]
    if(show_strongest):
        df = df.sort_values(ovr_col, ascending = False).drop_duplicates('Player Name', keep = 'first')
    plt.scatter(df[x_axis], df[y_axis], s = 4, c = df['color'], alpha = 1)
    for i in range(df.shape[0]):
        extra_txt = '\n'+df['pack'].values[i][1:] if show_pack else ''
        if((df['pack'].values[i]==pack)):
            plt.text(df[x_axis].values[i], df[y_axis].values[i], str(df[ovr_col].values[i])+' '+df['Player Name'].values[i]+extra_txt, size = 8, alpha = 1, color = 'darkred', weight='bold')
        else:
            plt.text(df[x_axis].values[i], df[y_axis].values[i], str(df[ovr_col].values[i])+' '+df['Player Name'].values[i]+extra_txt, size = 8, alpha = 1)

    plt.axis('off')
    st.write(fig)

    
    



if __name__ == "__main__":
    main()