# tse-de3-big-data-project
© DE3 - BERGAMIN Maximilien - JAULGEY Thomas - REYNARD Thibaut


# exécution de la GUI 
se mettre dans le dossier ```/Code```
et exécuter ```python gui.py``` en ligne de commande

# affichage du gantt
Ouvrir le gantt sur le site https://www.onlinegantt.com/#

# arborescence du projet
Le dossier ```Code``` contient les différents algorithmes python de pré-traitement et de machine learning.
Il y a des versions jupyter notebook et ```.py```. Les versions jupyter notebook servaient à développer et déboguer, tandis que les scripts ```.py``` sont les solutions finales exécutables.

Le script ```gui.py``` est l'interface graphique finale du projet. Elle sert à l'utilisateur final pour reseigner les caractéristiques de son logement et pour générer une prédiction d'un prix à la nuitée.

Les scripts ```mongoimport.py``` et ```script_aws.js``` permettent respectivement d'insérer un fichier ```.csv``` dans la base de données mongodb et de créer une instance EC2.

Le script ```script_aws.js``` est à lancer avec le nom du bucket s3 en argument (exemple : ```node script_aws.js nom-de-bucket-a-creer```)
```bash
.
├── Code
│   ├── airbnb.ico (icone de la GUI)
│   ├── big-data-project-2022.ipynb (notebook de pre-traitement)
│   ├── big-data-project-machine-learning.ipynb (notebook de machine learning)
│   ├── crontab_aws.txt (crontab AWS)
│   ├── donnees.py (script pour insertion fichier data entrainées dans la base mongodb)
│   ├── gui.py (GUI prediction prix - interface finale)
│   ├── ml.py (py script identique au notebook de pre-traitement)
│   ├── mongoimport.py (module python qui contient la fonction import dans mongodb)
│   ├── predicted.py (script pour importer les data inférence dans mongodb)
│   ├── prediction.py (py script identique au notebook de machine learning)
│   ├── script.sh (permet de rapatrier le fichier de data brut sur le data node hadoop et en ssh fait un scp dans un dossier instance EC2 AWS)
│   └── script_aws.js (script de creation instance EC2)
```

Le dossier ```data``` contient les différentes sources de données utilisées et générées au sein de notre projet. 

Le fichier ```33000-BORDEAUX_nettoye.csv``` est le fichier initial fourni pour le projet, contenant les données des airbnb de Bordeaux.

Les dossiers ```fv_commu_s``` et ```se_quart_s``` sont été récupérées du site opendata et contiennent les limites géographiques de la ville de Bordeaux ainsi que les limites géographiques des différents quartiers de la ville de Bordeaux.

Le fichier ```final_dataset.csv``` est le fichier généré par le script python de pré-traitement. C'est ce fichier qui est passé en entrée du script python effectuant le machine learning.

Le fichier ```predicted.csv``` historise l'ensemble des prédictions effectuées via la GUI par les utilisateurs.

Le fichier ```dataviz-soutenance-1.twbx``` est le fichier Tableau Desktop contenant les data visualisations.

```bash
├── Data
│   ├── 33000-BORDEAUX_nettoye.csv
│   ├── bordeaux-limits.csv
│   ├── dataviz-soutenance-1.twbx
│   ├── final_dataset.csv
│   ├── fv_commu_s
│   │   ├── fv_commu_s.dbf
│   │   ├── fv_commu_s.prj
│   │   ├── fv_commu_s.shp
│   │   └── fv_commu_s.shx
│   ├── fv_commu_s.zip
│   ├── predicted.csv
│   ├── se_quart_s
│   │   ├── se_quart_s.dbf
│   │   ├── se_quart_s.prj
│   │   ├── se_quart_s.shp
│   │   └── se_quart_s.shx
│   └── se_quart_s.zip
```

Ces fichiers et dossiers contiennent le ```readme``` ainsi que les présentations des soutenances et l'énoncé du projet.
```bash
├── README.md
├── Soutenances
│   ├── _finale
│   └── _intermediaire
│       ├── BigDataProject_BERGAMIN_JAULGEY_REYNARD.pdf
│       └── BigDataProject_BERGAMIN_JAULGEY_REYNARD.pptx
├── Sujet
│   └── FISA\ -\ DE3\ -\ Projet\ BigData\ NoSQL.pdf
├── gantt.gantt (importer dans https://www.onlinegantt.com/)
```

Le dossier ```images``` contient l'ensemble des images/vidéos générées lors du projet. On retrouve dans le dossier ```demo``` une capture d'écran et une vidéo démonstrative de la GUI. Dans le dossier ```regression_fit``` se trouvent toutes les regressions linéaires, triées par pourcentage de correlations entre chaque colonne. Le dossier ```wordcloud``` contient différents nuages de mots générés dans le scipt python de machine learning.
```bash
└── images
    ├── demo
    │   ├── demo_gui.mov
    │   ├── gui.png
    │   └── gantt.png
    ├── matrice_correlation.png
    ├── regression_fit
    │   ├── 0_10
    │   │   ├── regressions lineaires pour des correlations entre 0% et 10%
    │   ├── 10_20
    │   │   ├── regressions lineaires pour des correlations entre 10% et 20%
    │   ├── 20_30
    │   │   ├── regressions lineaires pour des correlations entre 20% et 30%
    │   ├── 30_40
    │   │   ├── regressions lineaires pour des correlations entre 30% et 40%
    │   ├── 40_50
    │   │   ├── regressions lineaires pour des correlations entre 40% et 50%
    │   ├── 50_60
    │   │   ├── regressions lineaires pour des correlations entre 50% et 60%
    │   ├── 60_70
    │   │   ├── regressions lineaires pour des correlations entre 60% et 70%
    │   ├── 70_80
    │   │   └── regressions lineaires pour des correlations entre 70% et 80%
    │   ├── 80_90
    │   │   └── regressions lineaires pour des correlations entre 80% et 90%
    │   ├── 90_100
    │   │   └── regressions lineaires pour des correlations entre 90% et 100%
    │   └── unclassified
    │   │   └── regressions lineaires non classifiees
    ├── regression_fit.zip
    └── wordcloud
        ├── Quartier.jpg
        ├── tokenized_Description.jpg
        ├── tokenized_Resume.jpg
        ├── tokenized_Titre.jpg
        ├── tokenized_Type_logement.jpg
        ├── tokenized_conditions_annulation.jpg
        ├── tokenized_reglement_interieur.jpg
        └── tokenized_type_propriete.jpg
```