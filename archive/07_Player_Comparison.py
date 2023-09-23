import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
from unidecode import unidecode
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')



@st.cache_data
def load_data():
	return pd.read_csv('data/mimo_dataset.csv')

def main():
    st.set_page_config(layout="wide")
    st.title("Player Comparison")
    adf = load_data()
    adf['Player ID'] = adf['Player ID'].astype(str)
    adf['Player Name_dcd'] = adf.apply(lambda row: unidecode(row['Player Name'].lower()), axis = 1)

    adf['Name-Pack'] = adf['Player Name'] + ' - ' + adf['pack']

    col1, col2 = st.columns(2)
    playerls = col1.multiselect("Enter Player:", adf['Name-Pack'].unique(), default = None)
    pos = col2.selectbox("Enter Position:", adf['Position'].unique())

    id_dict = adf[['Name-Pack','Player ID']].set_index('Name-Pack').to_dict()['Player ID']
    if len(playerls)>0 and pos:
        
        pidls = [id_dict[i] for i in playerls]

        colors = sns.color_palette("tab10",10)

        pdf = adf[adf['Player ID'] == pidls[0]]
        bdf = adf[(adf['or_'+pos]>=89)&(adf['Possible Positions'].str.contains(pos))]

        def plot_kde(col):
            sns.displot(bdf[col], kind = 'kde', height = 2, aspect = 2, color = 'darkgrey')
            plt.title(col)
            ax = plt.gca()
            fig = plt.gcf()
            ylim = ax.get_ylim()
            xlim = bdf[col].quantile(0.01)
            for i,pid_i in enumerate(pidls):
                tdf = adf[(adf['Player ID']==pid_i)]
                plt.plot([tdf[col].values[0],tdf[col].values[0]], [0, 1], linestyle = '--', color = colors[i])
                plt.text(tdf[col].values[0]+0.25, ylim[1]-(ylim[1]/(len(pidls)+1))*(i), tdf['Player Name'].values[0], size = 6, color = colors[i])
                plt.text(tdf[col].values[0]+0.25, ylim[1]-(ylim[1]/(len(pidls)+1))*(i)-0.01, tdf['pack'].values[0], size = 4, color = colors[i])
            plt.ylabel('')
            plt.xlabel('')
            plt.yticks([], [])
            plt.xlim(xlim, 100)
            plt.ylim(0, ylim[1]+0.02)
            return fig

        
        col1, col2, col3 = st.columns(3)
        with col1:

            col = "Offensive Awareness"
            with st.expander(col+' - :blue['+str(pdf[col].values[0])+']'):
                st.pyplot(plot_kde(col))
            
            
        
        


if __name__ == "__main__":
    main()