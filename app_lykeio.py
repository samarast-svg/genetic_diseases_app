import streamlit as st

st.set_page_config(page_title="Home", page_icon="🏠")

st.title("🏠 Welcome to GenEdu")
st.subheader("An interactive Genetics Education Tool for High School Biology")

st.markdown("Χρησιμοποίησε το μενού αριστερά ή πάτησε παρακάτω για να ξεκινήσεις:")

if st.button("📚 Μετάβαση στη Library"):
    st.switch_page("pages/1_Library.py")


