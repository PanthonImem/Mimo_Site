
import pandas as pd
import numpy as np
import streamlit as st
import pickle
import ast
from unidecode import unidecode
import warnings
warnings.filterwarnings('ignore')

import sys
sys.path.append("code")
from utility import hide_github

ability_cols = ['Offensive Awareness',
 'Ball Control',
 'Dribbling',
 'Tight Possession',
 'Low Pass',
 'Lofted Pass',
 'Finishing',
 'Heading',
 'Set Piece Taking',
 'Curl',
 'Defensive Awareness',
 'Tackling',
 'Aggression',
 'Defensive Engagement',
 'GK Awareness',
 'GK Catching',
 'GK Parrying',
 'GK Reflexes',
 'GK Reach',
 'Speed',
 'Acceleration',
 'Kicking Power',
 'Jumping',
 'Physical Contact',
 'Balance',
 'Stamina']

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
    hide_github()
    st.title("Player Analysis")
    st.write('This tool visualizes player stats and skills for analysis. Input their ID or search Player ID by Name below:')
    adf = load_data()
    adf['Player ID'] = adf['Player ID'].astype(str)
    adf['Player Name_dcd'] = adf.apply(lambda row: unidecode(row['Player Name'].lower()), axis = 1)

    with open('data/stat_stat_by_position.pkl', 'rb') as file:
        refdict = pickle.load(file)

    with open('data/main_skill_stat_dict.pkl', 'rb') as file:
        main_skill_stat_dict = pickle.load(file)

    st.markdown("""
    <style>
    [data-testid=column]:nth-of-type(1) [data-testid=stVerticalBlock]{
        gap: 0.05rem;
    }
    [data-testid=column]:nth-of-type(2) [data-testid=stVerticalBlock]{
        gap: 0.05rem;
    }
    [data-testid=column]:nth-of-type(3) [data-testid=stVerticalBlock]{
        gap: 0.05rem;
    }
    [data-testid=column]:nth-of-type(4) [data-testid=stVerticalBlock]{
        gap: 0.05rem;
    }
    </style>
    """,unsafe_allow_html=True)

    with st.expander("Player ID Search by Name"):
        name_part = st.text_input("Type Player Name", help = "Type part of player name to search.")
        name_part = name_part.lower()
        if name_part:
            st.write(adf[adf['Player Name_dcd'].str.contains(name_part)][['Player ID', 'Overall Rating','Player Name','pack']].sort_values('Overall Rating', ascending = False).reset_index(drop = True))
    col1, col2, col3 = st.columns(3)
    pid = col1.text_input("Enter Player ID:", help = 'Player ID is a number unique to each player in the game.\
     You can obtain the player ID of each card from the URL of any Database website such as PESDB or EFHub or the Search by Name tool above.')
    col1, col2, col3 = st.columns(3)
    col_per = col1
    
    
    if pid:
        pdf = adf[adf['Player ID'] == pid].reset_index(drop = True)
        if pdf.shape[0]:

            pos = pdf['max_position'].values[0].split(',')[0]
            posls = ast.literal_eval(pdf['Possible Positions'].values[0])
            pos = col2.selectbox("Pick Position for Analysis", posls, posls.index(pos))
            col1.header(str(pdf['or_'+pos].values[0])+' '+pdf['Player Name'].values[0])

            col1, col2, col3 = st.columns(3)

            
            col2.write("Best Positions: {} at {}".format(pdf['max_ovr_rating'].values[0], pdf['max_position'].values[0]))
            comp_base = col2.checkbox('Compare to Base', value = True)
            if comp_base:
                bdf = adf[(adf['Player Name']==pdf['Player Name'].values[0])&(adf['pack']=='base')]

            col1.write("Pack: {}".format(pdf['pack'].values[0].lstrip()))
            
            col1.write("Playstyle: {} {} {}".format(pdf['Playstyle'].values[0],\
             "(Inactivated)" if pdf['Playstyle'].values[0] in get_unactivated(pos) else '',\
             "(from {})".format(bdf['Playstyle'].values[0]) if comp_base and bdf['Playstyle'].values[0]!=pdf['Playstyle'].values[0] else ''))

            col1.write("Form: {}".format(pdf['Form'].values[0]))
            
            
            
            def display_stat(col, stat):
                def autocolor(val):
                    cutoff = np.array([-0.75, 0.75, 1.5])
                    colorls = ['red','orange','green','violet']
                    ind = np.sum(val>cutoff)
                    return colorls[ind]
                col1, col2, col3 = col.columns([0.6, 0.2, 0.2])
                val = np.round((pdf[stat].values[0]-refdict[pos][stat]['mean'])/refdict[pos][stat]['std'],2)
                colstr = autocolor(val)
                col1.markdown(f'{stat}')
                col2.markdown(':'+colstr+'['+f'{pdf[stat].values[0]}]')

                if comp_base:
                    diff = pdf[stat].values[0]-bdf[stat].values[0]
                    if(diff > 0):
                        col3.markdown(':green[+'+str(diff)+']')
                    elif(diff<0):
                        col3.markdown(':red['+str(diff)+']')

            def display_skill(col, skill):
                col1, col2, col3 = col.columns([0.6, 0.2, 0.2])
                col1.write(f'{skill}')
                if pdf['s_'+skill].values[0]==1:
                    col2.write(':green[✓]')
                else:
                    col2.write(' ')

                if comp_base:
                    if bdf['s_'+skill].values[0]==0 and pdf['s_'+skill].values[0]==1:
                        col3.write(':green[+]')
                    elif bdf['s_'+skill].values[0]==1 and pdf['s_'+skill].values[0]==0:
                        col3.write(':red[x]')
                    

            def display_weak_foot(col, weak_foot):
                wf_dict = { "Almost Never": 'red', 'Rarely':'orange', 'Regularly': 'green', "Occasionally" :"violet", \
                    "Low": 'red',  "Medium": 'orange',"High":  'green', "Very High": "violet"}
                col1, col2 = col.columns([0.6, 0.4])
                col1.write(f'{weak_foot}')
                col2.write(f':{wf_dict[pdf[weak_foot].values[0]]}[{pdf[weak_foot].values[0]}]')


            col1, col2, col3, col4, col5 = st.columns(5) 


            col1.subheader('Attacking')
            display_stat(col1, 'Offensive Awareness')
            display_stat(col1, 'Finishing')
            display_skill(col1, 'First-time Shot')
            display_skill(col1, 'Acrobatic Finishing')
            display_skill(col1, 'Chip Shot Control')
            display_weak_foot(col1, 'Weak Foot Usage')
            display_weak_foot(col1, 'Weak Foot Accuracy')
            col1.caption('---')
  

            col1.subheader('Shooting')
            display_stat(col1, 'Kicking Power')
            display_skill(col1, 'Long Range Shooting')
            display_skill(col1, 'Rising Shot')
            display_skill(col1, 'Dipping Shot')
            display_skill(col1, 'Knuckle Shot')
            col1.caption('---')

            col1.subheader('Set Piece')
            display_stat(col1, 'Set Piece Taking')
            display_skill(col1, 'Penalty Specialist')

            col2.subheader('Pace')
            display_stat(col2, 'Speed')
            display_stat(col2, 'Acceleration')
            col2.caption('---')    

            col2.subheader('Dribbling')
            display_stat(col2, 'Ball Control')
            display_stat(col2, 'Dribbling')
            display_stat(col2, 'Tight Possession')
            display_stat(col2, 'Balance')
            display_skill(col2, 'Sole Control')
            display_skill(col2, 'Double Touch')
            display_skill(col2, 'Flip Flap')
            display_skill(col2, 'Gamesmanship')
            display_skill(col2, 'Heel Trick')
            display_skill(col2, 'No Look Pass')
            display_skill(col2, 'Marseille Turn')
            display_skill(col2, 'Cut Behind &; Turn')
            display_skill(col2, 'Chop Turn')
            display_skill(col2, 'Scissors Feint')
            display_skill(col2, 'Scotch Move')
            display_skill(col2, 'Sombrero')
            display_skill(col2, 'Rabona')

                    
    
            col3.subheader('Passing')
            display_stat(col3, 'Low Pass')
            display_skill(col3, 'One-touch Pass')
            display_skill(col3, 'Through Passing')
            display_skill(col3, 'Weighted Pass')
            col3.caption('---')
            display_stat(col3, 'Lofted Pass')
            display_skill(col3, 'Low Lofted Pass')
            display_skill(col3, 'Pinpoint Crossing')
            display_stat(col3, 'Curl')
            display_skill(col3, 'Outside Curler')
            display_skill(col3, 'Long-Range Curler')
            col3.caption('---')

            col3.subheader('Utility')

            display_stat(col3, 'Stamina')
            display_skill(col3, 'Fighting Spirit')
            display_skill(col3, 'Captaincy')
            display_skill(col3, 'Track Back')
            display_skill(col3, 'Super-sub')

            col4.subheader('Physical')
            display_stat(col4, 'Physical Contact')
            display_stat(col4, 'Height')
            display_stat(col4, 'Jumping')
            display_skill(col4, 'Aerial Superiority')
            display_stat(col4, 'Heading')
            display_skill(col4, 'Heading')
            
            col4.caption('---')

            col4.subheader('Defense')
            display_stat(col4, 'Defensive Awareness')
            display_stat(col4, 'Tackling')
            display_stat(col4, 'Aggression')
            display_stat(col4, 'Defensive Engagement')
            display_skill(col4, 'Interception')
            display_skill(col4, 'Man Marking')
            display_skill(col4, 'Blocker')
            display_skill(col4, 'Acrobatic Clear')
            display_skill(col4, 'Sliding Tackle')

            

            st.divider()
    

if __name__ == "__main__":
    main()