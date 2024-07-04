Weather and Air Quality Indexing
Ce projet récupère des données météo et de qualité de l'air de différentes villes en France à partir des APIs WAQI et OpenWeather, traite ces données, les agrège, et les indexe dans un cluster Elasticsearch.

Prérequis
Python 3.x
Elasticsearch (local ou distant)
Bibliothèques Python nécessaires (listées dans requirements.txt)
Installation
Clonez ce dépôt sur votre machine locale :

bash
Copy code
git clone https://github.com/madixus/Weather-AirQuality.git
cd Weather-AirQuality
Installez les dépendances Python nécessaires :

bash
Copy code
pip install -r requirements.txt
Assurez-vous qu'Elasticsearch est installé et en cours d'exécution. Vous pouvez télécharger et installer Elasticsearch à partir de leur site officiel.

Configuration
Mettez à jour les URLs des APIs WAQI et OpenWeather dans le script weatherAirQualityIndex.py si nécessaire. Les URLs actuelles utilisent des tokens d'API spécifiques et des identifiants pour les villes.

Configurez les informations d'identification pour votre cluster Elasticsearch :

python
Copy code
es = Elasticsearch(
    ["http://localhost:9200"],
    http_auth=("elastic", "votre_mot_de_passe")
)
Utilisation
Exécutez le script pour commencer à récupérer et indexer les données :

bash
Copy code
python weatherAirQualityIndex.py
Le script fonctionnera en boucle infinie, récupérant les données toutes les 5 minutes et les indexant dans Elasticsearch.

Structure du projet
weatherAirQualityIndex.py : Le script principal qui récupère, traite, agrège et indexe les données.
requirements.txt : Liste des dépendances Python nécessaires pour exécuter le script.
Fonctionnement du script
Récupération des données : Le script utilise les APIs WAQI et OpenWeather pour récupérer les données de différentes villes.
Traitement des données : Les données récupérées sont traitées pour inclure des formats compatibles avec Elasticsearch (e.g., conversion en GeoJSON, arrondi des températures).
Agrégation des données : Les données de WAQI et OpenWeather sont agrégées en une seule structure.
Indexation dans Elasticsearch : Les données agrégées sont indexées dans Elasticsearch avec un timestamp actuel.
Boucle infinie : Le processus se répète toutes les 5 minutes pour obtenir des données mises à jour.
Remarques
Assurez-vous d'avoir des tokens d'API valides pour WAQI et OpenWeather.
Ajustez les coordonnées des villes ou ajoutez d'autres villes si nécessaire.
Vérifiez que votre cluster Elasticsearch est correctement configuré pour accepter les connexions et indexer les données.
Contribuer
Les contributions sont les bienvenues ! Veuillez soumettre un pull request ou ouvrir une issue pour discuter des changements que vous souhaitez apporter.

Licence
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus d'informations.
