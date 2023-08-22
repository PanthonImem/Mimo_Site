import pandas as pd
import numpy as np
import streamlit as st

import warnings
warnings.filterwarnings('ignore')


def main():
    st.set_page_config(layout="wide")
    st.title("POTW Pack Explorer")
    if 'df' not in st.session_state:
        st.session_state['df'] = pd.read_csv('data/mimo_dataset.csv')
    adf = st.session_state['df']

    st.write("Mimo Value Index is a made-up index for determining usefulness of a POTW player.")

    st.write("Overall Rating, How much of an upgrade from base, and Form are taken into account")

    potw_packs = [i for i in adf['pack'].unique() if 'POTW' in i]

    pdf = adf[adf.pack.isin(potw_packs)]
    bdf = adf[adf.pack=='base'][['Player Name','max_ovr_rating']].rename({'max_ovr_rating':'base_rating'}, axis = 1).drop_duplicates('Player Name')

    latest_pack = potw_packs[-1]

    pdf = pdf.merge(bdf, on = 'Player Name', how = 'left')
    pdf['base_rating'] = pdf['base_rating'].fillna(87)
    pdf['mimo_stat_value_index'] = np.clip(pdf['max_ovr_rating']-92, 0, 10)/10
    pdf['mimo_upgrade_value_index'] = 0.7+0.3*np.clip(pdf['max_ovr_rating']-pdf['base_rating'],0,3)/3

    pdf['mimo_form_value_index'] = 1
    pdf.loc[pdf.Form == 'Standard', 'mimo_form_value_index'] = 0.8
    pdf.loc[pdf.Form == 'Inconsistent', 'mimo_form_value_index'] = 0.5
    pdf['mimo_value_index'] = np.clip(pdf['mimo_upgrade_value_index']*pdf['mimo_stat_value_index']\
    *pdf['mimo_form_value_index']+0.1*pdf['s_Super-sub'],0.05,np.inf).round(2)

    gdf = pdf.groupby('pack').agg({'mimo_value_index':'mean'}).sort_values('mimo_value_index',ascending = False).round(3).reset_index()
    
    mmean = gdf['mimo_value_index'].mean().round(2)
    mstd = gdf['mimo_value_index'].std().round(2)
    
    pack = st.selectbox('Position Filter', potw_packs[::-1], index = 0)
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

    st.write(pdf[['pack','Player Name','max_ovr_rating','max_position','Playstyle','Form','mimo_value_index']]\
    .sort_values('mimo_value_index', ascending = False).reset_index(drop = True))

   
            
    

if __name__ == "__main__":
    main()