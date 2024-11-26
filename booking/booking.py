import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import showtime_pb2
import showtime_pb2_grpc
import json

# Définition du service gRPC BookingsServicer
class BookingsServicer(booking_pb2_grpc.BookingsServicer):

    # Chargement des données des réservations depuis un fichier JSON
    def __init__(self): 
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]

    # Méthode pour récupérer les horaires d'un utilisateur spécifique
    def GetTimesForBooking(self, request):
        for booking in self.db:
            if booking['userid'] == request.userid: 
                for time in booking['dates'] :
                    # Retourne chaque date et les films associés
                    yield booking_pb2.TimeB(date=time['date'], movies=time['movies']) 

    # Méthode pour récupérer toutes les réservations
    def GetAllBookings(self, request, context):
        for booking in self.db:
            userID = booking_pb2.UserID(userid=booking['userid'])
            times = self.GetTimesForBooking(userID) 
            # Retourne une réservation complète pour chaque utilisateur
            yield booking_pb2.Booking(userid=booking['userid'], dates=times) 

    # Méthode pour récupérer les réservations d'un utilisateur donné
    def GetBookingForUser(self, request, context):
        for booking in self.db:
            if booking['userid'] == request.userid:
                userID = booking_pb2.UserID(userid=booking['userid'])
                times = self.GetTimesForBooking(userID)
                # Retourne les données de réservation pour l'utilisateur
                return booking_pb2.Booking(userid=booking['userid'], dates=times)

    # Méthode pour ajouter une réservation pour un utilisateur donné     
    def AddBookingByUser(self, request, context):
        
        # Convertion du résultat de la requête en un format dictionnaire pour pouvoir le manipuler en json
        newBooking = {
            "userid": request.userid,
            "dates": [{"date": date.date, "movies": list(date.movies)} for date in request.dates]
        }

        # Vérification que l'utilisateur existe déjà ou non dans la base de données
        userExists = False
        for booking in self.db:
            if booking['userid'] == request.userid:
                userExists = True
                # Ajout des nouvelles dates et films
                for newDate in newBooking['dates']:
                    booking['dates'].append(newDate)
                    '''
                    # Vérification que la date existe déjà ou non pour l'utilisateur
                    existingDate = next((date for date in booking['dates'] if date['date'] == newDate['date']), None)
                    if existingDate:
                        # Ajout des films pour la même date
                        existingDate['movies'] = list(set(existingDate['movies'] + newDate['movies']))
                    else:
                        # Ajout de la nouvelle date
                        booking['dates'].append(newDate)
                    '''

        if not userExists:
            # Ajout d'une nouvelle réservation pour l'utilisateur
            self.db.append(newBooking)

        # Sauvegarde des modifications dans le fichier JSON
        with open('{}/data/bookings.json'.format("."), "w") as jsf:
            json.dump({"bookings": self.db}, jsf, indent=4)

        
        # Envoi d'un message retour de succès
        return booking_pb2.Response(response="Réservation ajoutée avec succès !")

# Récupère les films disponibles pour une date spécifique
def get_movies_by_date(stub, date):
    return stub.GetMoviesByDate(date)

# Récupère tout le programme des films
def get_schedule(stub):
    return stub.GetSchedule(showtime_pb2.Empty())

# Fonction pour démarrer le serveur gRPC
def serve():

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingsServicer_to_server(BookingsServicer(), server)
    server.add_insecure_port('[::]:3003')
    server.start()

    server.wait_for_termination()

# Point d'entrée du programme
if __name__ == '__main__':
    serve()
