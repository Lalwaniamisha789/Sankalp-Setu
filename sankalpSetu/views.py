from django.shortcuts import render, redirect
from matcher.models import MatcherHistory, NGOMatch
from mentor.models import MentorChat

def home(request):
    mentor_chats = []
    matcher_history = []
    ngo_matches = []

    if request.user.is_authenticated:
        mentor_chats = MentorChat.objects.filter(user=request.user).order_by('-created_at')[:10]
        matcher_history = list(
            MatcherHistory.objects.filter(user=request.user)
            .order_by('-created_at')
            .values('query', 'results')
        )
        ngo_matches = NGOMatch.objects.filter(user=request.user).order_by('-matched_at')[:5]

    return render(request, 'home.html', {
        'mentor_chats': mentor_chats,
        'matcher_history': matcher_history,
        'ngo_matches': ngo_matches,
    })
