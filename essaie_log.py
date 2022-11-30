#Creating and Configuring Logger
# création du fichier log.
import logging
Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(filename = "logfile.log",
                    filemode = "w",
                    format = Log_Format, 
                    level = logging.INFO)

logger = logging.getLogger()

#Testing our Logger
l = [1,3,3,4]
l2 = [1,3]
logger.info("la liste est :" + str(l))
logger.info("la liste2 est :" + str(l2))
