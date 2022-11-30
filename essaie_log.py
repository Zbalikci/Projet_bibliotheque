
# création du fichier log à adapter avec les listes.
import logging # importation du module logging

Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(filename = "logfile.log",
                    filemode = "w",
                    format = Log_Format, 
                    level = logging.INFO)

logger = logging.getLogger()

#Teste du log sur 2 listes à afficher 
l = [1,3,3,4]
l2 = [1,3]
logger.info("la liste est :" + str(l))
logger.info("la liste2 est :" + str(l2))
