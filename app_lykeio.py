import streamlit as st

# Κάνει redirect στη σελίδα Library (1_Library.py)
st.set_page_config(page_title="Library", page_icon="📚")

st.switch_page("pages/1_Library.py")
