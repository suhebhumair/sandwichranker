from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_sandwich),
    path('next_sandwich/', views.next_sandwich),
    path('leaderboard/', views.leaderboard)
]