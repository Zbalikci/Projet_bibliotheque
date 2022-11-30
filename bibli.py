#!/bin/env python3
import glob
import os 
from PyPDF2 import PdfReader # pour pouvoir l'utiliser : pip install PyPDF2
import ebooklib # pour pouvoir l'utiliser : pip install ebooklib
from ebooklib import epub 
from bs4 import BeautifulSoup #pour convertir HTML en STR
import fitz  # pour pouvoir l'utiliser : pip install PyMuPDF
from langdetect import detect # pour pouvoir l'utiliser : pip install langdetect
import aspose.words as aw

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
        self.titre = donnees.title if donnees.title else self.fichier[len(self.fichier)-6:len(self.fichier)-4]
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
    #ou bien : mais dans ce cas il faudra changer la class ToC
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


class Rapport():
    """
    Cette classe crée 3 documents (pdf,epub,txt) contenant le nom de chaque auteur des livres et crée 3 autres
    documents (pdf,epub,txt) contenant le titre de chaque livre.
    3 documents contenant : [ [auteur, (livre1,livre2,...)] , [auteur, (livre1,livre2,...)] , ... ]
    3 autres documents contenant : [ [titre,auteur,langage], [titre,auteur,langage] , ....].
    
    """
    def __init__(self, dossier):
        
        self.livresPDF=Trier(dossier).DocumentsPDF[:10] #liste des livres pdf (avec le chemin des fichiers)
        self.livresEpub=Trier(dossier).DocumentsEpub[:10] #liste des livres epub (avec le chemin des fichiers)
        
        self.rapport=Livres(self.livresEpub).livres #liste des livres : [ [titre, auteur, langage] , ... ]
        for livre in Livres(self.livresPDF).livres:
            self.rapport.append(livre)

        with open("La liste des ouvrages.txt","w") as f :
            f.write("Livre 1 : \n Le titre : "+self.rapport[0][0])
        
        with open("La liste des ouvrages.txt","a+") as f :
            f.write("\n L'auteur : "+self.rapport[0][1])
            f.write("\n Le langage : "+self.rapport[0][2])
            for i in range(1,len (self.rapport)):
                f.write(f"\n\nLivre {i+1} : \n Le titre : {self.rapport[i][0]}")
                f.write("\n L'auteur : "+self.rapport[i][1])
                f.write("\n Le langage : "+self.rapport[i][2])
        #pour obtenir la liste des auteurs :
        self.rapport2=[]
        self.auteurs=[]
        for livre in self.rapport:
            if livre[1] in self.auteurs:
                pass
            else :
                self.auteurs.append(livre[1])
                self.rapport2.append([livre[1]])

        for auteur in self.auteurs :
            for livre in self.rapport :
                if auteur == livre[1]:
                    self.rapport2[self.auteurs.index(auteur)].append(livre[0])

        with open("La liste des auteurs.txt","w") as f :
            f.write("Auteur 1 : "+self.rapport2[0][0])
            f.write("\n Ses livres :")
            for k in range (1,len(self.rapport2[0])):
                f.write(f"\n Livre {k} : {self.rapport2[0][k]}")
        with open("La liste des auteurs.txt","a+") as f :
            for i in range(1,len(self.rapport2)):
                f.write(f"\n\nAuteur {i+1} : {self.rapport2[i][0]}")
                f.write("\n Ses livres :")
                for j in range(1,len(self.rapport2[i])):
                    f.write(f"\n Livre {j} : {self.rapport2[i][j]}")
                    
        # conversion de la liste txt en pdf
        doc = aw.Document("La liste des ouvrages.txt")
        doc.save("La liste des ouvrages.pdf",aw.SaveFormat.PDF)
        doc = aw.Document("La liste des auteurs.txt")
        doc.save("La liste des auteurs.pdf",aw.SaveFormat.PDF)
        
        # conversion de la liste txt en epub
        doc = aw.Document("La liste des ouvrages.txt")
        doc.save("La liste des ouvrages.epub",aw.SaveFormat.EPUB)
        doc = aw.Document("La liste des auteurs.txt")
        doc.save("La liste des auteurs.epub",aw.SaveFormat.EPUB)
        
        
    def ToC(self):
        """
        Cette fonction crée 3 documents (pdf,epub,txt) contenant le table des matières de chacun des livres dans le dossier donne en argument.
        """
        for file in self.livresPDF:
            livre = PDF(file)
            toc= livre.toc()
            with open(f"Le table des matières de {livre.titre}.txt","w") as f :
                if len(toc)>0:    
                    f.write("\n"+str(toc[0]))
                    for i in range(1,len (toc)):
                        f.write(f"\n {str(toc[i])}")
                else :
                    f.write("Ce livre ne possède pas de table de matière")
            # conversion de la liste txt en pdf:           
            doc = aw.Document(f"Le table des matières de {livre.titre}.txt")
            doc.save(f"Le table des matières de {livre.titre}.pdf",aw.SaveFormat.PDF)
            # conversion de la liste txt en epub
            doc = aw.Document(f"Le table des matières de {livre.titre}.txt")
            doc.save(f"Le table des matières de {livre.titre}.epub",aw.SaveFormat.EPUB)
            
        for file in self.livresEpub:
            livre = Epub(file)
            toc= livre.toc()
            with open(f"Le table des matières de {livre.titre}.txt","w") as f :
                 f.write(toc)
            # conversion de la liste txt en pdf
            doc = aw.Document(f"Le table des matières de {livre.titre}.txt")
            doc.save(f"Le table des matières de {livre.titre}.pdf",aw.SaveFormat.PDF)
            # conversion de la liste txt en epub
            doc = aw.Document(f"Le table des matières de {livre.titre}.txt")
            doc.save(f"Le table des matières de {livre.titre}.epub",aw.SaveFormat.EPUB)
            
    def MaJ(self):#Mise à jour des rapports
        """
        Cette classe doit mettre à jour (sans tout regénérer) les rapports précédemment générés, 
        en tenant compte de l’état présent de la bibliothèque : générer les rapports des nouveaux livres, 
        modifier ceux correspondants à des livres qui ont été modifiés depuis la dernière génération, 
        et enfin supprimer les rapports des livres disparus.
    
        Chaque exécution d’une mise à jour consigne les opérations réalisées (créations, modifications et suppression) 
        dans un fichier de log.
        """
        pass

