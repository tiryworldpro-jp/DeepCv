import re
from transformers import AutoTokenizer

TOKENIZER = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

def fct_de_chunk(texte, taille=50, mode="mots", tag="", overlap = 10):
    if not texte:
        return []

    elements = []

    if mode == "lignes":
        # on coupe aux sauts de ligne
        lignes_brutes = re.split(r"\r?\n+", texte.strip())
        elements = [re.sub(r"\s+", " ", l).strip() for l in lignes_brutes if l.strip()]
    elif mode == "mots":
        # on coupe à chaque espace
        elements = texte.split()
    else:
        print(f"Mode '{mode}' inconnu, passage en mode mots par défaut")
        elements = texte.split()

    resultat_final = []    

    for j in range(0, taille, overlap) :
        for i in range(j, len(elements), taille):
            groupe = elements[i : i + taille]
            bloc_texte = " ".join(groupe)

            if tag:
                bloc_texte = f"{tag} {bloc_texte}"

            resultat_final.append(bloc_texte)

    return resultat_final


