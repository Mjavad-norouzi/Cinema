from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=200)
    poster = models.ImageField(upload_to='posters/')

    def __str__(self):
        return self.name


class MovieSession(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_session')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='movie_session')
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()

    def __str__(self):
        return f'{self.movie} - {self.room} - {self.start_at}'


class Seat(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='seats')
    row = models.PositiveIntegerField(default=1)
    number = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = (('room', 'row', 'number'),)

    def __str__(self):
        return f'{self.room} - {self.row} - {self.number}'


class Booking(models.Model):
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='bookings')
    movie_session = models.ForeignKey(MovieSession, on_delete=models.CASCADE, related_name='bookings')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('seat', 'movie_session'),)

    def __str__(self):
        return f'{self.seat} - {self.movie_session}'
