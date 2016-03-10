# backup_serveur
Programme de Backup de dossiers et Bases SQL d'un serveur.

Ce programme écrit en python 3.5 permet de faire une sauvegarde de répertoire et de base SQL d'un serveur sur un autre serveur en FTP.

Le fichier de config permet de donner l'ensemble des argument pour le fonctionnement du programme principale.

1er partie pour les tests : mode verbose et création d'un fichier log
2eme partie les données pour l'envoie d'un mail quand le procésus est terminé soit OK ou erreur
3eme partie connexion ftp en 2 modes SSL ou simple. Plus la possibilité de couper les fichier trop important pour votre serveur FTP
4eme partie le répertoire de sauvegarde du serveur de destination. le mode de compression ou non. les répertoires à sauvegarder et le répertoire de stokage des fichiers temporaires. Attention ne doit pas être dans un répertoire sauvegardé et sera supprimer à la fin du procésus.
5eme partie les donnée pour sauvegarder les base de données 

Les fichier sont créés avec au début le numéro du jour de la semaine (lundi 1- mardi 2- ...) donc avec une sauvegarde par jour vous aurez 7 jours de fichier et les anciens fichiers seront écrasés tous les jours.

Retrouver le bolg ici http://rasp-pi.fr.nf
