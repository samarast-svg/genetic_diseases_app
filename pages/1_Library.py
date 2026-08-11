import streamlit as st
import pandas as pd
import urllib.parse

# -------------------------------------------------
# ΡΥΘΜΙΣΕΙΣ ΣΕΛΙΔΑΣ
# -------------------------------------------------

st.set_page_config(
    page_title="Γενετικές Ασθένειες – Βιολογία Γ’ Λυκείου",
    page_icon="🧬",
    layout="centered"
)

# -------------------------------------------------
# ΦΟΡΤΩΣΗ DATASET
# -------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("genetic_diseases_lykeio_full_en.csv")


df = load_data()

# -------------------------------------------------
# ΤΙΤΛΟΣ
# -------------------------------------------------

st.title("🧬 Γενετικές Ασθένειες - Βιολογία Γ’ Λυκείου")

# -------------------------------------------------
# ΑΝΑΖΗΤΗΣΗ
# -------------------------------------------------

query = st.text_input(
    "🔎 Αναζήτηση ασθένειας ή λέξης-κλειδί:"
)

if query:

    results = df[
        df.apply(
            lambda row: row.astype(str).str.contains(
                query,
                case=False,
                na=False
            ).any(),
            axis=1
        )
    ]

    if not results.empty:

        st.subheader("📋 Αποτελέσματα")

        for _, row in results.iterrows():

            # URLs με σωστό encoding
            wiki_url = (
                "https://el.wikipedia.org/wiki/"
                + urllib.parse.quote(
                    str(row["Disease"]).replace(" ", "_")
                )
            )

            omim_url = (
                "https://www.omim.org/search/?search="
                + urllib.parse.quote(
                    str(row["Disease_EN"])
                )
            )

            st.markdown(
                f"""
### 🧬 {row['Disease']}

- **Τύπος μετάλλαξης:** {row['MutationType']}
- **Κληρονομικότητα:** {row['Inheritance']}
- **Γονίδιο/Χρωμόσωμα:** {row['Gene/Chromosome']}
- **Διάγνωση:** {row['Diagnostics']}
- **Φαινότυπος:** {row['Phenotype']}
- **Γονότυπος:** {row['Genotype']}

🔗 [Wikipedia]({wiki_url})

🔗 [OMIM]({omim_url})
""",
                unsafe_allow_html=True
            )

    else:
        st.warning("❌ Δεν βρέθηκαν αποτελέσματα.")

else:
    st.info(
        "✏️ Πληκτρολόγησε μια λέξη-κλειδί για να ξεκινήσεις αναζήτηση."
    )
