import json

# Recherche un film par son ID
def movie_with_id(_,info,_id):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie

# Met à jour la note (rating) d'un film
def update_movie_rate(_,info,_id,_rate):
    newmovies = {}
    newmovie = {}
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _id:
                movie['rating'] = _rate
                newmovie = movie
                newmovies = movies
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    return newmovie

# Récupère les acteurs associés à un film
def resolve_actors_in_movie(movie, info):
    with open('{}/data/actors.json'.format("."), "r") as file:
        actors = json.load(file)
        result = [actor for actor in actors['actors'] if movie['id'] in actor['films']]
        return result

# Recherche un film par son titre
def movie_by_title(_,info,_title):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['title'] == _title:
                return movie
            
# Recherche un acteur par son ID
def actor_with_id(_,info,_id):
    with open('{}/data/actors.json'.format("."), "r") as file:
        actors = json.load(file)
        for actor in actors['actors']:
            if actor['id'] == _id:
                return actor

# Recherche les films ayant une note spécifique           
def movies_by_rating(_,info,_rate):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        result = [movie for movie in movies['movies'] if movie['rating'] == _rate]
        return result

# Recherche les films réalisés par un réalisateur donné
def movies_by_director(_,info,_director):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        result = [movie for movie in movies['movies'] if movie['director'] == _director]
        return result

# Ajoute un nouveau film dans la base de données
def add_movie(_,info,_id, _title, _director, _rating):
    newmovie = {
        "id": _id,
        "title": _title,
        "director": _director,
        "rating": _rating
    }
    moviesTab = []
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            moviesTab.append(movie)
    moviesTab.append(newmovie)
    newmovies = {
        "movies": moviesTab
    }
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    return newmovie

# Supprime un film de la base de données
def delete_movie(_,info,_id):
    moviesTab = []
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] != _id:
                moviesTab.append(movie)
    newmovies = {
        "movies": moviesTab
    }
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    return moviesTab