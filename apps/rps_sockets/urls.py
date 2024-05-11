# urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Your other views
    path('ws/game/', views.GameView.as_view(), name='game_ws_view'),
]
