# Evil-Ransomware, Copyright 2020 ©
Un ransomware affectant un système de type Unix
</br>
<tt>Joyston Anton Raveendran & Roger Priou</tt>

## Détails du ransomware :
* Fonctionnement : 
    * ``` ask_key.php ``` : Fichier .php qui doit être stocké sur un serveur pour fournir la clé demandée par le script Python. 
   <span style="color:#E33F1D;"> __/!\ La clé doit être modifiée__ </span>
    * ``` verify_key.php ``` : Fichier .php qui doit être stocké sur un serveur pour vérifier la clé envoyée par le script Python. 
   <span style="color:#E33F1D;">__/!\ La clé doit être modifiée__</span>
    * ``` requirement.txt ``` : Fichier .txt qui indique les paquets à installer lorsqu'ils sont indisponibles.
    * ``` ransomware.py ``` : Ransomware chiffrant tous les fichiers dans le dossier /tmp. 
   <span style="color:#E33F1D;">__/!\ Les adresses URLs des serveurs doivent être modifiées__</span>
    
   <span style="color:#E33F1D;">__/!\ Nous sommes en aucun cas responsables des altérations qui pourraient arriver sur vos machines__</span>

* Résumé des fonctions :

    * ```recuperation_cle()``` : permet de récupérer la clé depuis le serveur distant ```/[hash]/ask_key.php``` et modifie la variable globale en conséquence.

    * ```creation_arbre()``` : permet la création du fichier ```tree.[hash]```, retourne de nom du fichier ```tree.[hash]```.

    * ```parcours_arbre(arbre)``` : parcours l'arbre ```(nom de fichier)``` passé en paramètre et qui pour chaque fichier fait appel à la fonction ```crypto(fichier, option, cle=KEY)``` puis si cela a réussi fait appel à la fonction ```suppression(fichier)```.

    * ```crypto(fichier, option, cle=KEY)``` : permet de chiffrer ou de déchiffrer (en fonction du paramètre option) le fichier ```(nom de fichier)``` passé également en paramètre. Retourne si l'opération a réussie ou non.

    * ```suppression(fichier)``` : permet la suppression de manière sécurisée d'un fichier.

    * ```fin_chiffrement(arbre)``` : supprime le fichier arbre de manière sécurisée avec la fonction ```suppression(arbre)``` ainsi que la clé de chiffrement.

    * ```attente_cle()``` : affiche le message comme quoi les fichiers ont été chiffré et attends la clé de la part de l'utilisateur. Si l'utilisateur entre une clé alors on la vérifie avec la fonction ```test_cle(cle)``` et on lance le déchiffrement si elle est bonne.

    * ```test_cle(cle)``` : vérification de la véracité d'une clé avec le serveur et l'adresse ```/[hash]/verify_key.php```

    * ```main()``` : n'a pas de paramètre et lance automatiquement :
        * ```creation_arbre() = fichier_arbre```
        * ```parcours_arbre(fichier_arbre)```
        * ```fin_chiffrement(fichier_arbre)```
        * ```attente_cle() (en boucle)```