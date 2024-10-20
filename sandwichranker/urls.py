from django.urls import path
from app import views


urlpatterns = [
    path('', views.show_sandwich, name='show_sandwich'),
    path('sandwichranker/', views.show_sandwich, name='show_sandwich'),
    path('sandwichranker/next_sandwich/', views.next_sandwich, name='next_sandwich'),
    path('sandwichranker/leaderboard/', views.leaderboard, name='leaderboard')
]
