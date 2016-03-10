# -*- coding: utf-8 -*-
from ftplib import FTP_TLS
import ftplib
import os
import sys
from config_ftp import *
import tarfile
import shutil
import time
import glob
import ssl
import smtplib
from email.mime.text import MIMEText
 
def connexionftp(adresseftp, nom, mdpasse, passif):
	"""connexion au serveur ftp et ouverture de la session
	   - adresseftp: adresse du serveur ftp
	   - nom: nom de l'utilisateur enregistré ('anonymous' par défaut)
	   - mdpasse: mot de passe de l'utilisateur ('anonymous@' par défaut)
	   - passif: active ou désactive le mode passif (True par défaut)
	   retourne la variable 'ftplib.FTP' après connexion et ouverture de session
	"""
	try:
		verbose('Attente connexion FTP .....')
		if modeSSL:
			ftp = FTP_TLS()
			ftp.connect(adresseftp, 21)
			ftp.login(nom, mdpasse)
			ftp.prot_p()
			ftp.set_pasv(passif)
		else:
			ftp = (ftplib.FTP(adresseftp, nom, mdpasse))
			
		ftp.cwd(destination)
		verbose ('Destination : '+destination)
		verbose('Connexion FTP OK')
		etat = ftp.getwelcome()
		verbose("Etat : "+ etat) 
		return ftp
	except:
		verbose('Connexion FTP impossible', True)
		suppressionDossierTemp(dossierTemporaireFTP)
		sys.exit()
		
def fermerftp(ftp):
    """ferme la connexion ftp
        - ftp: variable 'ftplib.FTP' sur une connexion ouverte
    """
    try:
        ftp.quit()
    except:
        ftp.close() 

def uploadftp(ftp, ficdsk, numero,nombreFichier, ficftp=None):
    """télécharge le fichier ficdsk du disque dans le rép. courant du Serv. ftp
        - ftp: variable 'ftplib.FTP' sur une session ouverte
        - ficdsk: nom du fichier disque avec son chemin
        - ficftp: si mentionné => c'est le nom qui sera utilisé sur ftp
    """
    try: 
        repdsk, ficdsk2 = os.path.split(ficdsk)
        if ficftp==None:
            ficftp = ficdsk2
        with open(ficdsk, "rb") as f:
            ftp.storbinary('STOR ' + ficftp, f)
            verbose('Fichier : ' + str(numero) + '/' + str(nombreFichier) + ' uploader sur le serveur')
    except:
        verbose('Erreur lors de l\'upload du fichier numero : ' + str(numero), True)
        suppressionDossierTemp(dossierTemporaireFTP)
        fermerftp(ftp)
        sys.exit()
    
def verbose(texte, erreur = False):
	"""print du texte si verbose du config est à True """
	"""écriture dans fichier log si log est à True"""
	if parole:
		print(texte)
	if log:
		lesLog(time.strftime('%d/%m/%y %H:%M',time.localtime()) + ' ' +texte + '\n')
	if mailNonOK & erreur:
		sendEmail(email_from, email_to, sujetMailNonOK, texte, smtp, portSmtp, mailLogin, passLogin)
		
def modeDeCompression():
	if modeCompression == 'tar':
		comp = 'w:'
		verbose('Mode compression ' + modeCompression + ' OK')
		return comp
	elif modeCompression == 'tar.bz2':
		comp = 'w:bz2'
		verbose('Mode compression ' + modeCompression + ' OK')
		return comp
	else:
		verbose('Erreur sur le mode de compression tar ou tar.bz2', True)
		suppressionDossierTemp(dossierTemporaireFTP)
		sys.exit()

def creationDossierTemp(dossierTemporaire):
	try:	
		if os.path.exists(dossierTemporaire):
			shutil.rmtree(dossierTemporaire)
		os.mkdir(dossierTemporaire) 
		verbose('Creation dossier temporaire OK')
	except:
		verbose('Erreur creation du dossier temporaire', True)
		suppressionDossierTemp(dossierTemporaireFTP)
		sys.exit()
		
