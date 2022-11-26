#!/bin/env python3
import glob
import numpy as np
import os
from os import path
import sys

dossier ="C:/Users/Zeynep/Downloads/livres"

#print(glob.glob("C:/Users/Zeynep/Downloads/livres/ze*"))

documents=glob.glob(os.path.join(dossier,"*"))
Nature=[]
#print(documents)
for doc in documents:
    nature=(os.path.splitext(doc)[1]) #le type de chaque fichier 
    Nature.append(nature)
    
#print(Nature)
print(np.unique(Nature)) #affiche les types de documents

DocumentsPDF=[]
DocumentsEpub=[]
DocumentsZip=[]
DocumentsAutres=[]

#on trie par type de fichier
for doc in documents:
    nature=(os.path.splitext(doc)[1])
    if nature =='.pdf':
        DocumentsPDF.append(doc)
    if nature =='.epub':
        DocumentsEpub.append(doc)
    if nature =='.zip':
        DocumentsZip.append(doc)
    if nature == '':
        DocumentsAutres.append(doc)
        
print(len(DocumentsPDF)+len(DocumentsEpub)+len(DocumentsZip)+len(DocumentsAutres)) #doit afficher 4323