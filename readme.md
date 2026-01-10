# YouExpress – Plateforme de gestion des livraisons des colis

## Contexte du projet

Actuellement, la gestion des opérations logistiques repose sur des outils manuels (fichiers Excel, supports papier), ce qui entraîne :
- Des erreurs de saisie
- Une faible fiabilité des données
- Des retards dans le traitement des colis
- Une absence de suivi en temps réel

Ce projet vise à concevoir et développer une application centralisée permettant d’automatiser et de moderniser la gestion des livraisons, tout en offrant une visibilité complète sur l’état des colis pour l’ensemble des acteurs.

## Objectifs

- Centraliser les données logistiques
- Automatiser le cycle de vie des colis
- Améliorer le suivi des livraisons en temps réel
- Réduire les erreurs et les retards opérationnels
- Faciliter la planification des tournées de livraison

---

## Fonctionnalités

### Fonctionnalités générales

- Création de compte utilisateur.
- Authentification par email et mot de passe.
- Génération d’un token JWT après authentification réussie.
- Accès sécurisé aux endpoints via JWT (Bearer Token).
- Contrôle des accès basé sur les rôles utilisateurs.

### Client

- Création d’une demande de livraison.
- Consultation de la liste de ses colis (envoyés ou destinés).

### Livreur

- Consultation de la liste des colis assignés.
- Mise à jour du statut des colis assignés (collecté, en transit, livré).

### Gestionnaire logistique

- Validation et acceptation des colis créés par les clients.
- Consultation de l’ensemble des colis.
- Assignation des colis aux livreurs.
- Filtrage des colis par statut et par ville.

---

## Technologies utilisées

- **FastAPI** – API REST
- **Pydantic** – Validation et sérialisation des données
- **SQLAlchemy (ORM)** – Accès à la base de données
- **PostgreSQL** – Base de données relationnelle
- **Postman** – Tests des endpoints
- **Pytest** – Tests unitaires
- **Docker & Docker Compose** – Conteneurisation et orchestration
- **pydantic-settings** – Gestion de la configuration via .env
- **loguru** – Journalisation des événements applicatifs
- **python-jose** - Créer des tokens JWT
- **passlib** - Chiffrer les mots de passe

---

## Architecture du projet

Le projet suit une architecture en couches :

```
Youlogix/
├── app/                
|   └── database.py         # Connexion et sessions DB PostgreSQL
├── auth  
|   ├── dependencies        # Fonctions d'authorisation et de gestion des roles                  
|   └── security            # Fonction d’authentification basée sur JWT                
├── controllers/           
├── entities/               # Schemas des tables de base de données
├── logs/        
├── models/                 # Configuration, sécurité, logging
├── routes/                 # Endpoints FastAPI
├── schemas/                # Pydantic schemas
├── tests/                  # Test Unitaire (pytest)
├── .env                    
├── config.py               # Chargement des variables d'environnement avec pydantic-settings
├── docker-compose.yml      
├── Dockerfile               
├── main.py                 # Point d’entrée de l’application
├── requirements.txt
└── test.db
```

## Bonnes pratiques appliquées

- Séparation claire des responsabilités
- Gestion centralisée des exceptions
- Validation stricte des données
- Configuration externalisée via variables d’environnement
- Tests unitaires pour assurer la fiabilité de l’API

---

## Lancement du projet

### 1. Construction et démarrage des conteneurs

Construire et lancer l’application à l’aide de Docker Compose :

```Bash
docker-compose up --build
```

Cette commande :

- Construit les images Docker
- Démarre l’API `FastAPI`, la base de données `PostgreSQL` et les tests unitaires `pytest`

### 2. Configuration des variables d’environnement

Copier le fichier d’exemple :

```Bash
cp .env_example .env
```

Modifier le fichier `.env` et renseigner les variables d’environnement nécessaires :

- Configuration de la base de données
- Clé secrète JWT

### 3. Génération de la clé secrète JWT

Générer une clé secrète sécurisée pour la signature des tokens JWT :

```Bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

- Copier la clé générée
- La renseigner dans le fichier .env (ex : SECRET_KEY=...)

### 4. Accès à l’application

Une fois l’application démarrée :

- Accès à l’API :
`http://localhost:8000`

- Accès à la documentation interactive (Swagger / OpenAPI) :
`http://localhost:8000/docs`

### 5. Exécution des tests unitaires

Lancer les tests unitaires avec Pytest depuis le conteneur Docker :

```Bash
docker-compose exec fastapi pytest
```

--- 

## Visualisations

## Documentation FastAPI

![FastAPI](https://github.com/user-attachments/assets/3f75de28-8e8e-42b5-8ed7-fded7ab334ad)

## Diagramme de classes UML

![UML](https://github.com/user-attachments/assets/ca93bfe3-ed95-4b74-b221-784576149d42)