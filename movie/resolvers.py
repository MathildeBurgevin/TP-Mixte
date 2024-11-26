import json

def movie_with_id(_,info,_id):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie

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

def resolve_actors_in_movie(movie, info):
    with open('{}/data/actors.json'.format("."), "r") as file:
        actors = json.load(file)
        result = [actor for actor in actors['actors'] if movie['id'] in actor['films']]
        return result
    
def movie_by_title(_,info,_title):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['title'] == _title:
                return movie
            
def actor_with_id(_,info,_id):
    with open('{}/data/actors.json'.format("."), "r") as file:
        actors = json.load(file)
        for actor in actors['actors']:
            if actor['id'] == _id:
                return actor
            
def movies_by_rating(_,info,_rate):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        result = [movie for movie in movies['movies'] if movie['rating'] == _rate]
        return result
    
def movies_by_director(_,info,_director):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        result = [movie for movie in movies['movies'] if movie['director'] == _director]
        return result
    
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