#!/bin/env python3
import glob
import os
import sys
import PyPDF2 # pour pouvoir l'utiliser : pip install PyPDF2
from PyPDF2 import PdfReader 
import ebooklib # pour pouvoir l'utiliser : pip install ebooklib
from ebooklib import epub 
from bs4 import BeautifulSoup #pour convertir HTML en STR
from pikepdf import Pdf
import fitz  # pour pouvoir l'utiliser : pip install PyMuPDF
import langdetect # pour pouvoir l'utiliser : pip install langdetect
from langdetect import detect 

class Trier():
    """
    Cette classe trie les fichiers dans un dossier donne en argument. Il crée 1 liste dans laquelle se trouve tous les fichiers pdf
    et une autre liste dans laquelle se trouve tous les fichiers epub du dossier donné en argument.
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
    Cette classe extrait le titre,le nombre de pages le nom de l'auteur, le langage et le table de matière du fichier pdf donne en argument.
    """
    def __init__(self,chemin_fichier):
        self.fichier= chemin_fichier
        livre = PdfReader(self.fichier)
        donnees = livre.getDocumentInfo()
        self.auteur = donnees.author if donnees.author else u'Inconnu'
        self.titre = donnees.title if donnees.title else self.fichier
        try:
            self.pages= len(livre.pages)
        except :
            self.pages=0
        if self.pages>4:
            page = livre.pages[4]
            text = page.extract_text()
            try:
                self.langage=detect(text)
            except:
                self.langage='Inconnu'
        else :
            self.langage='Inconnu'
        
        
    def __str__(self):
        return f"{self.titre} de {self.auteur}"
    
    def __repr__(self):
        return f"{self.titre} de {self.auteur}"
    
    # l'ancienne :
    # def toc(self):
    #     if self.pages>=2:
    #         with open(self.fichier,'rb') as f:
    #             pdf = PdfReader(f)
    #             page = pdf.getPage(1)
    #             text = page.extractText()
    #             return text
    # le nouveau :
    
    def toc(self):
        livre = fitz.open(self.fichier)
        return livre.get_toc()

class Epub():
    """
    Cette classe extrait le titre, le nom de l'auteur, le langage et le table de matière du fichier epub donne en argument.
    """
    def __init__(self,chemin_fichier):
        self.fichier=chemin_fichier
        livre = epub.read_epub(self.fichier)
        self.auteur=livre.get_metadata('DC', 'creator')[0][0]
        self.titre=livre.get_metadata('DC', 'title')[0][0]
        self.langage=livre.get_metadata('DC', 'language')[0][0]
        
        #ou bien :
        # self.titre=livre.metadata['title']
        # self.langage=livre.metadata['author']
        
        livre = fitz.open(self.fichier)
        self.pages=livre.page_count
        
    def toc(self):
        book = epub.read_epub(self.fichier)
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_NAVIGATION:
                soup = BeautifulSoup(item.get_content(), features="xml")
        toc = soup.get_text()
        return toc.replace('\n\n\n\n',"")
    #ou bien :
    # def toc(self):
        # livre = fitz.open(self.fichier)
        # return .get_toc()

    def __str__(self):
        return f"{self.titre} de {self.auteur}"
    
    def __repr__(self):
        return f"{self.titre} de {self.auteur}"

class Livres():
    """
    Cette classe crée une liste contenant le titre, l'auteur et le langage de chaque livre :
    [ [titre,auteur,langage], [titre,auteur,langage] , ....].
    """
    def __init__(self,liste_fichiers):
        self.livres=[]
        self.liste_fichiers=liste_fichiers
        for fichier in self.liste_fichiers:
            nature=(os.path.splitext(fichier)[1])
            if nature =='.pdf':
                livre=PDF(fichier)
                self.livres.append([livre.titre,livre.auteur,livre.langage])
            if nature =='.epub':
                livre=Epub(fichier)
                self.livres.append([livre.titre,livre.auteur,livre.langage])
                
    def __str__(self):
        return "\n".join([str(c) for c in self.livres])
    
    def __repr__(self):
        return "\n".join([str(c) for c in self.livres])
    
    def __iter__(self):
        return iter(self.livres)

    def __getitem__(self,i):
        return self.livres[i]
    
#"\n".join([str(c) for c in self.livres])

class Rapport():
    """
    Cette classe crée 3 documents (pdf,epub,txt) contenant le nom de chaque auteur des livres et crée 3 autres
    documents (pdf,epub,txt) contenant le titre de chaque livre.
    3 documents contenant : [ [auteur, (livre1,livre2,...)] , [auteur, (livre1,livre2,...)] , ... ]
    3 autres documents contenant : [ [titre,auteur,langage], [titre,auteur,langage] , ....].
    
    """
    # Ma classe n'est pas complète et ça ne marche pas bien , mais voici l'idée que jai :
    def __init__(self, dossier):
        
        livresPDF=Trier(dossier).DocumentsPDF #liste des livres pdf (avec le chemin des fichiers)
        livresEpub=Trier(dossier).DocumentsEpub #liste des livres epub (avec le chemin des fichiers)
        
        self.rapport=Livres(livresEpub).livres #liste des livres : [ [titre, auteur, langage] , ... ]
        for livre in Livres(livresPDF).livres:
            self.rapport.append(livre)

        with open("rapport.txt","w") as f :
            f.write("Livre 1 : \n Le titre : "+self.rapport[0][0])
        with open("rapport.txt","a+") as f :
            f.write("\n L'auteur : "+self.rapport[0][1])
            f.write("\n Le langage : "+self.rapport[0][2])

    def __str__(self):
        return "\n".join([str(c) for c in self.rapport])
    
    def __repr__(self):
        return "\n".join([str(c) for c in self.rapport]) 

    def __iter__(self):
        return iter(self.rapport) 

class ToC():
    """
    Cette classe crée 3 documents (pdf,epub,txt) contenant le table des matières des livres dans le dossier donne en argument.
    """
    pass

class MaS(): #Mise à jour des rapports
    """
    Cette classe doit mettre à jour (sans tout regénérer) les rapports précédemment générés, 
    en tenant compte de l’état présent de la bibliothèque : générer les rapports des nouveaux livres, 
    modifier ceux correspondants à des livres qui ont été modifiés depuis la dernière génération, 
    et enfin supprimer les rapports des livres disparus.
    
    Chaque exécution d’une mise à jour consigne les opérations réalisées (créations, modifications et suppression) 
    dans un fichier de log.
    """
    pass
