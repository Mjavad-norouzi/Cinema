import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.booking.models import Room, Seat, Movie, MovieSession, Booking
from django.utils import timezone
from datetime import timedelta


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def movie():
    return Movie.objects.create(name="inception", poster="test.jpg")


@pytest.fixture
def room():
    return Room.objects.create(name="Red")


@pytest.fixture
def another_room():
    return Room.objects.create(name="Blue")


@pytest.fixture
def session(room, movie):
    return MovieSession.objects.create(
        room=room,
        movie=movie,
        start_at=timezone.now(),
        end_at=timezone.now() + timedelta(hours=2)
    )


@pytest.fixture
def seat(room):
    return Seat.objects.create(room=room, row=1, number=1)


@pytest.mark.django_db
class TestRoomViews:
    def test_room_list_view(self, client, room, another_room):
        url = reverse('room-list')
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_room_detail_view(self, client, room, session):
        url = reverse('room-detail', args=[room.id])
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == "Red"


@pytest.mark.django_db
class TestSeatViews:
    def test_seat_list_view(self, client, room, session):
        Seat.objects.create(room=room, row=1, number=1)
        Seat.objects.create(room=room, row=1, number=2)

        url = reverse('room-seats', args=[room.id, session.id])
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_seat_booking_view(self, client, room, session, seat):
        url = reverse('room-seats', args=[room.id, session.id])
        response = client.post(url, data={"id": seat.id})

        assert response.status_code == status.HTTP_201_CREATED
        assert Booking.objects.filter(movie_session=session, seat=seat).exists()

    def test_seat_reservation_duplicate(self, client, room, session, seat):
        Booking.objects.create(seat=seat, movie_session=session)

        url = reverse("room-seats", args=[room.id, session.id])
        response = client.post(url, data={"id": seat.id})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "This seat is already reserved." in response.data["error"]

    def test_movie_session_not_in_room(self, client, room, another_room, movie, seat):
        session = MovieSession.objects.create(
            room=another_room,
            movie=movie,
            start_at=timezone.now(),
            end_at=timezone.now() + timedelta(hours=2)
        )

        url = reverse("room-seats", args=[room.id, session.id])
        response = client.post(url, {"id": seat.id})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Movie session does not belong to this room." in response.data["error"]

    def test_seat_not_in_room(self, client, room, another_room, movie):
        session = MovieSession.objects.create(
            room=another_room,
            movie=movie,
            start_at=timezone.now(),
            end_at=timezone.now() + timedelta(hours=2)
        )
        seat = Seat.objects.create(room=another_room, row=1, number=1)

        url = reverse("room-seats", args=[room.id, session.id])
        response = client.post(url, {"id": seat.id}, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Seat does not belong to this room." in response.data["error"]
