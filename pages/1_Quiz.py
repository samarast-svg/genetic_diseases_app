import streamlit as st
import pandas as pd
import random

# Ρυθμίσεις σελίδας
st.set_page_config(
    page_title="Quiz – Γενετικές Ασθένειες",
    page_icon="🧪",
    layout="centered"
)

QUIZ_LENGTH = 5  # αριθμός ερωτήσεων ανά quiz

# -----------------------------
# Φόρτωση δεδομένων
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("genetic_diseases_lykeio_full_en.csv")

df = load_data()

st.title("🧪 Quiz – Γενετικές Ασθένειες")
st.markdown("Απάντησε στις ερωτήσεις για να ελέγξεις τις γνώσεις σου!")

# -----------------------------
# Αρχικοποίηση state
# -----------------------------
if "score" not in st.session_state:
    st.session_state.score = 0
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "questions" not in st.session_state or len(st.session_state.questions) == 0:
    # δημιουργία σταθερού σετ ερωτήσεων με επιλογές
    raw = random.sample(df.to_dict("records"), min(QUIZ_LENGTH, len(df)))
    st.session_state.questions = []
    for row in raw:
        q_type = random.choice(["inheritance", "mutation"])
        if q_type == "inheritance":
            question = f"Ποια είναι η μορφή κληρονομικότητας της ασθένειας **{row['Disease']}**;"
            correct = str(row["Inheritance"])
            pool = df["Inheritance"].dropna().astype(str).unique().tolist()
        else:
            question = f"Ποιος είναι ο τύπος μετάλλαξης που σχετίζεται με την ασθένεια **{row['Disease']}**;"
            correct = str(row["MutationType"])
            pool = df["MutationType"].dropna().astype(str).unique().tolist()

        if correct in pool:
            pool.remove(correct)
        choices = random.sample(pool, k=min(2, len(pool))) + [correct]
        random.shuffle(choices)

        st.session_state.questions.append({
            "question": question,
            "correct": correct,
            "choices": choices
        })

# -----------------------------
# Έλεγχος αν τελείωσε το quiz
# -----------------------------
if st.session_state.q_index >= len(st.session_state.questions):
    st.success(f"📊 Τελικό σκορ: {st.session_state.score}/{len(st.session_state.questions)}")
    
    # Αξιολόγηση αποτελέσματος
    ratio = st.session_state.score / len(st.session_state.questions)
    if ratio == 1:
        st.balloons()
        st.info("🌟 Άριστα! Έχεις κατανοήσει πλήρως το κεφάλαιο.")
    elif ratio >= 0.6:
        st.info("👍 Πολύ καλά! Μικρή επανάληψη και θα είσαι τέλειος/α.")
    else:
        st.warning("📚 Χρειάζεται περισσότερη μελέτη. Δοκίμασε ξανά!")

    if st.button("🔄 Νέο Quiz"):
        st.session_state.score = 0
        st.session_state.q_index = 0
        st.session_state.questions = []
        st.rerun()
    st.stop()

# -----------------------------
# Τρέχουσα ερώτηση
# -----------------------------
current = st.session_state.questions[st.session_state.q_index]
question, correct, choices = current["question"], current["correct"], current["choices"]

st.write(f"**Ερώτηση {st.session_state.q_index+1}/{len(st.session_state.questions)}**")
st.write(question)

answer = st.radio("Επέλεξε μία απάντηση:", choices, key=f"answer_{st.session_state.q_index}")

# -----------------------------
# Κουμπί υποβολής
# -----------------------------
if st.button("Υποβολή"):
    if answer == correct:
        st.success("✅ Σωστό!")
        st.session_state.score += 1
    else:
        st.error(f"❌ Λάθος! Σωστή απάντηση: **{correct}**")
    st.session_state.q_index += 1
    st.rerun()

