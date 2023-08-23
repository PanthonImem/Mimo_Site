import streamlit as st
import warnings
warnings.filterwarnings('ignore')

def main():
    st.set_page_config(layout="wide")
    st.title(":orange[Mimo Skill Fit Score]")

    st.write("This page documents the inner working of :orange[Mimo Skill Fit Score].")

    st.subheader("Background:")
    st.write(f""" With the introduction of Skill Training, a big question many players have is **1) "I have this skill, who should I add it to?"** and\
     **2) "I have this player, what skills should I plan to add?"** """)

    st.subheader("Model Assumption:")

    st.write(f"The word **Fit** is a strong word -- there is no systematic way to tell whether a skill fits a player well")

    st.write("So instead an assumption is made for this model:")
    
    st.write(f"**A skill is fit for a player -- if the player is statistically likely to have this skill given the stats, positions, and playstyle.**")

    st.write(f"So if most players with **Pinpoint Crossing** have high **Lofted Pass**.\
    Then we assume that **Pinpoint Crossing** is fit for players with high **Lofted Pass**")

    st.write(f"If most players with **Interception** have high **Defensive Awareness** and can play in defensive positions.\
    Then we assume that **Interception** is fit for defensive players with high **Interception**.")

    st.write("Obviously there is a big limitation with correlation and causation here. We will discuss this more on the Limitation section.")

    st.subheader("Methodology:")
    st.write("43 Logistic Regression models are created -- one for each skills. Each takes in player stats + one-hot encoding of positions the player can play at + playstyle + Age\
     and tries to predict whether a player would have a specific skill. Then we take the probability of a player having a skill as :orange[Mimo Skill Fit Score]")

    st.write("Different Skills have different performance -- in general the model does well in skills like Man Marking, Interception, First-time Shot\
     but less well in skills like Rising Shots, Fighting Spirit, Captaincy and Sole Control.")

    st.subheader("Limitation:")

    st.write(f"**1. Correlation != Causation**")
    st.write("The model here is exploiting correlation between stats and skills in player data to suggest skills that it thinks Konami might assign to players.\
    However, just because certain types of players frequently have a skill does not necessarily mean the skill will only be good on that type of player.")

    st.write("For example, Captaincy is usually found in older and slower players. It doesn't mean younger or faster players will be any less good as a captain.\
    Just that the model cannot know this from data alone. Another example is interception. As a skill primarily found in CB/DMF, the model will try to\
    suggest the skill for defensive players. However some people also like Interception in Forward as it helps in creating a chance of a dangerous counterattack.\
    ")

    st.write(f"**2. Not all skills are equally useful.**")
    st.write("Skills like Cut Behing & Turn or Chop Turn are suggested very frequently because they are common skills.\
    However many dribblers perfer just Double Touch or Marseille Turn over most other Dribbling skills.\
     On the other hand skills like One-touch Pass are very useful for almost every position and you might prefer that to a dribbling skill you don't care about.")


    st.write("So in conclusion, Mimo Skill Fit score serves as a tool to help with skill selection but it's not meant to be a de-facto list. It just gives you skills that look common for that stats/position profile.")
    

    


if __name__ == "__main__":
    main()