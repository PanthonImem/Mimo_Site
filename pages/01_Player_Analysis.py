
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
    if "pid" not in st.session_state:
        st.session_state.pid = None
    pid = st.session_state.pid
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
    input_name = st.text_input("Type Player ID or Player Name", help = "Type Player ID or Part of player name to search.")
    is_numeric = lambda s: s.isdigit()
    if is_numeric(input_name):
        st.session_state.pid = input_name
        pid = st.session_state.pid
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
                        st.session_state.pid =  df['Player ID'].values[i]
                        pid = st.session_state.pid
                    col2.write(str(df['Overall Rating'].values[i]))
                    col3.write('['+df['Player Name'].values[i]+']({})'.format('https://efootballhub.net/efootball23/player/'+str(df['Player ID'].values[i])))
                    col4.write(df['pack'].values[i])
                    col5.write(df['Position'].values[i])
                    col6.write(df['Playstyle'].values[i])    
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

            pstr = ""
            if comp_base:
                bdf = adf[(adf['Player Name']==pdf['Player Name'].values[0])&(adf['pack']=='base')]
                if bdf.shape[0] == 0:
                    col2.text('Base Player Not Found')
                    comp_base = False
                    bdf = pdf.copy()
                else:
                    pstr =  "(from {})".format(bdf['Playstyle'].values[0]) if comp_base and bdf['Playstyle'].values[0]!=pdf['Playstyle'].values[0] else ''
            else:
                bdf = pdf.copy()

            col1.write("Pack: {}".format(pdf['pack'].values[0].lstrip()))
            
            col1.write("Playstyle: {} {} {}".format(pdf['Playstyle'].values[0],\
             "(Inactivated)" if pdf['Playstyle'].values[0] in get_unactivated(pos) else '',\
            pstr))

            col1.write("Form: {}".format(pdf['Form'].values[0]))
            
            def display_stat(col, stat):
                def autocolor(val):
                    cutoff = np.array([-0.75, 0.75, 1.5])
                    colorls = ['red','orange','green','violet']
                    ind = np.sum(val>cutoff)
                    return colorls[ind]
                col1, col2, col3 = col.columns([0.7, 0.15, 0.15])
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
                col1, col2, col3 = col.columns([0.7, 0.15, 0.15])
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
                col1, col2 = col.columns([0.7, 0.3])
                col1.write(f'{weak_foot}')
                col2.write(f':{wf_dict[pdf[weak_foot].values[0]]}[{pdf[weak_foot].values[0]}]')

            def display_strong_foot(col):
                col1, col2 = col.columns([0.7, 0.3])
                col1.write('Foot')
                col2.write('{}'.format(':green['+pdf['Stronger Foot'].values[0].split(' ')[0]+']'))



            col1, col2, col3, col4, col5 = st.columns(5) 


            col1.subheader('Attacking')
            display_stat(col1, 'Offensive Awareness')
            display_stat(col1, 'Finishing')
            display_skill(col1, 'First-time Shot')
            display_skill(col1, 'Acrobatic Finishing')
            display_skill(col1, 'Chip Shot Control')
            display_strong_foot(col1)
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
            st.subheader('Version Comparison')
               
            cdf = pd.concat([pdf,
                            adf[(adf['Player Name'].values==pdf['Player Name'].values[0])&(adf['Player ID']!=pid)].sort_values('max_ovr_rating', ascending = False)
                            ])            

            def plot_comparison(stat):
                cols = st.columns([0.1]+[0.8/cdf.shape[0]]*cdf.shape[0])
                cols[0].markdown(f'{stat}')
                for i in range(cdf.shape[0]):
                    if(stat in ['Player Name','pack','Playstyle']):
                        if(stat == 'Playstyle'):
                            if(cdf[stat].values[i] != bdf[stat].values[0]):
                                cols[i+1].markdown(':violet['+str(cdf[stat].values[i])+']')
                            else:
                                cols[i+1].markdown(':black['+str(cdf[stat].values[i])+']')

                        else:
                            cols[i+1].markdown(':black['+str(cdf[stat].values[i])+']')
                    elif stat in (['OR at {}'.format(pos)]):
                        stat = 'or_'+pos
                        if(cdf[stat].values[i] == cdf[stat].max()):
                            cols[i+1].markdown(':violet['+str(cdf[stat].values[i])+']')
                        elif(cdf[stat].values[i] > bdf[stat].values[0]):
                            cols[i+1].markdown(':green['+str(cdf[stat].values[i])+']')
                        elif(cdf[stat].values[i] < bdf[stat].values[0]):
                            cols[i+1].markdown(':red['+str(cdf[stat].values[i])+']')
                        else:
                            cols[i+1].markdown(':orange['+str(cdf[stat].values[i])+']')
                    else:
                        if(cdf[stat].values[i] == cdf[stat].max()):
                            cols[i+1].markdown(':violet['+str(cdf[stat].values[i])+']')
                        elif(cdf[stat].values[i] > bdf[stat].values[0]):
                            cols[i+1].markdown(':green['+str(cdf[stat].values[i])+']')
                        elif(cdf[stat].values[i] < bdf[stat].values[0]):
                            cols[i+1].markdown(':red['+str(cdf[stat].values[i])+']')
                        else:
                            cols[i+1].markdown(':orange['+str(cdf[stat].values[i])+']')
            def plot_skill_added():
                cols = st.columns([0.1]+[0.8/cdf.shape[0]]*cdf.shape[0])
                cols[0].markdown('Skill Added')
                for i in range(cdf.shape[0]):
                    ls = []
                    for skill in sset:
                        if((cdf['s_'+skill].values[i]==1)&(bdf['s_'+skill].values[0]==0)):
                            ls.append(skill)
                    if(len(ls)):
                        cols[i+1].markdown(':green[' + ', '.join(ls)+']')
                    else:
                        cols[i+1].markdown(' ')
            def plot_skill_loss():
                cols = st.columns([0.1]+[0.8/cdf.shape[0]]*cdf.shape[0])
                cols[0].markdown('Skill Lost')
                for i in range(cdf.shape[0]):
                    ls = []
                    for skill in sset:
                        if((cdf['s_'+skill].values[i]==0)&(bdf['s_'+skill].values[0]==1)):
                            ls.append(skill)
                    if(len(ls)):
                        cols[i+1].markdown(':red['+ ', '.join(ls)+']')
                    else:
                        cols[i+1].markdown(' ')
            
            plot_comparison('Overall Rating')
            plot_comparison('OR at {}'.format(pos))
            plot_comparison('Player Name')
            plot_comparison('Playstyle')
            plot_comparison('pack')
            for ability in ability_cols:
                if(pos!='GK' and 'GK' not in ability):
                    plot_comparison(ability)
            plot_skill_added()
            plot_skill_loss()
            

if __name__ == "__main__":
    main()