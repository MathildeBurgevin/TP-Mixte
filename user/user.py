# REST API
from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

 
import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc


app = Flask(__name__)

# Définition de l'URL de l'API GraphQL (pour les films)
MOVIE_API_URL = "http://localhost:3001"

# Route par défaut
@app.route("/", methods=['GET'])
def home():
    return "<h1>Welcome to the User Service</h1>"

# Route pour récupérer toutes les réservations des utilisateurs
@app.route("/users/bookings", methods=['GET'])
def get_all_bookings():
    # Connexion au service gRPC Booking sur localhost:3003
    with grpc.insecure_channel('localhost:3003') as channel:
        stub = booking_pb2_grpc.BookingsStub(channel)

        empty = booking_pb2.EmptyB()

        bookings = stub.GetAllBookings(empty)
        
        # Transformation des données reçues en JSON
        bookings_list = []
        for booking in bookings :
            booking_data = {
                "userid": booking.userid,
                "dates": [
                    {
                        "date": date.date,
                        "movies": list(date.movies)
                    }
                    for date in booking.dates
                ]
            }
            bookings_list.append(booking_data)
        
        # Retourne les réservations sous forme de JSON
        return jsonify(bookings_list)

    channel.close()

# Route pour récupérer les réservations d'un utilisateur spécifique
@app.route("/users/<userid>/bookings", methods=['GET'])
def get_user_bookings(userid):
    with grpc.insecure_channel('localhost:3003') as channel:
        stub = booking_pb2_grpc.BookingsStub(channel)

        userId = booking_pb2.UserID(userid=userid)
        bookings = stub.GetBookingForUser(userId)

        dates_list =[]
        for date in bookings.dates:
            date_data = {
                        "date": date.date,
                        "movies": list(date.movies)
                    }
            dates_list.append(date_data)

        # Retourne les réservations de l'utilisateur
        return jsonify(dates_list)
    
    channel.close()

# Route pour récupérer les détails des films réservés par un utilisateur
@app.route("/users/<userid>/movies", methods=['POST'])
def get_user_movies(userid):

    with grpc.insecure_channel('localhost:3003') as channel:
        stub = booking_pb2_grpc.BookingsStub(channel)

        userId = booking_pb2.UserID(userid=userid)
        bookings = stub.GetBookingForUser(userId)

        movie_details = []
        
        for date_item in bookings.dates:
            for movie_id in date_item.movies:
                body = f""" 
                {{
                    movie_with_id(_id:"{movie_id}") {{
                        id
                        title
                        rating
                        director 
                    }}
                }} 
                """
                movie_response = requests.post(f"{MOVIE_API_URL}/graphql", json={'query': body})
                if movie_response.status_code == 200:
                    movie_details.append(movie_response.json())

        # Retourne les détails des films
        return jsonify(movie_details), 200
    
    channel.close()

# Route pour ajouter une réservation pour un utilisateur
@app.route("/users/<userid>/addbooking", methods=['POST'])
def add_booking(userid):
    # Récupérer les données JSON de la requête POST
    data = request.get_json()
    if not data or 'date' not in data or 'movies' not in data:
        return jsonify({"error": "Invalid request. 'date' and 'movies' are required."}), 400

    try:
        date = data['date'] 
        movies = data['movies']  
        
        with grpc.insecure_channel('localhost:3003') as channel:
            stub = booking_pb2_grpc.BookingsStub(channel)

            # Construire l'objet TimeB
            newDate = booking_pb2.TimeB(date=date, movies=movies)
            newDates = [newDate] 

            # Construire l'objet Booking
            newBooking = booking_pb2.Booking(userid=userid, dates=newDates)  # Notez la liste pour `dates`

            # Appeler le service gRPC AddBookingByUser
            response = stub.AddBookingByUser(newBooking)

        # Retourner la réponse du service gRPC au client
        return jsonify({"message": response.response}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3202)