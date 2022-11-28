#!/bin/env python3
import glob
import numpy as np
import os
from os import path
import sys
import fitz  # pour pouvoir l'utiliser : pip install PyMuPDF
import langdetect # pour pouvoir l'utiliser : pip install langdetect
from langdetect import detect 

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

###################################      on test notre module      ###################################
from bibli import Trier

print(Trier(dossier))

#################################### TEST POUR TROUVER LA FONCTION ####################################
from PyPDF2 import PdfReader

myFile="C:/Users/Zeynep/Downloads/livres_2/gide_immoraliste.pdf"

reader = PdfReader(myFile)
number_of_pages = len(reader.pages)
page = reader.pages[0]
text = page.extract_text()
print("la langue du fichier est en :" ,detect(text)) # detect ne marche que pour un bout de texte.
metadata = reader.getDocumentInfo()

author = metadata.author if metadata.author else u'Unknown'
title = metadata.title if metadata.title else myFile
print (author + "|" + title )

# un autre choix de module :

# doc = fitz.open(myFile)
# doc.get_toc()
# doc.metadata['title']
# doc.metadata['author']
# doc.page_count

###################################      on test notre module      ###################################
from bibli import PDF

livre = PDF(myFile)
print(livre)
print(livre.toc())

#################################### TEST POUR TROUVER LA FONCTION ####################################
import ebooklib
from ebooklib import epub

myFile2="C:/Users/Zeynep/Downloads/livres_2/zola_emile_-_l_assommoir.epub"

book = epub.read_epub(myFile2)


items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))

print(book.get_metadata('DC', 'creator')[0][0])
print(book.get_metadata('DC', 'title')[0][0])
print(book.get_metadata('DC', 'language')[0][0])

# un autre choix de module :

# doc = fitz.open(myFile2)
# doc.get_toc()
# doc.metadata['title']
# doc.metadata['author']
# doc.page_count

#pour obtenir le table des matières (ne donne pas le page des chapitres):
from bs4 import BeautifulSoup #pour convertir HTML en STR

def item_to_str(item):
    soup = BeautifulSoup(item.get_content(), features="xml")
    toc = soup.get_text()
    return toc.replace('\n\n\n\n',"")


for item in book.get_items():
    if item.get_type() == ebooklib.ITEM_NAVIGATION:
        print('==================================')
        print('NAME : ', item.get_name())
        print('==================================')
        print(item_to_str(item))

###################################      on test notre module      ###################################
from bibli import Epub

livre2 = Epub(myFile2)
print(livre2)
print(livre2.toc())

###################################      on test notre module      ###################################
Files1=Trier(dossier).DocumentsPDF
Files2=Trier(dossier).DocumentsEpub

for file in Files1:
    l=PDF(file)
    print(l.toc())


for file in Files2:
    l=Epub(file)
    print(l.toc())
    
####################################       on test le module       ####################################
from bibli import Livres

Files1=Trier(dossier).DocumentsPDF
Books1=Livres(Files1)
print(Books1)

Files2=Trier(dossier).DocumentsEpub
Books2=Livres(Files2)
print(Books2)
