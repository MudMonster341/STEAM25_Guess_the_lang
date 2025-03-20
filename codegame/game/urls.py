from django.urls import path
from . import views

urlpatterns = [
    # Home page where the "Start" button lives.
    path('', views.home, name='home'),
    # Game page – you may protect this with a login requirement.
    path('game/', views.game, name='game'),
    path('final_score/', views.final_score, name='final_score'),
]
