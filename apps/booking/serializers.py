from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Room, Movie, MovieSession, Seat, Booking


class RoomSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='room-detail',
        lookup_field='pk'
    )

    class Meta:
        model = Room
        fields = ['id', 'name', 'url']


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'name', 'poster']


class MovieSessionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='movie.name')
    poster = serializers.ImageField(source='movie.poster')
    start_at = serializers.DateTimeField(format='%I:%M %p')
    end_at = serializers.DateTimeField(format='%I:%M %p')
    seats_url = serializers.SerializerMethodField()

    class Meta:
        model = MovieSession
        fields = ['name', 'start_at', 'end_at', 'poster', 'seats_url']

    def get_seats_url(self, obj):
        request = self.context.get('request')
        return reverse('room-seats', args=[obj.room.id, obj.id], request=request)


class RoomDetailsSerializer(serializers.ModelSerializer):
    movies = MovieSessionSerializer(many=True, source='movie_session')

    class Meta:
        model = Room
        fields = ['name', 'movies']


class SeatSerializer(serializers.ModelSerializer):
    is_available = serializers.SerializerMethodField()

    class Meta:
        model = Seat
        fields = ['id', 'row', 'number', 'is_available']

    def get_is_available(self, seat):
        session_id = self.context.get('session_id')
        if not session_id:
            return False
        return not Booking.objects.filter(movie_session_id=session_id, seat=seat).exists()
