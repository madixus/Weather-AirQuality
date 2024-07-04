import requests
import json
import time
from datetime import datetime
from elasticsearch import Elasticsearch

# Obtenir l'heure actuelle
now = datetime.now()

# Fonction pour récupérer les données à partir d'une URL
def fetch_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch data from {url}")
            return None
    except Exception as e:
        print(f"Exception occurred while fetching data from {url}: {str(e)}")
        return None

# Fonction pour traiter les données récupérées
def process_data(data):
    if data is not None:
        # Convertir l'attribut "geo" au format GeoJSON
        if "geo" in data:
            data["geo"] = {"type": "Point", "coordinates": [data["geo"][0], data["geo"][1]]}
        # Arrondir la température à l'entier le plus proche
        if "main" in data and "temp" in data["main"]:
            data["main"]["temp"] = round(data["main"]["temp"], 0)
        return data
    else:
        return None

# Fonction pour agréger les données de différentes sources
def aggregate_data(waqi_data, openweather_data):
    if all(data is not None for data in [waqi_data, openweather_data]):
        # Effectuer l'agrégation des données ici si nécessaire
        aggregated_data = {
            "waqi_data": waqi_data,
            "openweather_data": openweather_data
        }
        return aggregated_data
    else:
        return None

# Fonction pour créer un index et son mapping dans Elasticsearch
def create_index_and_mapping(es, index_name):
    mapping = {
        "mappings": {
            "properties": {
                "@timestamp": {
                    "type": "date"
                },
                "geo": {
                    "type": "geo_point"
                },
                "openweather_data": {
                    "properties": {
                        "coord": {
                            "type": "geo_point"
                        }
                    }
                },
                "waqi_data": {
                    "properties": {
                        "data": {
                            "properties": {
                                "city": {
                                    "properties": {
                                        "geo": {
                                            "type": "geo_point"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    try:
        es.indices.create(index=index_name, body=mapping)
        print(f"Index '{index_name}' created successfully with mapping.")
    except Exception as e:
        print(f"Failed to create index '{index_name}': {str(e)}")

# Fonction principale
def main():
    # Dictionnaire contenant les URLs pour récupérer les données de différentes villes
    cities = {
        "Lyon": {
            "waqi_url": "https://api.waqi.info/feed/lyon/?token=afb92d0903a7bdf5a4f4da63ad0db94e6bf95c20",
            "openweather_url": "https://api.openweathermap.org/data/2.5/weather?lat=45.75779318439&lon=4.854217317644&appid=888a17f445f1c7f53abaeb598212c362&units=metric"
        },
        "Dijon": {
            "waqi_url": "https://api.waqi.info/feed/dijon/?token=afb92d0903a7bdf5a4f4da63ad0db94e6bf95c20",
            "openweather_url": "https://api.openweathermap.org/data/2.5/weather?lat=47.325745&lon=5.041056&appid=888a17f445f1c7f53abaeb598212c362&units=metric"
        },
        "Rennes": {
            "waqi_url": "https://api.waqi.info/feed/rennes/?token=afb92d0903a7bdf5a4f4da63ad0db94e6bf95c20",
            "openweather_url": "https://api.openweathermap.org/data/2.5/weather?lat=48.11521&lon=-1.673088&appid=888a17f445f1c7f53abaeb598212c362&units=metric"
        },
        "Orléans": {
            "waqi_url": "https://api.waqi.info/feed/Orleans/?token=afb92d0903a7bdf5a4f4da63ad0db94e6bf95c20",
            "openweather_url": "https://api.openweathermap.org/data/2.5/weather?lat=47.9071&lon=1.90109&appid=888a17f445f1c7f53abaeb598212c362&units=metric"
        },
        "Ajaccio": {
            "waqi_url": "https://api.waqi.info/feed/ajaccio/?token=afb92d0903a7bdf5a4f4da63ad0db94e6bf95c20",
            "openweather_url": "https://api.openweathermap.org/data/2.5/weather?lat=41.92466736&lon=8.73567581&appid=888a17f445f1c7f53abaeb598212c362&units=metric"
        },
        "Strasbourg": {
            "waqi_url": "https://api.waqi.info/feed/strasbourg/?token=afb92d0903a7bdf5a4f4da63ad0db94e6bf95c20",
            "openweather_url": "https://api.openweathermap.org/data/2.5/weather?lat=48.59043&lon=7.744983&appid=888a17f445f1c7f53abaeb598212c362&units=metric"
        },
        "Lille": {
            "waqi_url": "https://api.waqi.info/feed/lille/?token=afb92d0903a7bdf5a4f4da63ad0db94e6bf95c20",
            "openweather_url": "https://api.openweathermap.org/data/2.5/weather?lat=50.67003055555521&lon=3.0765610522280102&appid=888a17f445f1c7f53abaeb598212c362&units=metric"
        },
        "Paris": {
            "waqi_url": "https://api.waqi.info/feed/paris/?token=afb92d0903a7bdf5a4f4da63ad0db94e6bf95c20",
            "openweather_url": "https://api.openweathermap.org/data/2.5/weather?lat=48.856614&lon=2.3522219&appid=888a17f445f1c7f53abaeb598212c362&units=metric"
        },
        "Rouen": {
            "waqi_url": "https://api.waqi.info/feed/rouen/?token=afb92d0903a7bdf5a4f4da63ad0db94e6bf95c20",
            "openweather_url": "https://api.openweathermap.org/data/2.5/weather?lat=49.4424766601236&lon=1.0936962257792&appid=888a17f445f1c7f53abaeb598212c362&units=metric"
        },
        "Bordeaux": {
            "waqi_url": "https://api.waqi.info/feed/bordeaux/?token=afb92d0903a7bdf5a4f4da63ad0db94e6bf95c20",
            "openweather_url": "https://api.openweathermap.org/data/2.5/weather?lat=44.858413102209&lon=-0.584282227097&appid=888a17f445f1c7f53abaeb598212c362&units=metric"
        },
        "Toulouse": {
            "waqi_url": "https://api.waqi.info/feed/toulouse/?token=afb92d0903a7bdf5a4f4da63ad0db94e6bf95c20",
            "openweather_url": "https://api.openweathermap.org/data/2.5/weather?lat=43.5873309&lon=1.444026232&appid=888a17f445f1c7f53abaeb598212c362&units=metric"
        },
        "Nantes": {
            "waqi_url": "https://api.waqi.info/feed/nantes/?token=afb92d0903a7bdf5a4f4da63ad0db94e6bf95c20",
            "openweather_url": "https://api.openweathermap.org/data/2.5/weather?lat=43.5873309&lon=1.444026232&appid=888a17f445f1c7f53abaeb598212c362&units=metric"
        },
        "Marseille": {
            "waqi_url": "https://api.waqi.info/feed/marseille/?token=afb92d0903a7bdf5a4f4da63ad0db94e6bf95c20",
            "openweather_url": "https://api.openweathermap.org/data/2.5/weather?lat=43.305287&lon=5.394716&appid=888a17f445f1c7f53abaeb598212c362&units=metric"
        }
    }

    # Connexion à Elasticsearch
    es = Elasticsearch(
        ["http://localhost:9200"],
        http_auth=("elastic", "uXdRkGuLzWrusYWD3drx")
    )
    index_name = "weatherAirQualityIndex"  # Nom de l'index Elasticsearch

    # Créer l'index et son mapping
    create_index_and_mapping(es, index_name)

    # Boucle infinie pour récupérer et indexer les données toutes les 5 minutes
    while True:
        for city, urls in cities.items():
            # Récupérer les données de l'API WAQI et OpenWeather
            waqi_data = fetch_data(urls["waqi_url"])
            openweather_data = fetch_data(urls["openweather_url"])

            # Traiter les données récupérées
            processed_waqi_data = process_data(waqi_data)
            processed_openweather_data = process_data(openweather_data)

            # Agréger les données traitées
            aggregated_data = aggregate_data(processed_waqi_data, processed_openweather_data)

            if aggregated_data is not None:
                # Ajouter un timestamp actuel aux données agrégées
                aggregated_data["@timestamp"] = datetime.utcnow().isoformat()

                # Indexer les données agrégées dans Elasticsearch
                try:
                    es.index(index=index_name, body=aggregated_data)
                    print(f"Data for {city} indexed successfully. {now.strftime('%Y-%m-%d %H:%M:%S')}")
                except Exception as e:
                    print(f"Failed to index data for {city}: {str(e)}")
            else:
                print(f"No data to aggregate for {city}")

        # Attendre 5 minutes avant de récupérer les données à nouveau
        time.sleep(300)

if __name__ == "__main__":
    main()
