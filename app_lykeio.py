import streamlit as st

st.set_page_config(page_title="Home", page_icon="🏠")

st.title("🏠 Καλωσήρθες στο Εκπαιδευτικό Εργαλείο Βιολογίας")

st.markdown("Χρησιμοποίησε το μενού αριστερά ή πάτησε παρακάτω για να ξεκινήσεις:")

if st.button("📚 Μετάβαση στη Library"):
    st.switch_page("pages/1_Library.py")
