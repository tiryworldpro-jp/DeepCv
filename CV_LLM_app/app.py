import os
from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename

from services.vectorizer_de_text import vectoriser_liste_text, calculer_scores_bdd, vectoriser_text, note_final_bdd
from services.pdf_parser import extraire_intelligent
from services.cosinus_similarity import pertinence
from services.chunking import fct_de_chunk

app = Flask(__name__)

BDD_GLOBALE = []
TEXTES_COMPLETS_GLOBAUX = {}

@app.route('/')
def accueil():
    return render_template("accueil.html")

@app.route('/reset', methods=['POST'])
def reset_memoire():
    global BDD_GLOBALE, TEXTES_COMPLETS_GLOBAUX
    BDD_GLOBALE = []
    TEXTES_COMPLETS_GLOBAUX = {}
    print("Mémoire vidée !")
    return jsonify({'message': 'Mémoire vidée'})

@app.route('/analyse', methods=['POST'])
def analyse_cv():
    global BDD_GLOBALE, TEXTES_COMPLETS_GLOBAUX
    user_prompt = request.form.get('prompt', '')
    vecteur_prompt = vectoriser_text(user_prompt)
    files = request.files.getlist('cv')
    nouveaux_fichiers_traites = 0

    for file in files:
        if file.filename == '' : continue
        filename = secure_filename(file.filename)
        if filename in TEXTES_COMPLETS_GLOBAUX:
            continue
        text_extrait = extraire_intelligent(file)
        if text_extrait:
            TEXTES_COMPLETS_GLOBAUX[filename] = text_extrait
            chunks = fct_de_chunk(text_extrait, taille=30, mode="mots", tag="", overlap=5)
            vectoriser_liste_text(chunks, filename, BDD_GLOBALE)
            nouveaux_fichiers_traites += 1
        else:
            continue
    if not BDD_GLOBALE:
        return jsonify({'error': 'Aucun fichier en mémoire. Envoyez des CVs !'}), 400
    calculer_scores_bdd(BDD_GLOBALE, vecteur_prompt)
    note_final_bdd(BDD_GLOBALE)
    data_pour_le_front = []
    vus = set()
    for ligne in BDD_GLOBALE :
        nom = ligne['nomFichier']
        if nom not in vus:
            texte_entier = TEXTES_COMPLETS_GLOBAUX.get(nom, 'null')
            data_pour_le_front.append({
                'nom_fichier': ligne['nomFichier'],
                'meilleur_extrait': ligne['texte'],
                'pertinence': ligne['score'],
                'texte_fichier': texte_entier
            })
            vus.add(ligne['nomFichier'])

    return jsonify({
        'message': 'Analyse terminée',
        'count' : len(data_pour_le_front),
        'data' : data_pour_le_front
    })

if __name__ == '__main__':
    app.run(debug=True)