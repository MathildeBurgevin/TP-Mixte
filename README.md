# TP MIXTE

### Sommaire 
Présentation de l'application

Exemples de structure de données dans les JSON

Lancement de l'application

Tests avec Insomnia

Tests avec les clients grpc

### Présentation de l'application
Il s’agit d’une application jouet et peu réaliste pour gérer les films et les réservations d’utilisateurs dans un cinéma. Elle utilise les technologies Flask, REST, GrahQL, gRPC et OpenAPI.
Cette application est composée de 4 micro-services :

Movie est le micro-service (en GraphQL) responsable de la gestion des films du cinéma. Il contient et gère une petite base de données json contenant la liste des films disponibles avec quelques informations sur les films.

Showtime est le micro-service (en gRPC) responsable des jours de passage des films dans le cinéma. Il contient et gère une petite base de données json contenant la liste des dates avec l’ensemble des films disponibles à cette date.

Booking est le micro-service (en gRPC) responsable de la réservation des films par les utilisateurs. Il contient et gère une petite base de données json contenant une entrée par utilisateurs avec la liste des dates et films réservés. Booking fait appel à Times pour connaître et vérifier que les créneaux réservés existent bien puisqu’il ne connait pas lui même les créneaux des films.

User est le micro-service (en REST) qui sert de point d’entrée à tout utilisateur et qui permet ensuite de récupérer des informations sur les films, sur les créneaux disponibles et de réserver. Il contient et gère une petite base de données json avec la liste des utilisateurs. User fait appel à Booking et Movie pour respectivement permettre aux utilisateurs de réserver un film ou d’obtenir des informations sur les films.

![image](https://github.com/user-attachments/assets/aa173398-8337-44de-bda9-881e08dc7ff4)

### Exemples de structure des données dans les JSON
Movie : 
    {
      "title": "Spectre", 
      "rating": 7.1, 
      "director": "Sam Mendes", 
      "id": "39ab85e5-5e8e-4dc5-afea-65dc368bd7ab"
    }
Times : 
    {
      "date":"20151130",
      "movies":[
        "720d006c-3a57-4b6a-b18f-9b713b073f3c",
        "a8034f44-aee4-44cf-b32c-74cf452aaaae",
        "39ab85e5-5e8e-4dc5-afea-65dc368bd7ab"
      ]
    }

Booking : 
    {
        "bookings": {"userid": "chris_rivers", 
            "dates": 
                [{"date": "20151201", 
                "movies": ["267eedb8-0f5d-42d5-8f43-72426b9fb3e6"]}, 
                {"date": "20151205", 
                "movies": ["7daf7208-be4d-4944-a3ae-c1c2f516f3e6"]}
            ]},
    }

User : 
    {
      "id": "peter_curley",
      "name": "Peter Curley",
      "last_active": 1360031222
    }

### Lancement
Pour lancer les quatre services de l'application, il faut lancer 4 terninaux différents, puis se déplacer à la racine du projet dans chacun d'entre eux.

Ensuite, il faut exécuter les commandes suivantes dans le premier terminal pour le service movie :

$ python -m venv monenv
$ .\monenv\Scripts\Activate
$ cd movie
$ pip install -r .\requirements.txt
$ py movie.py

Puis les commandes suivantes dans le deuxième terminal pour le service showtime :

$ python -m venv monenv
$ .\monenv\Scripts\Activate
$ cd showtime
$ python -m pip install --upgrade pip
$ python -m pip install grpcio
$ python -m pip install grpcio-tools
$ pip install -r .\requirements.txt
$ py -m grpc_tools.protoc --proto_path=./protos --python_out=. --grpc_python_out=. showtime.proto 
$ py time.py

Puis les commandes suivantes dans le troisième terminal pour le service booking :

$ python -m venv monenv
$ .\monenv\Scripts\Activate
$ cd booking
$ python -m pip install --upgrade pip
$ python -m pip install grpcio
$ python -m pip install grpcio-tools
$ pip install -r .\requirements.txt
$ py -m grpc_tools.protoc --proto_path=./protos --python_out=. --grpc_python_out=. booking.proto 
$ py -m grpc_tools.protoc --proto_path=./protos --python_out=. --grpc_python_out=. showtime.proto 
$ py time.py

Et enfin les commandes suivantes dans le quatrième terminal pour le service user :

$ python -m venv monenv
$ .\monenv\Scripts\Activate
$ cd user
$ python -m pip install --upgrade pip
$ python -m pip install grpcio
$ python -m pip install grpcio-tools
$ pip install -r .\requirements.txt
$ py -m grpc_tools.protoc --proto_path=./protos --python_out=. --grpc_python_out=. booking.proto 
$ py user.py

L'application est maintenant prête à être utilisée !

### Tests avec Insomnia
Pour effectuer les tests Insomnia, il est possible d'importer les tests que nous avons effectués à l'aide
du logiciel Insomnia. Il suffit dans l'application de créer une collection, de cliquer sur importer, puis
d'aller chercher le [fichier insomnia](https://github.com/MathildeBurgevin/TP-Mixte/blob/main/insomnia/Insomnia_TP_Miste). Les tests devraient maintenant
apparaitre par collections correspondant à chacun des services.

### Tests avec les clients grpc

Pour effectuer ces tests, il suffit de lancer l'exécution des client grpc depuis :

 - Le terminal de user, avec la commande : $ py clientTestBooking.py
 - Le terminal de booking, avec la commande : $ py clientTestShowtime.py
