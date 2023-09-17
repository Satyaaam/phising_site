# # project_name/urls.py
# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('phishing/', include('phishing_app.urls')),  # Include your app's URL patterns here
# ]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('phishing_app/', include('phishing_app.urls')),
]

