from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, ObjectType, QueryType, MutationType
from flask import Flask, request, jsonify, make_response

import resolvers as r

# Définition des constantes pour l'hôte et le port du serveur
PORT = 3001
HOST = '0.0.0.0'
app = Flask(__name__)

# Chargement du schéma GraphQL
type_defs = load_schema_from_path('movie.graphql')

# Définition des types et des résolveurs pour les requêtes et mutations
query = QueryType()
movie = ObjectType('Movie')
actor = ObjectType('Actor')

# Association des champs des requêtes avec leurs résolveurs respectifs
query.set_field('movie_with_id', r.movie_with_id)
query.set_field('movie_by_title', r.movie_by_title)
query.set_field('actor_with_id', r.actor_with_id)
query.set_field('movies_by_rating', r.movies_by_rating)
query.set_field('movies_by_director', r.movies_by_director)

# Définition des mutations et de leurs résolveurs respectifs
mutation = MutationType()
mutation.set_field('update_movie_rate', r.update_movie_rate)
mutation.set_field('add_movie', r.add_movie)
mutation.set_field('delete_movie', r.delete_movie)

# Définition des relations entre les types
movie.set_field('actors', r.resolve_actors_in_movie)

# Création du schéma GraphQL exécutable avec les types définis
schema = make_executable_schema(type_defs, movie, query, mutation, actor)

# Route HTTP pour l'accueil
@app.route("/", methods=['GET'])
def home():
    # Renvoie une réponse HTML simple pour la route principale
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>",200)

# Route pour gérer les requêtes GraphQL
@app.route('/graphql', methods=['POST'])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
                        schema,
                        data,
                        context_value=None,
                        debug=app.debug
                    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

# Point d'entrée du programme pour démarrer le serveur
if __name__ == "__main__":
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)