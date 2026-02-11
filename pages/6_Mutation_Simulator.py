import streamlit as st

st.set_page_config(page_title="Mutation Simulator", layout="centered")
st.title("🧬 Mutation Simulator")
st.write("Παρατήρησε πώς οι μεταλλάξεις αλλάζουν τη μετάφραση DNA → πρωτεΐνη.")

# -------------------------------------------------
# ΓΕΝΕΤΙΚΟΣ ΚΩΔΙΚΑΣ (εκπαιδευτικός μικρός πίνακας)
# -------------------------------------------------

genetic_code = {
    "UUU":"Phe","UUC":"Phe","UUA":"Leu","UUG":"Leu",
    "UCU":"Ser","UCC":"Ser","UCA":"Ser","UCG":"Ser",
    "UAU":"Tyr","UAC":"Tyr","UAA":"STOP","UAG":"STOP",
    "UGU":"Cys","UGC":"Cys","UGA":"STOP","UGG":"Trp",

    "CUU":"Leu","CUC":"Leu","CUA":"Leu","CUG":"Leu",
    "CCU":"Pro","CCC":"Pro","CCA":"Pro","CCG":"Pro",
    "CAU":"His","CAC":"His","CAA":"Gln","CAG":"Gln",
    "CGU":"Arg","CGC":"Arg","CGA":"Arg","CGG":"Arg",

    "AUU":"Ile","AUC":"Ile","AUA":"Ile","AUG":"Met",  # start codon
    "ACU":"Thr","ACC":"Thr","ACA":"Thr","ACG":"Thr",
    "AAU":"Asn","AAC":"Asn","AAA":"Lys","AAG":"Lys",
    "AGU":"Ser","AGC":"Ser","AGA":"Arg","AGG":"Arg",

    "GUU":"Val","GUC":"Val","GUA":"Val","GUG":"Val",
    "GCU":"Ala","GCC":"Ala","GCA":"Ala","GCG":"Ala",
    "GAU":"Asp","GAC":"Asp","GAA":"Glu","GAG":"Glu",
    "GGU":"Gly","GGC":"Gly","GGA":"Gly","GGG":"Gly"
}

st.markdown("### ✏️ Δώσε δική σου αλληλουχία DNA")

user_dna = st.text_input(
    "Εισάγετε DNA (μόνο A, T, G, C):",
    value="ATGGAATTTCGATAA"
)

# καθαρισμός εισόδου
user_dna = user_dna.upper().replace(" ", "")

valid_bases = set("ATGC")

if set(user_dna).issubset(valid_bases) and len(user_dna) >= 6:
    original_dna = user_dna
else:
    st.error("Η αλληλουχία πρέπει να περιέχει μόνο A, T, G, C και να έχει μήκος ≥ 6.")
    st.stop()


# -------------------------------------------------
# ΒΟΗΘΗΤΙΚΕΣ ΣΥΝΑΡΤΗΣΕΙΣ
# -------------------------------------------------

def dna_to_mrna(dna):
    return dna.replace("T", "U")

def split_codons(seq):
    return " ".join([seq[i:i+3] for i in range(0, len(seq), 3)])

def codon_list(seq):
    return [seq[i:i+3] for i in range(0, len(seq), 3)]

def translate_rna(mrna):
    codons = [mrna[i:i+3] for i in range(0, len(mrna), 3)]
    
    protein = []
    started = False
    
    for codon in codons:
        if len(codon) < 3:
            break
        
        # ξεκινάμε από START codon
        if codon == "AUG":
            started = True
        
        if not started:
            continue
        
        aa = genetic_code.get(codon, "?")
        
        if aa == "STOP":
            protein.append("STOP")
            break
        
        protein.append(aa)
    
    return codons, protein

def classify_mutation(original_protein, mutated_protein, mutation_type):
    
    if original_protein == mutated_protein:
        return "Silent mutation 🟢"

    if mutated_protein == "":
        return "No protein produced 🔴"

    if "*" in mutated_protein[:-1]:
        return "Nonsense mutation 🔴"

    if len(original_protein) != len(mutated_protein):
        return "Frameshift mutation 🟠"

    return "Missense mutation 🟡"

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

original_codons, original_protein = translate_rna(original_mrna)
mutated_codons, mutated_protein = translate_rna(mutated_mrna)

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

mutation_result = classify_mutation(
    original_protein,
    mutated_protein,
    mutation_choice = st.selectbox, (
    "Επίλεξε τύπο μετάλλαξης",
    ["Substitution", "Insertion", "Deletion"]
)
st.subheader("Αποτέλεσμα μετάλλαξης")
st.success(mutation_result)
    
)

st.markdown("## 🧬 Τύπος μετάλλαξης")
st.success(mutation_result)

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
