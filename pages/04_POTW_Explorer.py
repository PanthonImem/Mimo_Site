import pandas as pd
import numpy as np
import streamlit as st

import warnings
warnings.filterwarnings('ignore')
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

@st.cache_data
def load_data():
	return pd.read_csv('data/mimo_dataset.csv')

def main():
    st.set_page_config(layout="wide")
    st.title("POTW Pack Explorer")

    adf = load_data()

    st.write('Powered by :violet[Mimo Value Index]')

    st.write(":violet[Mimo Value Index] is a made-up index for determining value of a POTW player. The calculation will be adjusted as I get more time to work on it.")

    st.write("Currently, Overall Rating, How much of an upgrade from base, Super-sub, and Form are taken into account")

    potw_packs = [i for i in adf['pack'].unique() if 'POTW' in i]

    pdf = adf[adf.pack.isin(potw_packs)]
    bdf = adf[adf.pack=='base'][['Player Name','max_ovr_rating']].rename({'max_ovr_rating':'base_rating'}, axis = 1).drop_duplicates('Player Name')

    latest_pack = potw_packs[-1]

    pdf = pdf.merge(bdf, on = 'Player Name', how = 'left')
    pdf['base_rating'] = pdf['base_rating'].fillna(87)
    pdf['mimo_stat_value_index'] = np.clip(pdf['max_ovr_rating']-92, 0, 10)
    pdf['mimo_upgrade_value_index'] = 0.7+0.3*np.clip(pdf['max_ovr_rating']-pdf['base_rating'],0,3)/3

    pdf['mimo_form_value_index'] = 1
    pdf.loc[pdf.Form == 'Standard', 'mimo_form_value_index'] = 0.8
    pdf.loc[pdf.Form == 'Inconsistent', 'mimo_form_value_index'] = 0.5
    pdf['mimo_value_index'] = np.clip(pdf['mimo_upgrade_value_index']*pdf['mimo_stat_value_index']\
    *pdf['mimo_form_value_index']+1*pdf['s_Super-sub'],0.5,np.inf).round(1)

    gdf = pdf.groupby('pack').agg({'mimo_value_index':'mean'}).sort_values('mimo_value_index',ascending = False).round(2).reset_index()
    
    mmean = gdf['mimo_value_index'].mean().round(2)
    mstd = gdf['mimo_value_index'].std().round(2)
    
    pack = st.selectbox('POTW Pack Filter', potw_packs[::-1], index = 0)
    df = pdf[pdf.pack == pack][['pack','Player Name','max_ovr_rating','max_position','Playstyle','Form','mimo_value_index']]\
    .sort_values('mimo_value_index', ascending = False).reset_index(drop = True)

    pack_val = df['mimo_value_index'].mean().round(2)
    pack_val_n = (pack_val-mmean)/mstd

    if pack_val_n >= 1.29:
        ttext = ":blue[Great]"
    elif pack_val_n >= 0.68:
        ttext = ":green[Good]"
    elif pack_val_n >= -0.68:
        ttext = ":violet[Average]"
    elif pack_val_n >= -1.29:
        ttext = ":orange[Weak]"
    else:
        ttext = ":red[Very Weak]"

    sc1, sc2 = st.columns((1,2))
    with sc1:
        st.write(gdf)
    with sc2:
        st.write("At Mimo Value Index of {}, {} is {} as a POTW pack".format(pack_val, pack, ttext))
        st.write(df)


    #sc1, sc2 = st.columns((1,2))
    st.write('Best POTW Players by Position')
    #with sc1:
    pos = st.selectbox('Position Filter', list((adf['Position'].unique())))
    #with sc2:
    activated = st.checkbox('Show Only Players with Activated Playstyle')

    flag_playstyle = True
    if activated:
        flag_playstyle = ~pdf['Playstyle'].isin(get_unactivated(pos))
    df = pdf[(pdf['Possible Positions'].str.contains(pos))&(flag_playstyle)]

    df['mimo_value_index_'+pos] = np.clip(np.clip(df['or_'+pos]-92, 0, 10)
    *df['mimo_form_value_index']+1*df['s_Super-sub'],0.5,np.inf).round(1)
    st.write(df[['pack','Player Name','or_'+pos,'max_ovr_rating','max_position','Playstyle','Form','mimo_value_index_'+pos]]\
    .sort_values('mimo_value_index_'+pos, ascending = False).reset_index(drop = True))

   
if __name__ == "__main__":
    main()