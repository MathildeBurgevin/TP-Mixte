import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import showtime_pb2
import showtime_pb2_grpc
import json

class BookingsServicer(booking_pb2_grpc.BookingsServicer):

    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]

    def GetTimesForBooking(self, request):
        for booking in self.db:
            if booking['userid'] == request.userid:
                for time in booking['dates'] :
                    yield booking_pb2.TimeB(date=time['date'], movies=time['movies'])

    def GetAllBookings(self, request, context):
        for booking in self.db:
            userID = booking_pb2.UserID(userid=booking['userid'])
            times = self.GetTimesForBooking(userID)
            yield booking_pb2.Booking(userid=booking['userid'], dates=times)

    def GetBookingForUser(self, request, context):
        for booking in self.db:
            if booking['userid'] == request.userid:
                userID = booking_pb2.UserID(userid=booking['userid'])
                times = self.GetTimesForBooking(userID)
                return booking_pb2.Booking(userid=booking['userid'], dates=times)
            
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

def get_movies_by_date(stub, date):
    return stub.GetMoviesByDate(date)

def get_schedule(stub):
    return stub.GetSchedule(showtime_pb2.Empty())

def serve():

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingsServicer_to_server(BookingsServicer(), server)
    server.add_insecure_port('[::]:3003')
    server.start()

    server.wait_for_termination()


if __name__ == '__main__':
    serve()
