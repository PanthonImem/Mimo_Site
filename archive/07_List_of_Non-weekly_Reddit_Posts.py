import streamlit as st
import warnings
warnings.filterwarnings('ignore')

def main():
    st.set_page_config(layout="wide")
    st.title("My Writing on Efootball")

    st.write("List of my non-weekly Reddit posts")

    st.write("[Analysis of Stats Profile of GK](https://www.reddit.com/r/pesmobile/comments/15128uq/analysis_of_stats_profile_of_goalkeepersgk_mimos/)")

    st.write("[Here is How Overall Rating Works](https://www.reddit.com/r/pesmobile/comments/14xov22/here_is_how_overall_rating_works_mimos_post/)")

    st.write("[Using Inconsistent Form Players](https://www.reddit.com/r/pesmobile/comments/146myro/using_inconsistent_form_players_mimos_post/)")

    st.write("[Analysis of Wide Players Skills](https://www.reddit.com/r/pesmobile/comments/138gvpb/analysis_of_wide_playerslwf_rwf_lmf_rmf_skills/)")

    st.write("[Analysis of CF Players Skill](https://www.reddit.com/r/pesmobile/comments/132p86n/analysis_of_cf_player_skills_mimos_post/)")

    st.write("[A Full List of POTW Players Who Have Higher Overall Rating Outside of Position](https://www.reddit.com/r/pesmobile/comments/12d9ae0/a_full_list_of_potw_players_who_have_higher/)")

    
if __name__ == "__main__":
    main()