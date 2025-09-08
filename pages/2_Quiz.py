# pages/2_Quiz.py
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
if "quiz_questions" not in st.session_state or len(st.session_state.quiz_questions) == 0:
    # δημιουργία σταθερού σετ ερωτήσεων με επιλογές
    sample_size = min(QUIZ_LENGTH, len(df))
    raw = random.sample(df.to_dict("records"), sample_size)
    st.session_state.quiz_questions = []
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

        # φτιάχνουμε 2 λανθασμένες επιλογές (αν υπάρχουν) + 1 σωστή
        if correct in pool:
            pool.remove(correct)
        wrong_count = min(2, len(pool))
        wrong_choices = random.sample(pool, k=wrong_count) if wrong_count > 0 else []
        choices = wrong_choices + [correct]
        random.shuffle(choices)

        st.session_state.quiz_questions.append({
            "disease": row.get("Disease", ""),
            "question": question,
            "correct": correct,
            "choices": choices
        })

if "quiz_q_index" not in st.session_state:
    st.session_state.quiz_q_index = 0
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "quiz_user_answers" not in st.session_state or len(st.session_state.quiz_user_answers) != len(st.session_state.quiz_questions):
    # αρχικοποίηση λίστας απαντήσεων (None = ανέπαφη)
    st.session_state.quiz_user_answers = [None] * len(st.session_state.quiz_questions)

# -----------------------------
# Έλεγχος αν τελείωσε το quiz
# -----------------------------
if st.session_state.quiz_q_index >= len(st.session_state.quiz_questions):
    total = len(st.session_state.quiz_questions)
    score = st.session_state.quiz_score
    st.success(f"📊 Τελικό σκορ: {score}/{total}")

    # Αξιολόγηση αποτελέσματος
    ratio = score / total if total > 0 else 0
    if ratio == 1:
        st.balloons()
        st.info("🌟 Άριστα! Έχεις κατανοήσει πλήρως το κεφάλαιο.")
    elif ratio >= 0.6:
        st.info("👍 Πολύ καλά! Μικρή επανάληψη και θα είσαι τέλειος/α.")
    else:
        st.warning("📚 Χρειάζεται περισσότερη μελέτη. Δοκίμασε ξανά!")

    # --- Εμφάνιση αναλυτικής λίστας απαντήσεων ---
    st.markdown("### Ανασκόπηση Απαντήσεων")
    rows = []
    for i, q in enumerate(st.session_state.quiz_questions):
        user_ans = st.session_state.quiz_user_answers[i]
        correct = q["correct"]
        ok = (user_ans == correct)
        rows.append({
            "Ερώτηση": q["question"],
            "Η απάντησή σου": user_ans if user_ans is not None else "(Δεν απαντήθηκε)",
            "Σωστή απάντηση": correct,
            "Αποτέλεσμα": "✅" if ok else "❌"
        })
    df_summary = pd.DataFrame(rows)
    st.dataframe(df_summary, use_container_width=True)

    # Επιπλέον: αναλυτικά expanders
    st.markdown("---")
    st.markdown("### Λεπτομέρειες (για κάθε ερώτηση)")
    for i, q in enumerate(st.session_state.quiz_questions):
        user_ans = st.session_state.quiz_user_answers[i]
        correct = q["correct"]
        ok = (user_ans == correct)
        with st.expander(f"Ερώτηση {i+1}: {q['disease']}"):
            st.write(q["question"])
            st.write(f"- **Η απάντησή σου:** {user_ans if user_ans is not None else '(Δεν απαντήθηκε)'}")
            st.write(f"- **Σωστή απάντηση:** {correct}")
            if ok:
                st.success("✅ Σωστή")
            else:
                st.error("❌ Λάθος")

    # Κουμπί για νέο quiz
    if st.button("🔄 Νέο Quiz"):
        st.session_state.quiz_questions = []
        st.session_state.quiz_q_index = 0
        st.session_state.quiz_score = 0
        st.session_state.quiz_user_answers = []
        st.rerun()

    st.stop()

# -----------------------------
# Τρέχουσα ερώτηση (interactive)
# -----------------------------
current = st.session_state.quiz_questions[st.session_state.quiz_q_index]
question = current["question"]
choices = current["choices"]
correct = current["correct"]

st.write(f"**Ερώτηση {st.session_state.quiz_q_index + 1}/{len(st.session_state.quiz_questions)}**")
st.write(question)

# Το radio έχει μοναδικό key ανά ερώτηση, ώστε να αποθηκεύεται τοπικά
radio_key = f"answer_{st.session_state.quiz_q_index}"
# Αν ο χρήστης έχει ήδη απαντήσει την τρέχουσα ερώτηση (π.χ. γύρισε πίσω), φορτώνουμε την προηγούμενη επιλογή
default = st.session_state.quiz_user_answers[st.session_state.quiz_q_index]
# Εφόσον το default μπορεί να είναι None, χειριζόμαστε το index σωστά
index = choices.index(default) if (default is not None and default in choices) else 0

answer = st.radio("Επέλεξε μία απάντηση:", choices, index=index, key=radio_key)

# -----------------------------
# Callback για υποβολή (χωρίς st.rerun() μέσα)
# -----------------------------
def submit_answer(index):
    sel = st.session_state.get(f"answer_{index}")
    # Αποθήκευση απάντησης
    st.session_state.quiz_user_answers[index] = sel
    # Ενημέρωση σκορ
    if sel == st.session_state.quiz_questions[index]["correct"]:
        st.session_state.quiz_score += 1
    # Μετάβαση στην επόμενη ερώτηση
    st.session_state.quiz_q_index += 1
    # **ΜΗ st.rerun() ΕΔΩ** — ο Streamlit θα rerun μετά την callback αυτόματα

st.button("Υποβολή", on_click=submit_answer, args=(st.session_state.quiz_q_index,))
