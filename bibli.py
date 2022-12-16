#!/bin/env python3
import sys
from Partie1_Balikci_Mbaye import Rapport

if __name__ == "__main__":
    if sys.argv[1]="-c":
        conf=sys.argv[2]
    
    conf="bibli.conf"
    f = open(conf, "r")
    lines=f.readlines()
    dossier=lines[0]
    chemin_rapports=lines[1]

    if(sys.argv[-1])=="init":
        r=Rapport(dossier)
        r.write(chemin_rapports)
        r.ToC(chemin_rapports)

    elif(sys.argv[-1])=="update":
        r.MaJ(chemin_rapports)
