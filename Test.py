#!/bin/env python3
import glob
import numpy as np
import os
from os import path
import sys

#################################### TEST POUR TROUVER LA FONCTION ####################################

dossier ="/users/2023/ds1/122003362/Téléchargements/livres"

#print(glob.glob("/users/2023/ds1/122003362/Téléchargements/livres/ze*"))

documents=glob.glob(os.path.join(dossier,"*"))
Nature=[]
#print(documents)
for doc in documents:
    nature=(os.path.splitext(doc)[1]) #le type de chaque fichier 
    Nature.append(nature)
    
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

####################################       on test le module       ####################################
from bibli import Trier

print(Trier(dossier))

#################################### TEST POUR TROUVER LA FONCTION ####################################
from PyPDF2 import PdfReader
from langdetect import detect # installer le module langdetect.

myFile="/users/2023/ds1/122003362/Téléchargements/livres/gide_immoraliste.pdf"

reader = PdfReader(myFile)
number_of_pages = len(reader.pages)
page = reader.pages[0]
text = page.extract_text()


metadata = reader.getDocumentInfo()

author = metadata.author if metadata.author else u'Unknown'
title = metadata.title if metadata.title else myFile


####################################       on test le module       ####################################
from bibli import PDF

livre = PDF(myFile)


#################################### TEST POUR TROUVER LA FONCTION ####################################

import ebooklib
import lxml
from ebooklib import epub
from ebooklib import utils

myFile2="/users/2023/ds1/122003362/Téléchargements/livres/zola_emile_-_l_assommoir.epub"

book = epub.read_epub(myFile2)


items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))

print(book.get_metadata('DC', 'creator')[0][0])
print(book.get_metadata('DC', 'title')[0][0])
print(book.get_metadata('DC', 'language')[0][0])


import re
from bs4 import BeautifulSoup

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

####################################       on test le module       ####################################
from bibli import Epub

livre2 = Epub(myFile2)
print(livre2)
print(livre2.toc())

####################################       on test le module       ####################################

Files1=Trier(dossier).DocumentsPDF
Files2=Trier(dossier).DocumentsEpub


for file in Files1:
    l=Pdf(file)
    print(l.toc())

for file in Files2:
    l=Epub(file)
    print(l.toc())
    #print(l.language)
    
    
####################################       on test le module       ####################################

from bibli import Livres


# Files1=Trier(dossier).DocumentsPDF
# Books1=Livres(Files1)
# print(Books1)

# Files2=Trier(dossier).DocumentsEpub
# Books2=Livres(Files2)
# print(Books2)
# print(type(Files1))
# print(len(Files1))

