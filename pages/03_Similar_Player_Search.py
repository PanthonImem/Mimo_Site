
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

common_picks = [88029649700314, 88029649706260, 88029649833402]

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
    st.title("Similar Player Search")
    st.write('This tool search for players with similar stats and playstyle. Input their ID or search Player ID by Name below:')
    adf = load_data()
    adf['Player ID'] = adf['Player ID'].astype(str)
    adf['Player Name_dcd'] = adf.apply(lambda row: unidecode(row['Player Name'].lower()), axis = 1)

    with open('data/kdtree_similar_player_search.pkl', 'rb') as file:
        simdict = pickle.load(file)
    with open('data/base_player_avg_stat.pkl', 'rb') as file:
        weightdict = pickle.load(file)
    with open('data/main_skill_stat_dict.pkl', 'rb') as file:
        main_skill_stat_dict = pickle.load(file)

    
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
    
    col1, col2 = st.columns(2)
    show_base_only = col1.checkbox('Show Base Player Only')
    if not show_base_only:
        threshold = col1.select_slider("Select Maximum Stat Distance Threshold", [0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2], 0.7, help = 'Larger value will return more players, but will be less similar')

    if pid:
        pdf = adf[adf['Player ID'] == pid].reset_index(drop = True)
        if pdf.shape[0]:

            pos = pdf['max_position'].values[0].split(',')[0]
            posls = ast.literal_eval(pdf['Possible Positions'].values[0])
            pos = col2.selectbox("Pick Position", posls, posls.index(pos))
            
            st.header(str(pdf['or_'+pos].values[0])+' '+pdf['Player Name'].values[0])

            col1, col2, col3 = st.columns(3)
            col1.write('Pack: {}'.format(pdf['pack'].values[0].lstrip()))
            col2.write("Analyze as Position: {}".format(pos))

            col1.write('Playstyle: {}'.format(pdf['Playstyle'].values[0]))
            st.caption("Only highest/most similar version of each player is shown.")
            def search_similar(pdf, pos):
                for col in ability_cols:
                    pdf[col] = pdf[col] * weightdict[pos][col]
                vec = pdf.loc[0, ability_cols]
                dist, ind = simdict[pos].query(np.array(vec).reshape(1,len(ability_cols)), k=adf.shape[0]) 
                tempdf = adf.loc[ind[0]]
                tempdf['stat_dist'] = np.round(dist[0]/len(ability_cols),2)
                tempdf = tempdf[tempdf['Possible Positions'].str.contains(pos)]
                tempdf = tempdf.sort_values('max_ovr_rating', ascending = False)
                if show_base_only:
                    tempdf = tempdf[tempdf.pack == 'base']

                tempdf = tempdf#.drop_duplicates(['Player Name','Playstyle']).reset_index(drop = True)
                tempdf = tempdf.sort_values('stat_dist')
                tempdf = tempdf[tempdf.stat_dist>0]
                return tempdf

            rdf = search_similar(pdf, pos)          

            rdf['Player ID'] = ["https://efootballhub.net/efootball23/compare2players?player1Id={}&player2Id={}"\
            .format(str(pid),str(i)) for i in rdf['Player ID'].values]

            rdf['Similarity'] = "Not Similar"
            rdf.loc[rdf.stat_dist <1.2, 'Similarity'] = "Some resemblance but different player"
            rdf.loc[rdf.stat_dist <0.75, 'Similarity'] = "Kind of Similar"
            rdf.loc[rdf.stat_dist <0.60, 'Similarity'] = "Similar"
            rdf.loc[rdf.stat_dist <0.45, 'Similarity'] = "Very Similar"


            rdf['Pros'] = ''
            rdf['Cons'] = ''
            for skill in main_skill_stat_dict[pos]['primary_skill']+main_skill_stat_dict[pos]['secondary_skill']:
                if pdf['s_'+skill].values[0]==0:
                    rdf.loc[(rdf['s_'+skill]==1), 'Pros'] += '+{}<br>'.format(skill)
                if pdf['s_'+skill].values[0]==1:
                    rdf.loc[(rdf['s_'+skill]==0), 'Cons'] += '-{}<br>'.format(skill)
            if pdf['Form'].values[0]=='Unwavering':
                rdf.loc[(rdf['Form']=='Standard'), 'Cons'] += '-Standard Form<br>'
                rdf.loc[(rdf['Form']=='Inconsistent'), 'Cons'] += '-Inconsistent Form<br>'
            if pdf['Form'].values[0]=='Standard':
                rdf.loc[(rdf['Form']=='Unwavering'), 'Pros'] += '+Unwavering Form<br>'
                rdf.loc[(rdf['Form']=='Inconsistent'), 'Cons'] += '-Inconsistent Form<br>'
            if pdf['Form'].values[0]=='Inconsistent':
                rdf.loc[(rdf['Form']=='Unwavering'), 'Pros'] += '+Unwavering Form<br>'
                rdf.loc[(rdf['Form']=='Standard'), 'Pros'] += '+Standard Form<br>'

            if show_base_only:
                threshold = 10

            def make_clickable(link):
                text = link.split('=')[-1]
                return f'<a target="_blank" href="{link}">{text}</a>'

            # link is the column with hyperlinks
            playstyle = pdf['Playstyle'].values[0]

            if (playstyle in get_unactivated(pos)):
                playstyle = 'Inactivated'
            rdf['Player ID'] = rdf['Player ID'].apply(make_clickable)
            rdf.loc[rdf['Playstyle'].isin(get_unactivated(pos)), 'Playstyle'] = 'Inactivated'

            rdf = rdf[['Player ID','or_'+pos,'Player Name','pack','Playstyle','stat_dist','Similarity','Pros','Cons']]
            rdf1 = rdf[(rdf['or_'+pos]-pdf['or_'+pos].values[0])>=-1]            
            rdf2 = rdf1[(rdf1.Playstyle == playstyle)&(rdf1.stat_dist<=threshold)]
            showdf = rdf2[0:10]

            st.subheader('Good Replacement')
            if(showdf.shape[0]>0):
                st.write(showdf.reset_index(drop = True).to_html(escape=False), unsafe_allow_html=True)
            else:
                st.caption('There is no good substitute for this player. Try increasing search threshold.')

            rdf3 = rdf1[(rdf1.Playstyle != playstyle)&(rdf1.stat_dist<=threshold)]
            showdf = rdf3[0:10]
            st.subheader('Similar Stat, Different Playstyle')
            if(showdf.shape[0]>0):
                st.write(showdf.reset_index(drop = True).to_html(escape=False), unsafe_allow_html=True)
            else:
                st.caption('There is no similar card with different playstyle for this player. Try increasing search threshold.')


            rdf4 = rdf[(rdf['or_'+pos]-pdf['or_'+pos].values[0])<-1]
            rdf4 = rdf4[(rdf4.stat_dist<=threshold)&(rdf4.Playstyle == playstyle)]
            showdf = rdf4[0:10]
            st.subheader('Lite version -- similar but weaker')
            if(showdf.shape[0]>0):
                st.write(showdf.reset_index(drop = True).to_html(escape=False), unsafe_allow_html=True)
            else:
                st.caption('There is no lite version for this player. Try increasing search threshold.')
        else:
            st.caption('Player Not Found')

    st.divider()
    st.write('Example Player ID:')
    st.write(adf[adf['Player ID'].isin([str(i) for i in common_picks])][['Player ID', 'Overall Rating','Player Name','pack']].reset_index(drop = True))


            #st.write(rdf1[rdf1.Playstyle != playstyle][:10].to_html(escape=False), unsafe_allow_html=True)
        


if __name__ == "__main__":
    main()