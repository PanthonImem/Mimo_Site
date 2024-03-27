
import pandas as pd
import numpy as np
import streamlit as st
from unidecode import unidecode
import pickle
import sklearn
import warnings
warnings.filterwarnings('ignore')

import sys
sys.path.append("../code")
from utility import hide_github


common_picks = [88029649700314, 88029649706260, 88029649833402]

sset = ['Acrobatic Clear',
 'Acrobatic Finishing',
 'Aerial Superiority',
 'Blocker',
 'Captaincy',
 'Chip Shot Control',
 'Chop Turn',
 'Cut Behind &; Turn',
 'Dipping Shot',
 'Double Touch',
 'Fighting Spirit',
 'First-time Shot',
 'Flip Flap',
 'GK High Punt',
 'GK Long Throw',
 'GK Low Punt',
 'GK Penalty Saver',
 'Gamesmanship',
 'Heading',
 'Heel Trick',
 'Interception',
 'Knuckle Shot',
 'Long Range Shooting',
 'Long-Range Curler',
 'Low Lofted Pass',
 'Man Marking',
 'Marseille Turn',
 'No Look Pass',
 'One-touch Pass',
 'Outside Curler',
 'Penalty Specialist',
 'Pinpoint Crossing',
 'Rabona',
 'Rising Shot',
 'Scissors Feint',
 'Scotch Move',
 'Sliding Tackle',
 'Sole Control',
 'Sombrero',
 'Super-sub',
 'Through Passing',
 'Track Back',
 'Weighted Pass']

def find_top_skills(pdf):
    for skill in sset:
        pdf['pred_'+skill] *= (pdf['s_'+skill]==0)
    pred_cols = [i for i in pdf.columns if 'pred_' in i]
    top_n = np.argsort(pdf[pred_cols])[0][::-1]
    top_score = np.sort(pdf[pred_cols])[0][::-1]
    sdf = pd.DataFrame(list(zip([i.lstrip('pred_') for i in np.array(pred_cols)[top_n]],top_score)), \
    columns = ['Suggested Skill','Mimo Skill Fit Score'])
    return sdf[sdf['Mimo Skill Fit Score']>=10]

@st.cache_data
def load_data():
	return pd.read_csv('data/new_mimo_dataset.csv')

def main():
    st.set_page_config(layout="wide")
    hide_github()
    st.title("Mimo Skill Suggest")
    st.write('Powered by :orange[Mimo Skill Fit Score]')
    adf = load_data()
    adf['Player ID'] = adf['Player ID'].astype(str)
    adf['Player Name_dcd'] = adf.apply(lambda row: unidecode(row['Player Name'].lower()), axis = 1)
    with open('data/skill_suggest_dict.pkl', 'rb') as file:
        sdict = pickle.load(file)

    st.write('Enter Player ID to obtain Skill Suggestion.')
    st.caption("Mimo Skill Fit Score goes between 0 to 100. Higher means the model thinks the player should have this skill based on stats.")
    st.caption("Generally, >70 is very nice to add, 30-70 is nice to have but not essential")

    #Player Search Snippet
    col1, col2 = st.columns(2)
    pack = col1.selectbox('Recent Packs', adf['pack'].unique()[-10:][::-1])
    if pack:
        with st.expander(':violet[{}]'.format(pack)):
            st.write(adf[adf.pack == pack][['Player ID','Overall Rating','Player Name','Position','pack']]\
            .sort_values('Overall Rating', ascending = False).reset_index(drop = True))
    if "expanded" not in st.session_state:
        st.session_state.expanded = True
    # write a function for toggle functionality
    def toggle():
        if st.session_state.expanded:
            st.session_state.expanded = False
    pid = None
    col1, col2 = st.columns(2)
    input_name = col1.text_input("Type Player ID or Player Name", help = "Type Player ID or Part of player name to search.")
    is_numeric = lambda s: s.isdigit()
    if is_numeric(input_name):
        pid = input_name
    else:
        name_part = input_name.lower()
        if name_part:
            df = adf[adf['Player Name_dcd'].str.contains(name_part)].sort_values('max_ovr_rating', ascending = False).reset_index(drop = True)
            with st.expander('Showing Versions of ":violet[{}]"'.format(input_name), expanded = st.session_state.expanded):
                col1, col2, col3, col4, col5, col6, col7 = st.columns([0.075, 0.05, 0.1, 0.15, 0.055, 0.07, 0.50])
                col1.write('')
                col2.write('Ovr. Rat.')
                col3.write('Name')
                col4.write('Pack')
                col5.write('Position')
                col6.write('Playstyle')
                for i in range(df.shape[0]):
                    col1, col2, col3, col4, col5, col6, col7 = st.columns([0.075, 0.05, 0.1, 0.15, 0.055, 0.07, 0.50])
                    if col1.button(label ='Select', key = df['Player ID'].values[i],type = 'primary', on_click = toggle):
                        pid = df['Player ID'].values[i]
                    col2.write(str(df['Overall Rating'].values[i]))
                    col3.write('['+df['Player Name'].values[i]+']({})'.format('https://efootballhub.net/efootball23/player/'+str(df['Player ID'].values[i])))
                    col4.write(df['pack'].values[i])
                    col5.write(df['Position'].values[i])
                    col6.write(df['Playstyle'].values[i])
    if pid:
        pdf = adf[adf['Player ID']==pid]
        if(pdf.shape[0]>0):
            st.subheader("{} - {} {}".format(pdf['Player Name'].values[0],\
            pdf['Overall Rating'].values[0],\
            pdf['Position'].values[0]))
            st.write("Pack: {}".format(pdf['pack'].values[0].lstrip(' ')))
            st.write("Playstyle: {}".format(pdf['Playstyle'].values[0]))
            if('POTW' in pdf['pack'].values[0][1:]):
                st.write('POTW player cannot have skill added.')

            df = find_top_skills(pdf).reset_index(drop = True)
            def gen_reason(pdf, skill, sdict):
                features = sdict[skill].feature_names_in_
                val = np.multiply(pdf[features], sdict[skill].coef_[0]).reset_index(drop = True)
                def top_n_keys(input_dict, n = 3):
                    sorted_items = sorted(input_dict.items(), key=lambda item: item[1], reverse=True)
                    top_n_items = sorted_items[:n]
                    top_n_keys = [item[0] for item in top_n_items]
                    return top_n_keys
                txt = ''
                f_dict = {key: value for key, value in val.T.to_dict()[0].items() if value > 5}
                for item in top_n_keys(f_dict):
                    txt+= '{} {}, '.format(pdf[item].values[0], item)
                return txt
            df['Top Reasons for Suggestion'] = ''
            for i in range(df.shape[0]):
                txt = gen_reason(pdf, df['Suggested Skill'].values[i], sdict)
                df.loc[i, 'Top Reasons for Suggestion'] = txt if txt != '' else 'Multiple Stats Combined'
            st.dataframe(df, hide_index  = False)
            
        else:
            st.write('Player {} not found.'.format(pid))

    st.divider()
    st.write('Example Player ID:')
    st.write(adf[adf['Player ID'].isin([str(i) for i in common_picks])][['Player ID', 'Overall Rating','Player Name','pack']].reset_index(drop = True))

  

if __name__ == "__main__":
    main()