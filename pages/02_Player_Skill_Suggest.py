
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


common_picks = [88029649833393, 88029649836770, 88029649833414]+[105624520229984, 105624520206751, 105624520215799, 105625325514975,
       105625325547356, 105625325542316, 105625325510796, 105625325513700,
       105625325510960, 105625325514599, 105625325463961]

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
	return pd.read_csv('data/mimo_dataset.csv')

def main():
    st.set_page_config(layout="centered")
    hide_github()
    st.title("Mimo Skill Suggest")
    st.write('Powered by :orange[Mimo Skill Fit Score]')
    adf = load_data()
    adf['Player ID'] = adf['Player ID'].astype(str)
    adf['Player Name_dcd'] = adf.apply(lambda row: unidecode(row['Player Name'].lower()), axis = 1)
    with open('data/skill_suggest_dict.pkl', 'rb') as file:
        sdict = pickle.load(file)

    st.write('Enter Player ID to obtain Skill Suggestion.')
    st.write("Mimo Skill Fit Score goes between 0 to 100. Higher means the model thinks the player should have this skill based on stats.")
    st.write("Generally, >70 is very nice to add, 30-70 is nice to have but not essential")

    with st.expander("Player ID Search by Name"):
        name_part = st.text_input("Enter Player Name", help = "Type part of player name to search.")
        if name_part:
            name_part = name_part.lower()
            st.write(adf[adf['Player Name_dcd'].str.contains(name_part)][['Player ID', 'Overall Rating','Player Name','pack']].sort_values('Overall Rating', ascending = False).reset_index(drop = True))

    pid = st.text_input("Enter Player ID:", help = 'Player ID is a number unique to each player in the game.\
     You can obtain the player ID of each card from the URL of any Database website such as PESDB or EFHub or the Search by Name tool above.')
    
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