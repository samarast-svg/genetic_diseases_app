import streamlit as st
import pandas as pd
import random

st.set_page_config(
    page_title="Flashcards – Γενετικές Ασθένειες",
    page_icon="🃏",
    layout="centered"
)

# -----------------------------
# Φόρτωση dataset
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("genetic_diseases_lykeio_full_en.csv")

df = load_data()

st.title("🃏 Flashcards – Γενετικές Ασθένειες")
st.markdown("Μάθε τις ασθένειες με flashcards: δες το όνομα, σκέψου την απάντηση και μετά γύρνα την κάρτα 👇")

# -----------------------------
# State management
# -----------------------------
if "flashcards" not in st.session_state:
    # ανακάτεμα όλων των ασθενειών
    st.session_state.flashcards = random.sample(df.to_dict("records"), len(df))
    st.session_state.flash_index = 0
    st.session_state.flash_show_answer = False

# -----------------------------
# Τρέχουσα κάρτα
# -----------------------------
if st.session_state.flash_index >= len(st.session_state.flashcards):
    st.success("🎉 Τέλος! Εξέτασες όλες τις κάρτες.")
    if st.button("🔄 Ξεκίνα ξανά"):
        st.session_state.flashcards = random.sample(df.to_dict("records"), len(df))
        st.session_state.flash_index = 0
        st.session_state.flash_show_answer = False
        st.rerun()
    st.stop()

row = st.session_state.flashcards[st.session_state.flash_index]

st.subheader(f"Κάρτα {st.session_state.flash_index+1}/{len(st.session_state.flashcards)}")

if not st.session_state.flash_show_answer:
    # Ερώτηση
    st.markdown(f"### 🧬 {row['Disease']}")
    st.info("👉 Σκέψου ποια είναι η κληρονομικότητα, ο τύπος μετάλλαξης και το γονίδιο. Μετά πάτησε το κουμπί για να δεις.")
    if st.button("Δείξε την απάντηση"):
        st.session_state.flash_show_answer = True
        st.rerun()
else:
    # Απάντηση
    st.markdown(f"""
    ### 🧬 {row['Disease']}
    - **Τύπος μετάλλαξης:** {row['MutationType']}
    - **Κληρονομικότητα:** {row['Inheritance']}
    - **Γονίδιο/Χρωμόσωμα:** {row['Gene/Chromosome']}
    - **Διάγνωση:** {row['Diagnostics']}
    - **Φαινότυπος:** {row['Phenotype']}
    """)
    if st.button("➡️ Επόμενη κάρτα"):
        st.session_state.flash_index += 1
        st.session_state.flash_show_answer = False
        st.rerun()
