#!/bin/env python3
import glob
import numpy as np
import os
from os import path
import sys
#################################### TEST POUR TROUVER LA FONCTION ####################################
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

####################################       on test le module       ####################################
from bibli import Trier

print(Trier(dossier))

#################################### TEST POUR TROUVER LA FONCTION ####################################
from PyPDF2 import PdfReader

myFile="C:/Users/Zeynep/Downloads/livres_2/gide_immoraliste.pdf"

reader = PdfReader(myFile)
number_of_pages = len(reader.pages)
page = reader.pages[0]
text = page.extract_text()

metadata = reader.getDocumentInfo()

author = metadata.author if metadata.author else u'Unknown'
title = metadata.title if metadata.title else myFile
print (author + "|" + title )

####################################       on test le module       ####################################
from bibli import Pdf

livre = Pdf("C:/Users/Zeynep/Downloads/livres_2/gide_immoraliste.pdf")
print(livre)

#################################### TEST POUR TROUVER LA FONCTION ####################################

import ebooklib
from ebooklib import epub

book = epub.read_epub("C:/Users/Zeynep/Downloads/livres_2/zola_emile_-_l_assommoir.epub")

items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))

print(book.get_metadata('DC', 'creator')[0][0])
print(book.get_metadata('DC', 'title')[0][0])


####################################       on test le module       ####################################

from bibli import Livres

Files1=Trier(dossier).DocumentsPDF
Books1=Livres(Files1)
print(Books1)

Files2=Trier(dossier).DocumentsEpub
Books2=Livres(Files2)
print(Books2)
