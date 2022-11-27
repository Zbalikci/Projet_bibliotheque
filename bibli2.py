import glob
import os
import sys
import PyPDF2 # pour pouvoir l'utiliser : pip install PyPDF2
from PyPDF2 import PdfReader 
import ebooklib # pour pouvoir l'utiliser : pip install ebooklib
from ebooklib import epub 
from bs4 import BeautifulSoup
from pikepdf import Pdf


class Trier():
    """
    Cette classe trie les fichiers dans un dossier donne en argument.
    Il crée 1 liste dans laquelle se trouve tous les fichiers pdf et une autre liste
    dans laquelle se trouve tous les fichiers epub du dossier donné en argument.
    """
    def __init__(self,dossier):
        self.dossier=glob.glob(os.path.join(dossier,"*"))
        self.DocumentsPDF=[]
        self.DocumentsEpub=[]
        self.DocumentsZip=[]
        self.DocumentsAutres=[]
        for doc in self.dossier:
            nature=(os.path.splitext(doc)[1])
            if nature =='.pdf':
                self.DocumentsPDF.append(doc)
            if nature =='.epub':
                self.DocumentsEpub.append(doc)
            if nature =='.zip':
                self.DocumentsZip.append(doc)
            if nature == '':
                self.DocumentsAutres.append(doc)
    
    def __str__(self):
        return f"Il y a {len(self.DocumentsPDF)+len(self.DocumentsEpub)+len(self.DocumentsZip)+len(self.DocumentsAutres)} fichiers dans ce dossier"
    def __repr__(self):
        return f"Il y a {len(self.DocumentsPDF)+len(self.DocumentsEpub)+len(self.DocumentsZip)+len(self.DocumentsAutres)} fichiers dans ce dossier"

class PDF():
    """
    Cette classe extrait le titre, le nom de l'auteur et le table de matière du fichier pdf donne en argument.
    """
    def __init__(self,chemin_fichier):
        self.fichier= chemin_fichier
        livre = PdfReader(self.fichier)
        donnees = livre.getDocumentInfo()
        self.auteur = donnees.author if donnees.author else u'Inconnu'
        self.titre = donnees.title if donnees.title else self.fichier

    def __str__(self):
        return f"{self.titre} de {self.auteur}"
    
    def __repr__(self):
        return f"{self.titre} de {self.auteur}"
    
    def toc(self):
        with Pdf.open(self.fichier) as f:
              outline = f.open_outline()
              print(outline)
              for title in outline.root:
                  print(title)
                  for subtitle in title.children:
                      print('\t', subtitle)
    # nouvelle fonction toc qui marche un peu
class Epub():
    """
    Cette classe extrait le titre, le nom de l'auteur et le table de matière du fichier epub donne en argument.
    """
    def __init__(self,chemin_fichier):
        self.fichier=chemin_fichier
        livre = epub.read_epub(self.fichier)
        self.auteur=livre.get_metadata('DC', 'creator')[0][0]
        self.titre=livre.get_metadata('DC', 'title')[0][0]
        
    def toc(self):
        book = epub.read_epub(self.fichier)
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_NAVIGATION:
                soup = BeautifulSoup(item.get_content(), 'html.parser')
        toc = soup.get_text()
        return toc.replace('\n\n\n\n',"")

    def __str__(self):
        return f"{self.titre} de {self.auteur}"
    
    def __repr__(self):
        return f"{self.titre} de {self.auteur}"

class Livres():
    """
    Cette classe crée une liste contenant le titre et l'auteur de chaque livre : [[titre,auteur],[titre,auteur],....].
    """
    def __init__(self,liste_fichiers):
        self.livres=[]
        self.liste_fichiers=liste_fichiers
        for fichier in self.liste_fichiers:
            nature=(os.path.splitext(fichier)[1])
            if nature =='.pdf':
                livre=Pdf(fichier)
                self.livres.append([livre.titre,livre.auteur])
            if nature =='.epub':
                livre=Epub(fichier)
                self.livres.append([livre.titre,livre.auteur])
                
    def __str__(self):
        return "\n".join([str(c) for c in self.livres])
    
    def __repr__(self):
        return "\n".join([str(c) for c in self.livres])
    
