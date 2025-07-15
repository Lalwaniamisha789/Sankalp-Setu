from django.urls import path
from .views import ngo_matcher_api, matcher_frontend
urlpatterns = [
    path('api/', ngo_matcher_api, name='matcher-api'),
]
urlpatterns += [
    path('frontend/', matcher_frontend, name='matcher_frontend'),
]