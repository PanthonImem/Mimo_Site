
import pandas as pd
import numpy as np
import streamlit as st

import warnings
warnings.filterwarnings('ignore')

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
 'Long-Range Shooting',
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

def main():
    st.title("Mimo Player Search by Skill")
    adf = pd.read_csv('data/mimo_skill.csv')
    adf['Player ID'] = adf['Player ID'].astype(str)
    st.write('Powered by Mimo Skill Score')
    skill = st.selectbox('Select Skill You Have',sset)
    if skill:
        st.write('The sorting is done by overall rating + how likely the player should have the skill based on stats/position/playstyle')
        df = adf[(adf['s_'+skill]==0)&(adf['Maximum Level']>1)&(adf['pred_'+skill]>=25)].sort_values('skill_addition_score_'+skill, ascending = False)\
[['pred_'+skill, 'Overall Rating','Player Name','pack', 'Position','Playstyle','Player ID']]
        df = df.reset_index(drop = True).rename({'pred_'+skill:'Mimo Skill Score: {}'.format(skill)}, axis = 1)
        st.dataframe(df[:120])
    else:
        st.write('Error')


if __name__ == "__main__":
    main()