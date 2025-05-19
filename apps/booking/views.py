from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


from .models import Room, Seat, MovieSession, Booking
from .serializers import RoomSerializer, RoomDetailsSerializer, SeatSerializer


class RoomListApiView(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, context={'request': request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoomDetailsApiView(APIView):
    def get(self, request, pk):
        room = get_object_or_404(
            Room.objects.prefetch_related('movie_session__movie'),
            pk=pk
        )
        serializer = RoomDetailsSerializer(room, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class SeatListApiView(APIView):

    def get(self, request, room_id, session_id):
        room = get_object_or_404(Room.objects.prefetch_related('seats'), pk=room_id)
        seats = room.seats.all()
        serializer = SeatSerializer(seats, context={'request': request, 'session_id': session_id}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, room_id, session_id):
        seat_id = request.data.get('id')
        if not seat_id:
            return Response({"error": "seat_id and session_id are required."}, status=status.HTTP_400_BAD_REQUEST)

        movie_session = get_object_or_404(MovieSession, pk=session_id)
        seat = get_object_or_404(Seat, pk=seat_id)

        if seat.room_id != room_id:
            return Response({"error": "Seat does not belong to this room."},
                            status=status.HTTP_400_BAD_REQUEST)

        if movie_session.room_id != room_id:
            return Response({"error": "Movie session does not belong to this room."},
                            status=status.HTTP_400_BAD_REQUEST)

        if Booking.objects.filter(movie_session=movie_session, seat=seat).exists():
            return Response({"error": "This seat is already reserved."},
                            status=status.HTTP_400_BAD_REQUEST)

        Booking.objects.create(movie_session=movie_session, seat=seat)

        return Response({"message": "Seat reserved successfully."}, status=status.HTTP_201_CREATED)



