#!/bin/env python3

from glob import glob
import os
from os import path
import sys

class Trier():
    """
    Cette classe trie les fichiers dans un dossier donne en argument.
    Il crée 1 liste dans laquelle se trouve tous les fichiers pdf et une autre liste
    dans laquelle se trouve tous les fichiers epub du dossier donné en argument.
    """
    def __init__(self,dossier):
        self.dossier=dossier
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
    
    pass

class Pdf():
    """
    Cette classe extrait le titre, le nom de l'auteur et le table de matière du fichier pdf donne en argument.
    Il retourne un liste contenant ces informations : titre,auteur,[table des matières]
    """
    def __init__(self,fichier):
        self.fichier=fichier
    pass

class Epub():
    """
    Cette classe extrait le titre, le nom de l'auteur et le table de matière du fichier epub donne en argument.
    Il retourne un liste contenant ces informations : titre,auteur,[table des matières]
    """
    def __init__(self,fichier):
        self.fichier=fichier
    pass

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

