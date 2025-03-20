from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # The home page is in the game app.
    path('', include('game.urls')),
    # All account-related URLs are prefixed with 'accounts/'
    path('accounts/', include('accounts.urls')),
]
