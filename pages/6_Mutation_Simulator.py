import streamlit as st

st.set_page_config(page_title="Mutation Simulator", layout="centered")
st.title("🧬 Mutation Simulator")
st.write("Παρατήρησε πώς οι μεταλλάξεις αλλάζουν τη μετάφραση DNA → πρωτεΐνη.")

# -------------------------------------------------
# ΓΕΝΕΤΙΚΟΣ ΚΩΔΙΚΑΣ (εκπαιδευτικός μικρός πίνακας)
# -------------------------------------------------

genetic_code = {
    "AUG":"Met", "GAA":"Glu", "UUU":"Phe", "CGA":"Arg",
    "AAU":"Asn", "UUC":"Phe", "GAU":"Asp",
    "UAA":"STOP", "UAG":"STOP", "UGA":"STOP"
}

original_dna = "ATGGAATTTCGATAA"

# -------------------------------------------------
# ΒΟΗΘΗΤΙΚΕΣ ΣΥΝΑΡΤΗΣΕΙΣ
# -------------------------------------------------

def dna_to_mrna(dna):
    return dna.replace("T", "U")

def split_codons(seq):
    return " ".join([seq[i:i+3] for i in range(0, len(seq), 3)])

def codon_list(seq):
    return [seq[i:i+3] for i in range(0, len(seq), 3)]

def translate(mrna):
    codons = codon_list(mrna)
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
# ΜΕΤΑΛΛΑΞΕΙΣ + ΘΕΣΗ ΜΕΤΑΛΛΑΞΗΣ
# -------------------------------------------------

def missense_mutation(dna):
    pos = 4
    mutated = dna[:pos] + "C" + dna[pos+1:]
    return mutated, pos

def nonsense_mutation(dna):
    pos = 6
    mutated = dna[:pos] + "TAA" + dna[pos+3:]
    return mutated, pos

def frameshift_mutation(dna):
    pos = 5
    mutated = dna[:pos] + dna[pos+1:]
    return mutated, pos

# -------------------------------------------------
# ΕΠΙΛΟΓΗ ΜΕΤΑΛΛΑΞΗΣ
# -------------------------------------------------

mutation_type = st.selectbox(
    "Επιλέξτε τύπο μετάλλαξης:",
    ["Καμία", "Missense", "Nonsense", "Frameshift"]
)

mutated_dna = original_dna
mutation_pos = None

if mutation_type == "Missense":
    mutated_dna, mutation_pos = missense_mutation(original_dna)
elif mutation_type == "Nonsense":
    mutated_dna, mutation_pos = nonsense_mutation(original_dna)
elif mutation_type == "Frameshift":
    mutated_dna, mutation_pos = frameshift_mutation(original_dna)

# -------------------------------------------------
# ΜΕΤΑΦΡΑΣΗ
# -------------------------------------------------

original_mrna = dna_to_mrna(original_dna)
mutated_mrna = dna_to_mrna(mutated_dna)

original_protein = translate(original_mrna)
mutated_protein = translate(mutated_mrna)

# -------------------------------------------------
# ΕΜΦΑΝΙΣΗ DNA ΜΕ ΤΡΙΑΔΕΣ
# -------------------------------------------------

st.markdown("### 🔬 Σύγκριση αλληλουχιών")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Φυσιολογικό DNA")
    st.code(split_codons(original_dna))

with col2:
    st.subheader("Μεταλλαγμένο DNA")
    st.code(split_codons(mutated_dna))

# -------------------------------------------------
# ΕΜΦΑΝΙΣΗ mRNA & ΠΡΩΤΕΪΝΗΣ
# -------------------------------------------------

st.markdown("### 🧾 Έκφραση γονιδίου")

col1, col2 = st.columns(2)

with col1:
    st.write("mRNA:", split_codons(original_mrna))
    st.write("Πρωτεΐνη:", " - ".join(original_protein))

with col2:
    st.write("mRNA:", split_codons(mutated_mrna))
    st.write("Πρωτεΐνη:", " - ".join(mutated_protein))

# -------------------------------------------------
# ΕΠΙΣΤΗΜΟΝΙΚΗ ΕΞΗΓΗΣΗ
# -------------------------------------------------

st.markdown("### 📚 Ερμηνεία")

if mutation_type == "Missense":
    st.info("Η αντικατάσταση βάσης άλλαξε ένα κωδικόνιο → αλλαγή ενός αμινοξέος.")
elif mutation_type == "Nonsense":
    st.warning("Δημιουργήθηκε πρόωρο κωδικόνιο λήξης → μικρότερη πρωτεΐνη.")
elif mutation_type == "Frameshift":
    st.error("Η διαγραφή βάσης άλλαξε το πλαίσιο ανάγνωσης → πλήρης αλλαγή πρωτεΐνης.")
else:
    st.success("Χωρίς μετάλλαξη: φυσιολογική πρωτεΐνη.")
