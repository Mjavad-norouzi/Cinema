import pytest
from rest_framework.test import APIRequestFactory
from rest_framework.reverse import reverse
from datetime import timedelta
from django.utils import timezone
from apps.booking.models import Room, Seat, Movie, MovieSession, Booking
from apps.booking.serializers import MovieSessionSerializer, SeatSerializer


@pytest.fixture
def movie() -> Movie:
    return Movie.objects.create(name="inception", poster="test.jpg")


@pytest.fixture
def room() -> Room:
    return Room.objects.create(name="Red")


@pytest.fixture
def session(movie: Movie, room: Room) -> MovieSession:
    return MovieSession.objects.create(
        movie=movie,
        room=room,
        start_at=timezone.now(),
        end_at=timezone.now() + timedelta(hours=2)
    )


@pytest.fixture
def seat(room: Room) -> Seat:
    return Seat.objects.create(room=room, row=1, number=1)


@pytest.fixture
def factory() -> APIRequestFactory:
    return APIRequestFactory()


@pytest.mark.django_db
class TestMovieSessionSerializer:
    def test_seats_url(self, factory: APIRequestFactory, session: MovieSession, room: Room):
        request = factory.get('/')
        serializer = MovieSessionSerializer(session, context={'request': request})

        expected_url = reverse('room-seats', args=[room.id, session.id], request=request)
        assert serializer.data['seats_url'] == expected_url


@pytest.mark.django_db
class TestSeatSerializer:
    def test_is_available_when_seat_free(self, seat: Seat, session: MovieSession):
        serializer = SeatSerializer(seat, context={'session_id': session.id})
        assert serializer.data['is_available'] is True

    def test_is_available_when_seat_booked(self, seat: Seat, session: MovieSession):
        Booking.objects.create(movie_session=session, seat=seat)
        serializer = SeatSerializer(seat, context={'session_id': session.id})
        assert serializer.data['is_available'] is False