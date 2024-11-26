import grpc
from concurrent import futures
import showtime_pb2
import showtime_pb2_grpc

def get_movies_by_date(stub, date):
    movies = stub.GetMoviesByDate(date)
    print(movies)

def get_schedule(stub):
    schedule = stub.GetSchedule(showtime_pb2.Empty())
    for time in schedule:
        print("Time date %s" % (time.date))

def run():
    with grpc.insecure_channel('localhost:3002') as channel:
        stub = showtime_pb2_grpc.ShowtimeStub(channel)

        print("-------------- GetMoviesByDate --------------")
        date = showtime_pb2.Date(date="20151202")
        get_movies_by_date(stub, date)

        print("-------------- GetSchedule --------------")
        get_schedule(stub)

    channel.close()


if __name__ == '__main__':
    run()
