from django.urls import path

from apps.booking import views
from apps.booking.views import SeatListApiView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', views.RoomListApiView.as_view(), name='room-list'),
                  path('api/room/<int:pk>/movies/', views.RoomDetailsApiView.as_view(), name='room-detail'),
                  path('api/room/<int:room_id>/session/<int:session_id>/seats/', SeatListApiView.as_view(),
                       name='room-seats'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
