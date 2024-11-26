import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import json

def get_all_bookings(stub) :
    empty = booking_pb2.EmptyB()
    bookings = stub.GetAllBookings(empty)
    for booking in bookings :
        print("Bookings for user : " + booking.userid)
        for date in booking.dates:
            print("- Date %s :" % (date.date))
            print(date.movies)

def get_booking_for_user(stub, userId):
    bookings = stub.GetBookingForUser(userId)
    print("Bookings for user : " + bookings.userid)
    for date in bookings.dates:
        print("- Date %s :" % (date.date))
        print(date.movies)

def add_booking_by_user(stub, newBooking):
    response = stub.AddBookingByUser(newBooking)
    print(response)

def run():
    with grpc.insecure_channel('localhost:3003') as channel:
        stub = booking_pb2_grpc.BookingsStub(channel)

        print("-------------- GetAllBookings --------------")
        get_all_bookings(stub)

        print("-------------- GetBookingForUser --------------")
        userId = booking_pb2.UserID(userid="dwight_schrute")
        get_booking_for_user(stub, userId)

        print("-------------- AddBookingByUser --------------")
        newDate = booking_pb2.TimeB(date="20241203", movies=["id_test_add_movie1", "id_test_add_movie2"])
        newDates = [newDate]
        newBooking = booking_pb2.Booking(userid="dwight_schrute", dates=newDates)
        add_booking_by_user(stub, newBooking)

    channel.close()


if __name__ == '__main__':
    run()