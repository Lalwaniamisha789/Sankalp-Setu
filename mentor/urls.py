from django.urls import path
from . import views
from .views import mentor_frontend

urlpatterns = [
    path('mentor-chatbot/', views.mentor_chatbot, name='mentor_chatbot'),
    path('frontend/', mentor_frontend, name='mentor_frontend'),
]