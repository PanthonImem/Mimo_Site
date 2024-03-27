
import pandas as pd
import numpy as np
import streamlit as st

import warnings
warnings.filterwarnings('ignore')

import sys
sys.path.append("code")
from utility import hide_github

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

nc_packs = [
    " Mid-season MVPs Jan '23",
    " Transfer Feb '23",
    " European Club Championship Selection 16 Mar '23",
    " Masterful Stars 13 Apr '23",
    " End-season MVPs 11 May '23",
    " European Club Championship 16 Jun '22",
    " European Masters Cup 16 Jun '22",
    " Breakout Stars Jul '22",
    " Back in the Game 3 Aug '23",
    " Transfer Aug '22",
    " Transfer Oct '22",
    " Alltime Greats Nov '22",
    " Golden Boys Dec '22",
]

@st.cache_data
def load_data():
	return pd.read_csv('data/new_mimo_dataset.csv')

def main():
    st.set_page_config(layout="wide")
    hide_github()
    st.title("Mimo Player Search by Skill")
    adf = load_data()
    adf['Player ID'] = adf['Player ID'].astype(str)
    st.write('Powered by :orange[Mimo Skill Fit Score]')

    st.write('This page takes in skill(s) you have and suggest a list of high overall players that look fit for training with that skill(s).')
    skills = st.multiselect(
    'Select Skill(s) You Have. Only players :red[without any] of the skills you select will be shown',
    sset, ['Gamesmanship'], max_selections = 5)

    skill_weight = st.select_slider('Weight between Skill Fit Score and Overall Rating for Sorting', 
    [np.round(0.05 * i,2) for i in range(21)], value = 0.2, help = '0 = entirely by Overall Rating, 1 = entirely by Skill Fit Score')

    sc1, sc2 = st.columns((1,2))
    with sc1:
        pos = pos = st.selectbox('Position Filter', ['All']+list((adf['Position'].unique())))


    pack_filter = st.radio("Pack Filter", ["All", 'Epic/BT/ST Only','F2P-Friendly Only'])
    adf['skill_score_avg'] = 0
    adf['no_skill'] = True
    for skill in skills:
         adf['skill_score_avg'] += adf['pred_'+skill]/len(skills)
         adf['no_skill'] = adf['no_skill'] & ~adf['s_'+skill]
    adf['final_score'] = np.round(skill_weight*adf['skill_score_avg']+(1-skill_weight)*adf['max_ovr_rating'].clip(40,99),1)


    df = adf[(adf['no_skill']==1)&(adf['Maximum Level']>1)&(adf['final_score']>=10)].sort_values('final_score', ascending = False)\

    
    if pack_filter == 'Epic/BT/ST Only':
        df = df[(df['pack'].str.contains('Big Time')|df['pack'].str.contains('Show Time')|df['pack'].str.contains('-')\
     |df['pack'].str.contains('19')|df['pack'].str.contains('20'))&(~df['pack'].str.contains("Fans' Choice"))\
     &(~df['pack'].str.contains("Highlight"))&(~df['pack'].str.contains("Derby"))&(~df['pack'].str.contains("Selection"))&\
     ~df['pack'].str.contains("Pack")&~df['pack'].isin(nc_packs)]
        df = df[df.Condition == 'B']

    elif pack_filter == 'F2P-Friendly Only':
        ind = df['pack'].str.contains('Big Time')|df['pack'].str.contains('Show Time')|df['pack'].str.contains('-')\
     |df['pack'].str.contains('19')|df['pack'].str.contains('20')|df['pack'].str.contains('Highlight')
        df = df[~ind]

    if pos != 'All':
        df = df[df['max_position'].str.contains(pos)]
    df = df.reset_index(drop = True).rename({'skill_score_avg':'Mimo Skill Fit Score'}, axis = 1)
    df = df.drop('Condition', axis = 1)
    st.dataframe(df[['Mimo Skill Fit Score', 'Overall Rating','Player Name','pack', 'Position','Playstyle','Player ID']][:120])


if __name__ == "__main__":
    main()