from sentence_transformers import SentenceTransformer
from services.cosinus_similarity import pertinence

model = SentenceTransformer('all-MiniLM-L6-v2')


def vectoriser_text(texte) :
    vecteur_cv = model.encode(texte)
    return vecteur_cv

def vectoriser_liste_text(chunks, nom_fichier, base_de_donnees) :
    liste_vecteurs = [vectoriser_text(chunk) for chunk in chunks]
    for chunk, vecteur in zip(chunks, liste_vecteurs) :
        donnee = {
            "nomFichier" : nom_fichier,
            "texte" : chunk,
            "vecteur" : vecteur
        }
        base_de_donnees.append(donnee)
    return base_de_donnees

def calculer_scores_bdd(base_de_donnee, prompt_vecteur) :
    for ligne in base_de_donnee :
        var_pertinence = int(pertinence(prompt_vecteur, ligne['vecteur']))
        ligne['score'] = var_pertinence

def note_final_bdd(base_de_donnee) :
    compteur_pertinence = {}
    compteur_chunk = {}
    for ligne in base_de_donnee :
        nom_fichier = ligne['nomFichier']
        if ligne['score'] > 50 :
            compteur_pertinence[nom_fichier] = compteur_pertinence.get(nom_fichier, 0) + 1
        compteur_chunk[nom_fichier] = compteur_chunk.get(nom_fichier, 0) + 1

    for ligne in base_de_donnee :
        nom_fichier = ligne['nomFichier']
        nb_passage_pertinent = compteur_pertinence.get(nom_fichier, 0)
        #nb_passage = compteur_chunk.get(nom_fichier, 0)
        facteur_boost = min(0.9, nb_passage_pertinent*0.10)
        ligne['score'] = ligne['score'] + (100 - ligne['score']) * facteur_boost
    base_de_donnee.sort(key=lambda x : x['score'], reverse = True)