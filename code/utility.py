
import streamlit as st
def hide_github():
    st.markdown(
        """
        <style>
        .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
        .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
        .viewerBadge_text__1JaDK, css-ztfqz8 ef3psqc4, {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )