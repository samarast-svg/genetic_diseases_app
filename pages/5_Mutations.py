import streamlit as st
import xml.etree.ElementTree as ET
import os

st.set_page_config(page_title="Mutations – Διερεύνηση", layout="centered")

st.title("🧬 Mutations – Διερεύνηση Γονιδιακών Μεταλλάξεων")
st.write(
    "Σε αυτή την ενότητα θα μελετήσεις διαφορετικούς τύπους γονιδιακών μεταλλάξεων. "
    "Διάβασε προσεκτικά το σενάριο, απάντησε στο ερώτημα και έλεγξε την απάντησή σου."
)

# ---------- ΦΟΡΤΩΣΗ XML ----------

MUTATIONS_FOLDER = "mutations"


def load_mutations(folder):
    mutations = []
    for file in sorted(os.listdir(folder)):
        if file.endswith(".xml"):
            path = os.path.join(folder, file)
            tree = ET.parse(path)
            root = tree.getroot()

            mutation = {
                "id": root.attrib.get("id"),
                "title": root.findtext("Metadata/Title"),
                "context": root.findtext("Context"),
                "question": root.findtext("Question"),
                "options": [
                    (opt.attrib["id"], opt.text)
                    for opt in root.findall("Options/Option")
                ],
                "correct": root.findtext("CorrectAnswer"),
                "general_feedback": root.findtext("Feedback/General"),
                "feedback": {
                    opt.attrib["id"]: opt.text
                    for opt in root.findall("Feedback/PerOption/Option")
                },
            }
            mutations.append(mutation)

    return mutations


mutations = load_mutations(MUTATIONS_FOLDER)

# ---------- SESSION STATE ----------

if "current_index" not in st.session_state:
    st.session_state.current_index = 0

if "answered" not in st.session_state:
    st.session_state.answered = False

if "selected_option" not in st.session_state:
    st.session_state.selected_option = None

# ---------- ΕΠΙΛΟΓΗ ΜΕΤΑΛΛΑΞΗΣ ----------

titles = [m["title"] for m in mutations]

selected_title = st.selectbox(
    "Επιλέξτε μετάλλαξη:",
    titles,
    index=st.session_state.current_index
)

current_index = titles.index(selected_title)
mutation = mutations[current_index]

st.session_state.current_index = current_index

st.markdown("---")

# ---------- ΠΑΡΟΥΣΙΑΣΗ ΜΕΤΑΛΛΑΞΗΣ ----------

st.subheader(mutation["title"])
st.markdown(f"**Σενάριο:** {mutation['context']}")
st.markdown(f"**Ερώτημα:** {mutation['question']}")

# ---------- ΕΠΙΛΟΓΕΣ ----------

options_dict = {opt_id: text for opt_id, text in mutation["options"]}

selected = st.radio(
    "Επιλέξτε απάντηση:",
    options=list(options_dict.keys()),
    format_func=lambda x: options_dict[x],
    disabled=st.session_state.answered
)

# ---------- ΕΛΕΓΧΟΣ ΑΠΑΝΤΗΣΗΣ ----------

if st.button("Έλεγχος απάντησης") and not st.session_state.answered:
    st.session_state.selected_option = selected
    st.session_state.answered = True

if st.session_state.answered:
    st.markdown("---")

    if st.session_state.selected_option == mutation["correct"]:
        st.success("✔️ Σωστή απάντηση")
    else:
        st.error("❌ Λάθος απάντηση")

    st.info(mutation["general_feedback"])
    st.write(mutation["feedback"][st.session_state.selected_option])

    # ---------- ΕΠΟΜΕΝΗ ΜΕΤΑΛΛΑΞΗ ----------

    if current_index < len(mutations) - 1:
        if st.button("➡️ Επόμενη μετάλλαξη"):
            st.session_state.current_index += 1
            st.session_state.answered = False
            st.session_state.selected_option = None
            st.experimental_rerun()
    else:
        st.success("🎉 Ολοκλήρωσες όλες τις μεταλλάξεις!")
