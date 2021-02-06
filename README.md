# Description

CLI permettant de télécharger les images d'un manifest ark, 
s'il est dans le domaine public, via l'API IIIF de Gallica.
Il permet de récupérer des images de meilleure qualité par
rapport aux téléchargements image par image depuis l'interface web de Gallica.

Télécharge des fichiers images à partir d'un intervalle de folios,
présents dans un id ark. __Ce script présuppose donc une connaissance 
du contenu de l'ark duquel on souhaite avoir les images.__ 

Enregistrement par défaut des fichiers image en __JPEG__ dans un nouveau dossier, situé
là où se trouve le script python. Le nommage des fichiers respecte le numéro de folio.
Il est possible de télécharger les fichiers en __TIFF__ et en __PNG__ grâce à des options 
dans le CLI. 

Si je télécharge l'image du folio 198 en JPEG, mon fichier sera nommé "f198.jpg" et sera
enregistré dans mon répertoire lenomdurépertoirequejaichoisi.  

Le script génère également un fichier csv, nommé par l'utilisateur.ice, regroupant les
metadata de l'identifiant ark.

# Comment ça marche

Une seule commande est disponible : query

Pour exécuter le script :

```
python gallicality.py query ark from_f to_f directory_name csv_file_name
```

* ark : ID ARK
* from_f : numéro de folio indiquant le départ de l'intervalle de téléchargement
* to_f : numéro de folio indiquant la fin de l'intervalle de téléchargement
* directory_name : nom du nouveau dossier créé, dans lequel seront enregistrées les images. 
* csv_file_name : nom du fichier csv créé où sont regroupées les métadonnées.

Par exemple, pour récupérer les folios 7 à 20 du [Horla](https://gallica.bnf.fr/ark:/12148/bpt6k9923506/) de Guy de Maupassant,
édité par la librairie Ollendorff, en 1908, à Paris, et conservé à la Bibliothèque nationale de France :
 
```
python gallicality.py query ark:/12148/bpt6k9923506 7 20 le_horla le_horla_metadata
```

Il est possible de récupérer les images en TIFF avec l'option -t ou --tif 

```
python gallicality.py query ark:/12148/bpt6k9923506 7 20 le_horla le_horla_metadata -t
```
Ou bien :
```
python gallicality.py query ark:/12148/bpt6k9923506 7 20 le_horla le_horla_metadata -tif
```

Ou en PNG avec l'option -p ou --png

```
python gallicality.py query ark:/12148/bpt6k9923506 7 20 le_horla le_horla_metadata -p
```
Ou bien :
```
python gallicality.py query ark:/12148/bpt6k9923506 7 20 le_horla le_horla_metadata --png
```


# Requirements

Pour faire fonctionner ce script :

## Linux (Ubuntu/Debian) : 

Téléchargez ou clonez ce repository Github sur votre machine, au sein du dossier de votre choix.
Dans ce dossier, créez un nouvel environnement virtuel qui sera utilisé
pour installer les librairies nécessaires au fonctionnement du script et dans lequel il sera exécuté.

Pour cela, une fois dans votre dossier, ouvrez un terminal et tapez la commande suivante pour créer
un nouvel environnement virtuel :

```
virtualenv le_nom_de l'environnement_virtuel_que_vous_aurez_choisi -p python3
```

Pour l'activer, tapez la commande suivante : 

```
source le_nom_de l'environnement_virtuel_que_vous_aurez_choisi/bin/activate
```

Les librairies à télécharger dans l'environnement virtuel, une fois que celui-ci est activé, sont les suivantes : 

* requests
* click
* Pillow

L'installation peut se faire grâce au fichier requirements.txt avec la commande suivante, dans le terminal :

```
pip install -r requirements.txt
```

### Quelques informations sur la librairie Pillow

Pillow est une librairie permettant d'ouvrir, manipuler et sauvegarder des formats d'images. 
Le script utilise ici le module Image de Pillow.
Voir le site officiel de Pillow : https://pillow.readthedocs.io/en/stable/index.html
Documentation spécifique à l'installation : https://pillow.readthedocs.io/en/stable/installation.html
