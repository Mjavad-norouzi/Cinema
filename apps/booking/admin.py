from django.contrib import admin
from django.utils.html import format_html

from .models import Room, Seat, Movie, MovieSession, Booking


class SeatInline(admin.TabularInline):
    model = Seat
    extra = 0


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'seat_count']
    list_display_links = ['name']
    search_fields = ['name']
    inlines = [SeatInline]

    def seat_count(self, obj):
        return obj.seats.count()

    seat_count.short_description = 'Total Seats'


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['room', 'row', 'number']
    list_filter = ['room']
    search_fields = ['room__name']
    ordering = ['room', 'row', 'number']


class MovieSessionInline(admin.TabularInline):
    model = MovieSession
    extra = 0


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'poster_preview']
    search_fields = ['name']
    inlines = [MovieSessionInline]

    def poster_preview(self, obj):
        if obj.poster:
            return format_html('<img src="{}" style="height: 60px;" />', obj.poster.url)
        return "-"

    poster_preview.short_description = 'Poster'


@admin.register(MovieSession)
class MovieSessionAdmin(admin.ModelAdmin):
    list_display = ['movie', 'room', 'start_at', 'end_at', 'booking_count']
    list_filter = ['room', 'movie']
    search_fields = ['movie__name']
    autocomplete_fields = ['movie', 'room']

    def booking_count(self, obj):
        return obj.bookings.count()

    booking_count.short_description = 'Booked Seats'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['movie_session', 'seat', 'created_at']
    list_filter = ['movie_session__room', 'movie_session']
    search_fields = ['movie_session__movie__name', 'seat__number', 'seat__row']
    ordering = ['-created_at']