def suppressionDossierTemp(dossierTemporaire):
	try:	
		if os.path.exists(dossierTemporaire):
			shutil.rmtree(dossierTemporaire)		
			verbose('Suppression dossier temporaire OK')
	except:
		verbose('Erreur suppression du dossier temporaire', True)
		sys.exit()

def compressionDossier(dossier, comp):
	try:
		numJourSemaine = time.localtime().tm_wday + 1
		nomArchive = dossierTemporaireFTP + '/' + str(numJourSemaine) +  dossier.replace('/', '-') + '.' + modeCompression
		archive = tarfile.open(nomArchive, comp)
		archive.debug = 0 #parole  
		archive.add(dossier)
		archive.close()
		
		nomArchive2 = dossierTemporaireFTP + '/' + str(numJourSemaine) +  dossier.replace('/', '-') + '-' 
		
		if os.path.getsize(nomArchive) > tailleMaxi:
			os.system('split -b ' + str(tailleMaxi) + ' ' + nomArchive + ' ' + nomArchive2)
			os.system('rm ' + nomArchive)
			
		verbose ('Dossier ' + dossier + ' archive OK')
	except Exception as e:
		verbose('Erreur sur fichier archive', True)
		suppressionDossierTemp(dossierTemporaireFTP)
		sys.exit()
		
#Ecriture dans fichier log		
def lesLog(texte):		
	with open(fichierLog + 'ftp.log', 'a') as fichier:
		fichier.write(texte)
		
# Envoie mail 
def sendEmail(email_from, email_to, subject, text, smtp, portSmtp, mailLogin, passLogin):
	try:
		verbose('Sendmail ...')
		msg = MIMEText(text)
		msg['Subject'] = subject
		msg['From']    = email_from
		msg['To']      = email_to
		s = smtplib.SMTP(smtp, portSmtp)
		s.ehlo()
		s.starttls()
		s.ehlo()
		s.login(mailLogin, passLogin)
		s.sendmail(email_from,[email_to],msg.as_string())
		s.quit()
		verbose('Sendmail OK')
	except:
		verbose('Erreur lors du sendmail')
		suppressionDossierTemp(dossierTemporaireFTP)
		fermerftp(ftp)
		sys.exit()
		
def dumpSQL(dossier):
	try:
		commande = 'mysqldump -u ' + userSQL + ' -p' + passSQL + ' ' + dossier + ' > ' + dossierTemporaireSQL + '/' + dossier + '.sql'
		os.system(commande)
		verbose('Archive Base SQL : ' + dossier + ' OK')
	except:
		verbose('Erreur sur archive Base SQL : ' + dossier)
		suppressionDossierTemp(dossierTemporaireSQL)
		suppressionDossierTemp(dossierTemporaireFTP)
		
#Archive des dossiers		
creationDossierTemp(dossierTemporaireFTP)
comp = modeDeCompression()		
for dossier in dossierupload: 		
	compressionDossier(dossier, comp)
	
#Sauvegarde base SQL
if sql:
	creationDossierTemp(dossierTemporaireSQL)
	for dossier in basesSQL: 		
		dumpSQL(dossier)
	compressionDossier(dossierTemporaireSQL, comp)
	suppressionDossierTemp(dossierTemporaireSQL)
	
#connexion au FTP
ftp = connexionftp(serveur, user, mdp, mode)

#upload des fichier d'archive
listeFichier = glob.glob(dossierTemporaireFTP + '/*')
nombreFichier = len(listeFichier)
len(os.listdir('.'))
for numero, fichier in enumerate(listeFichier):	
	numero = numero + 1
	uploadftp(ftp, fichier, numero, nombreFichier, ficftp=None)

suppressionDossierTemp(dossierTemporaireFTP)

if mailOK:
	sendEmail(email_from, email_to, sujetMailOK, texteMailOK, smtp, portSmtp, mailLogin, passLogin)
	
#Fermeture FTP
fermerftp(ftp)
