from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from mentor.models import MentorChat
from matcher.models import NGOMatch
from sankalpSetu.views import home 
from django.contrib.auth import views as auth_views
from django.urls import path, include


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),  # ✅ this is the key fix
    path('accounts/', include('accounts.urls')), 
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('matcher/', include(('matcher.urls', 'matcher'), namespace='matcher')),
    path('mentor/', include(('mentor.urls', 'mentor'), namespace='mentor')),
    path('accounts/', include('accounts.urls')),
]