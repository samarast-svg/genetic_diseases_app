import streamlit as st

st.set_page_config(page_title="Mutation Simulator", layout="centered")

st.title("🧬 Mutation Simulator")
st.write("Δες πώς αλλάζει η πρωτεΐνη όταν συμβαίνουν μεταλλάξεις στο DNA.")

# -------------------------------------------------
# ΓΕΝΕΤΙΚΟΣ ΚΩΔΙΚΑΣ (μικρός πίνακας για διδακτική χρήση)
# -------------------------------------------------

genetic_code = {
    "AUG":"Met", "GAA":"Glu", "UUU":"Phe", "CGA":"Arg",
    "AAU":"Asn", "UUC":"Phe", "GAU":"Asp",
    "UAA":"STOP", "UAG":"STOP", "UGA":"STOP"
}

# Αρχική αλληλουχία (διδακτικά μικρή)
original_dna = "ATGGAATTTCGATAA"

# -------------------------------------------------
# ΣΥΝΑΡΤΗΣΕΙΣ
# -------------------------------------------------

def dna_to_mrna(dna):
    return dna.replace("T", "U")

def split_codons(seq):
    return [seq[i:i+3] for i in range(0, len(seq), 3)]

def translate(mrna):
    codons = split_codons(mrna)
    protein = []
    for codon in codons:
        if len(codon) < 3:
            break
        aa = genetic_code.get(codon, "?")
        protein.append(aa)
        if aa == "STOP":
            break
    return protein

# -------------------------------------------------
# ΜΕΤΑΛΛΑΞΕΙΣ
# -------------------------------------------------

def missense_mutation(dna):
    # αλλάζουμε 1 βάση
    return dna[:4] + "C" + dna[5:]

def nonsense_mutation(dna):
    # δημιουργούμε STOP (TAA)
    return dna[:6] + "TAA" + dna[9:]

def frameshift_mutation(dna):
    # διαγραφή βάσης
    return dna[:5] + dna[6:]

# -------------------------------------------------
# ΕΠΙΛΟΓΗ ΜΕΤΑΛΛΑΞΗΣ
# -------------------------------------------------

mutation_type = st.selectbox(
    "Επιλέξτε τύπο μετάλλαξης:",
    ["Καμία", "Missense", "Nonsense", "Frameshift"]
)

mutated_dna = original_dna

if mutation_type == "Missense":
    mutated_dna = missense_mutation(original_dna)
elif mutation_type == "Nonsense":
    mutated_dna = nonsense_mutation(original_dna)
elif mutation_type == "Frameshift":
    mutated_dna = frameshift_mutation(original_dna)

# -------------------------------------------------
# ΥΠΟΛΟΓΙΣΜΟΙ
# -------------------------------------------------

original_mrna = dna_to_mrna(original_dna)
mutated_mrna = dna_to_mrna(mutated_dna)

original_protein = translate(original_mrna)
mutated_protein = translate(mutated_mrna)

# -------------------------------------------------
# ΕΜΦΑΝΙΣΗ
# -------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.subheader("Φυσιολογικό")
    st.write("DNA:", original_dna)
    st.write("mRNA:", original_mrna)
    st.write("Πρωτεΐνη:", " - ".join(original_protein))

with col2:
    st.subheader("Μετάλλαξη")
    st.write("DNA:", mutated_dna)
    st.write("mRNA:", mutated_mrna)
    st.write("Πρωτεΐνη:", " - ".join(mutated_protein))
