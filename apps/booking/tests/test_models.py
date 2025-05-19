import pytest
from django.utils import timezone
from datetime import timedelta
from apps.booking.models import Room, Seat, Movie, MovieSession, Booking


@pytest.fixture
def room() -> Room:
    return Room.objects.create(name="Red")


@pytest.fixture
def movie() -> Movie:
    return Movie.objects.create(name="inception", poster="test.jpg")


@pytest.fixture
def seat(room: Room) -> Seat:
    return Seat.objects.create(room=room, row=1, number=1)


@pytest.fixture
def movie_session(room: Room, movie: Movie) -> MovieSession:
    start_time = timezone.now()
    end_time = start_time + timedelta(hours=2)
    return MovieSession.objects.create(
        movie=movie,
        room=room,
        start_at=start_time,
        end_at=end_time
    )


@pytest.mark.django_db
class TestModelCreation:
    def test_create_room(self, room: Room):
        assert room.name == "Red"
        assert str(room) == "Red"

    def test_create_seat(self, seat: Seat, room: Room):
        assert seat.room == room
        assert seat.row == 1
        assert seat.number == 1

    def test_create_movie(self, movie: Movie):
        assert movie.name == "inception"
        assert movie.poster == "test.jpg"

    def test_create_movie_session(self, movie_session: MovieSession, movie: Movie, room: Room):
        assert movie_session.movie == movie
        assert movie_session.room == room

    def test_create_booking(self, movie_session: MovieSession, seat: Seat):
        booking = Booking.objects.create(movie_session=movie_session, seat=seat)

        assert booking.seat == seat
        assert booking.movie_session == movie_session
        assert booking.created_at is not None
