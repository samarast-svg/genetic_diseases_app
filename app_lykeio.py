import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Library",   # 👈 αυτό θα φαίνεται στο sidebar
    page_icon="📚",
    layout="centered"
)

# Φόρτωση dataset με ελληνικές και αγγλικές ονομασίες
@st.cache_data
def load_data():
    return pd.read_csv("genetic_diseases_lykeio_full_en.csv")

df = load_data()

st.set_page_config(
    page_title="Γενετικές Ασθένειες – Βιολογία Γ’ Λυκείου",
    page_icon="🧬",
    layout="centered"
)

st.title("🧬 Γενετικές Ασθένειες - Βιολογία Γ’ Λυκείου")

# Πεδίο αναζήτησης
query = st.text_input("🔎 Αναζήτηση ασθένειας ή λέξης-κλειδί:")

if query:
    results = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]

    if not results.empty:
        st.subheader("📋 Αποτελέσματα")

        for _, row in results.iterrows():
            # URLs με σωστό encoding
            wiki_url = "https://el.wikipedia.org/wiki/" + urllib.parse.quote(str(row["Disease"]).replace(" ", "_"))
            omim_url = "https://www.omim.org/search/?search=" + urllib.parse.quote(str(row["Disease_EN"]))

            st.markdown(
                f"""
                ### 🧬 {row['Disease']}
                - **Τύπος μετάλλαξης:** {row['MutationType']}
                - **Κληρονομικότητα:** {row['Inheritance']}
                - **Γονίδιο/Χρωμόσωμα:** {row['Gene/Chromosome']}
                - **Διάγνωση:** {row['Diagnostics']}
                - **Φαινότυπος:** {row['Phenotype']}
                - **Γονότυπος:** {row['Genotype']}

                🔗 [![Wikipedia](https://img.shields.io/badge/Wikipedia-Διάβασε-0366d6?style=for-the-badge)]({wiki_url})
                🔗 [![OMIM](https://img.shields.io/badge/OMIM-Database-ff6600?style=for-the-badge)]({omim_url})
                """,
                unsafe_allow_html=True
            )
    else:
        st.warning("❌ Δεν βρέθηκαν αποτελέσματα.")
else:
    st.info("✏️ Πληκτρολόγησε μια λέξη-κλειδί για να ξεκινήσεις αναζήτηση.")




