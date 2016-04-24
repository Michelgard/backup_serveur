# -*- coding: utf-8 -*-

#############################################
#Mode verbose à True									
parole =False											
																
#Répertoire fichier log								
log = False	 												
fichierLog = '/home/michelgard/ftp_python/'	
#############################################

#########################################################
#Données pour le mail													
smtp = 'smtp.gmail.com'												
portSmtp = 587															
mailLogin = 'xxxxxxxx.xxxx@gmail.com'						
passLogin = 'xxxxxxxxx'													
email_from = 'xxxxxxxxxxxxxx.xxxx@gmail.com'						
email_to = 'xxxxxxxxxxxx.xxxx@gmail.com'						
																				
mailOK = True																
sujetMailOK = 'Procédure de sauvegarde serveur'				
texteMailOK = "Sauvegarde de l'ensemble des fichiers OK"		
																				
mailNonOK = True															
sujetMailNonOK = 'Erreur Sauvegarde'								
#########################################################

########################################
serveur = 'ftp.gdfgdfgdf.net'			
user =  'nameuser'						
mdp = 'xxxxx'									
														
mode =  True										
modeSSL = False									
tailleMaxi = 10000000							
########################################

############################################################
#Répertoire de destination des sauvegardes														
destination = '/ssssss/CloudVPS/'										
																					
#sans compression tar ou avec compression tar.bz2				
modeCompression = 'tar.bz2'												
																					
#Les répertoire à sauvegarder											
dossierupload = ["/var/www/dashscreen", "/var/www/domotic", 
"/var/www/raspberry", "/var/www/tache_cron", "/home"]				
																					
"""Le répertoire temporaire pour les sauvegarde					
Attention ne pas mettre le fichier temporaire dans un 		
répertoire sauvegarté	"""												
dossierTemporaireFTP = '/tempSauvegardeFTP'						
############################################################

###############################################################
#Sauvegarde des base de données											
sql = True																																	
userSQL = 'xxxxxxxxx'															
passSQL = 'xxxxxxxx'															
basesSQL = ["Base_DashScreen", "Base_Domotic", "Base_WordPress"]	
"""Le répertoire temporaire pour les sauvegarde						
Attention ne pas mettre le fichier temporaire SQL dans un 		
répertoire sauvegarté	"""													
dossierTemporaireSQL = '/tempSauvegardeSQL'							
###############################################################
