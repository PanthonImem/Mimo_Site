
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
    st.set_page_config(layout="wide")
    st.title("Mimo Player Search by Skill")
    if 'df' not in st.session_state:
        st.session_state['df'] = pd.read_csv('data/mimo_dataset.csv')
    adf = st.session_state['df']
    adf['Player ID'] = adf['Player ID'].astype(str)
    st.write('Powered by Mimo Skill Fit Score')

    skills = st.multiselect(
    'Select Skill(s) You Have. Only players :red[without any] of the skills you select will be shown',
    sset, ['Double Touch', 'Sole Control'], max_selections = 5)

    skill_weight = st.select_slider('Weight between Skill Fit Score and Overall Rating for Sorting', 
    [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1], value = 0.2, help = '0 = entirely by Overall Rating, 1 = entirely by Skill Fit Score')

    adf['skill_score_avg'] = 0
    adf['no_skill'] = True
    for skill in skills:
         adf['skill_score_avg'] += adf['pred_'+skill]/len(skills)
         adf['no_skill'] = adf['no_skill'] & ~adf['s_'+skill]
    adf['final_score'] = np.round(skill_weight*adf['skill_score_avg']+(1-skill_weight)*adf['max_ovr_rating'].clip(40,99),1)

    df = adf[(adf['no_skill']==1)&(adf['Maximum Level']>1)&(adf['final_score']>=10)].sort_values('final_score', ascending = False)\
[['skill_score_avg', 'Overall Rating','Player Name','pack', 'Position','Playstyle','Player ID']]
    df = df.reset_index(drop = True).rename({'skill_score_avg':'Mimo Skill Score'}, axis = 1)
    st.dataframe(df[:120])


if __name__ == "__main__":
    main()