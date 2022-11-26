#!/bin/env python3
import glob
import os
import sys
from PyPDF2 import PdfReader # pour pouvoir l'utiliser : pip install PyPDF2

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

class Pdf():
    """
    Cette classe extrait le titre, le nom de l'auteur et le table de matière du fichier pdf donne en argument.
    """
    def __init__(self,fichier):
        self.fichier= fichier
        reader = PdfReader(self.fichier)
        metadata = reader.getDocumentInfo()
        
        self.auteur = metadata.author if metadata.author else u'Inconnu'
        self.titre = metadata.title if metadata.title else self.fichier
        
    def __str__(self):
        return f"{self.titre} de {self.auteur}"
    
    def __repr__(self):
        return f"{self.titre} de {self.auteur}"

class Epub():
    """
    Cette classe extrait le titre, le nom de l'auteur et le table de matière du fichier epub donne en argument.
    """
    def __init__(self,fichier):
        self.fichier=fichier
        self.auteur=''
        self.titre=''
        
    def __str__(self):
        return f"{self.titre} de {self.auteur}"
    
    def __repr__(self):
        return f"{self.titre} de {self.auteur}"
    pass

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
    

class Rapport():
    """
    Cette classe crée 3 documents (pdf,epub,txt) contenant le nom de chaque auteur des livres et crée 3 autres
    documents (pdf,epub,txt) contenant le titre de chaque livre.
    3 documents contenant : [ [auteur, (livre1,livre2,...)] , [auteur, (livre1,livre2,...)] ,... ]
    3 autres documents contenant : [[titre,auteur],[titre,auteur],....].
    
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



