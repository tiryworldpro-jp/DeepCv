import os 
from pypdf import PdfReader
import pdfplumber


def cleaner_text(texte) :
    liste = texte.split()
    #J'ai rencontré un problème de taille, le pdf, en fonction de la mise en forme très variable
    #que peut utiliser un utilisateur, donne un résultat assez aléatoire avec PdfReader, la solution que j'ai trouvé
    #et qui coute un peu plus en temps de calcul, (et en mémoire) c'est de regarder si deux lettres orphelines
    #se suivent, alors c'est pas parfait et ça peut faire des erreurs mais c'est un bon compromis
    text_final = ""
    liste_final = list()
    mot_temp = ""
    for i in range(len(liste)) :
        if (len(liste[i]) <= 1) :
            mot_temp += liste[i]
        else :
            text_final += mot_temp + " "
            text_final += liste[i]
            mot_temp = ""
    return text_final[1:] + mot_temp

def cleaner_texte2(texte) :  #on laisse fct chunk gerer les sauts a la ligne, donc on les preserve
    if not texte:
        return ""
    return texte.strip()

def extraire_text_pdf(pdf_path) :

    if not os.path.exists(pdf_path) : # Test si le chemin du pdf est valide (sécurité)
        print("Chemin non valide")
        return None

    try :
        reader = PdfReader(pdf_path)
        text_final = ""

        for page in reader.pages :
            text = page.extract_text()
            if len(text) != 0 :
                text_final += text
        text_final2 = cleaner_text(text_final)

    except Exception as e :
        print("Erreur avec PdfReader")
        return None

    return text_final2


#Version avec pdfPlumber qui marche tellement mieux qu'avec PdfReader
def extraire_intelligent(pdf_object):
    texte_complet = ""
    with pdfplumber.open(pdf_object) as pdf:
        for page in pdf.pages:
            texte = page.extract_text(layout=True)
            if texte:
                texte_complet += texte + " "

    return cleaner_texte2(texte_complet)

if __name__ == "__main__":
    print("--------------")
    test_path = "../uploads/CV_Samy.pdf"

    text = extraire_text_pdf(test_path)
    print(text)
    with open("../uploads/CV_Samy.txt", "w", encoding="utf-8") as fichier:
        fichier.write(text)
    print("----------")