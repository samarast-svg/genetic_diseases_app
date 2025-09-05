import streamlit as st
import pandas as pd
import random

# Ρυθμίσεις σελίδας
st.set_page_config(
    page_title="Quiz – Γενετικές Ασθένειες",
    page_icon="🧪",
    layout="centered"
)

QUIZ_LENGTH = 5  # άλλαξέ το αν θες περισσότερες/λιγότερες ερωτήσεις

# Φόρτωση δεδομένων (ίδιο CSV με την πρώτη σελίδα)
@st.cache_data
def load_data():
    return pd.read_csv("genetic_diseases_lykeio_full_en.csv")

df = load_data()

# --- αρχικοποίηση state ---
if "score" not in st.session_state:
    st.session_state.score = 0
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "questions" not in st.session_state:
    # φτιάχνουμε όλες τις ερωτήσεις με τις πιθανές απαντήσεις από την αρχή
    raw = random.sample(df.to_dict("records"), 5)
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

st.title("🧪 Quiz – Γενετικές Ασθένειες")
st.markdown("Απάντησε στις ερωτήσεις για να ελέγξεις τις γνώσεις σου!")

# --------- helpers ---------
def generate_question(row):
    """Δημιουργεί ερώτηση είτε για κληρονομικότητα είτε για τύπο μετάλλαξης."""
    q_type = random.choice(["inheritance", "mutation"])

    if q_type == "inheritance":
        question = f"Ποια είναι η μορφή κληρονομικότητας της ασθένειας **{row['Disease']}**;"
        correct = str(row["Inheritance"])
        pool = df["Inheritance"].dropna().astype(str).unique().tolist()
    else:
        question = f"Ποιος είναι ο τύπος μετάλλαξης που σχετίζεται με την ασθένεια **{row['Disease']}**;"
        correct = str(row["MutationType"])
        pool = df["MutationType"].dropna().astype(str).unique().tolist()

    # φτιάχνουμε 2 λανθασμένες επιλογές (αν υπάρχουν) + 1 σωστή
    wrong = [c for c in pool if c != correct]
    k = min(2, len(wrong))
    choices = random.sample(wrong, k) + [correct]
    random.shuffle(choices)
    return question, correct, choices

# --------- state ---------
if "score" not in st.session_state:
    st.session_state.score = 0
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "questions" not in st.session_state:
    st.session_state.questions = random.sample(df.to_dict("records"), 5)
if "quiz_q_index" not in st.session_state:
    st.session_state.quiz_q_index = 0
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "quiz_questions" not in st.session_state:
    sample_size = min(QUIZ_LENGTH, len(df))
    st.session_state.quiz_questions = random.sample(df.to_dict("records"), sample_size)
if "quiz_checked" not in st.session_state:
    st.session_state.quiz_checked = False
if "quiz_last_correct" not in st.session_state:
    st.session_state.quiz_last_correct = None

# --------- έλεγχος αν τελείωσε το quiz ---------
if st.session_state.q_index >= len(st.session_state.questions):
    st.success(f"📊 Τελικό σκορ: {st.session_state.score}/{len(st.session_state.questions)}")
    if st.button("🔄 Νέο Quiz"):
        st.session_state.score = 0
        st.session_state.q_index = 0
        st.session_state.questions = random.sample(df.to_dict("records"), 5)
    st.stop()  # σταματά την εκτέλεση εδώ

# --------- τρέχουσα ερώτηση ---------
current = st.session_state.questions[st.session_state.q_index]
question, correct, choices = generate_question(current)


st.write(f"**Ερώτηση {st.session_state.quiz_q_index + 1}/{len(st.session_state.quiz_questions)}**")
st.write(question)

answer = st.radio(
    "Επέλεξε μία απάντηση:",
    choices,
    key=f"quiz_answer_{st.session_state.quiz_q_index}",
    horizontal=False
)

col1, col2 = st.columns([1,1])

def check_answer():
    st.session_state.quiz_checked = True
    if answer == correct:
        st.session_state.quiz_last_correct = True
        st.session_state.quiz_score += 1
    else:
        st.session_state.quiz_last_correct = False

def next_question():
    st.session_state.quiz_checked = False
    st.session_state.quiz_last_correct = None
    st.session_state.quiz_q_index += 1

with col1:
    st.button("Έλεγχος", on_click=check_answer, disabled=st.session_state.quiz_checked)

with col2:
    st.button("Επόμενη", on_click=next_question, disabled=not st.session_state.quiz_checked)

# feedback
if st.session_state.quiz_checked:
    if st.session_state.quiz_last_correct:
        st.success("✅ Σωστό!")
    else:
        st.error(f"❌ Λάθος. Σωστή απάντηση: **{correct}**")

# --------- έλεγχος αν τελείωσε το quiz ---------
if st.session_state.q_index >= len(st.session_state.questions):
    st.success(f"📊 Τελικό σκορ: {st.session_state.score}/{len(st.session_state.questions)}")
    if st.button("🔄 Νέο Quiz"):
        st.session_state.score = 0
        st.session_state.q_index = 0
        st.session_state.questions = []  # θα ξαναδημιουργηθούν με refresh
        st.experimental_rerun()
    st.stop()

# --------- τρέχουσα ερώτηση ---------
current = st.session_state.questions[st.session_state.q_index]
question, correct, choices = current["question"], current["correct"], current["choices"]

st.write(f"**Ερώτηση {st.session_state.q_index+1}/{len(st.session_state.questions)}**")
st.write(question)

answer = st.radio("Επέλεξε μία απάντηση:", choices, key=f"q{st.session_state.q_index}")
