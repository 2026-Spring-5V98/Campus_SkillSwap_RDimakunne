from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Django's built-in auth URLs: login, logout, password change/reset
    # These live at /accounts/login/, /accounts/logout/, etc.
    path('accounts/', include('django.contrib.auth.urls')),

    # All MainApp URLs — the empty string means they start at the root /
    path('', include('MainApp.urls')),
]
