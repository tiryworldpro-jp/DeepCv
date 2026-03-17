import numpy as np

def norme_euclidienne(vecteur):
    return np.linalg.norm(vecteur)

def produit_Scalaire(vecteur1, vecteur2):
    if len(vecteur1) != len(vecteur2):
        return 0
    produi_scalaire = 0
    for i in range(len(vecteur1)):
        produi_scalaire += vecteur1[i] * vecteur2[i]
    return produi_scalaire


def cosinus_similarity(vecteur1, vecteur2) :
    produit_scalaire = produit_Scalaire(vecteur1, vecteur2)
    norme_euclidienne1 = norme_euclidienne(vecteur1)
    norme_euclidienne2 = norme_euclidienne(vecteur2)

    if norme_euclidienne1 == 0 or norme_euclidienne2==0 :
        return 0

    return produit_scalaire/(norme_euclidienne1*norme_euclidienne2)


def pertinence(vecteur1, vecteur2) :
    cosinus_similarite = cosinus_similarity(vecteur1, vecteur2)
    if cosinus_similarite < 0 :
        return 0
    else :
        return cosinus_similarite*100