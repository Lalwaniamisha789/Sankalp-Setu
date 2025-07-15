from django.shortcuts import render
from .matcher_utils import match_ngo
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from .models import MatcherHistory

@csrf_exempt
def ngo_matcher_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        query = data.get('query')
        if query:
            raw_results = match_ngo(query)
            if request.user.is_authenticated:
                print("Saving history for user:", request.user)
                MatcherHistory.objects.create(
                    user=request.user,
                    query=query,
                    results=raw_results
                )
            else:
                matcher_history = request.session.get('matcher_history', [])
                matcher_history.insert(0, {'query': query, 'results': raw_results})
                request.session['matcher_history'] = matcher_history
            return JsonResponse({'results': raw_results}, safe=False)
        return JsonResponse({'error': 'No query provided'}, status=400)
    return JsonResponse({'error': 'POST only'}, status=405)


def matcher_frontend(request):
    if request.user.is_authenticated:
        matcher_history = list(MatcherHistory.objects.filter(user=request.user).order_by('-created_at').values('query', 'results'))
    else:
        matcher_history = request.session.get('matcher_history', [])
    return render(request, 'matcher/matcher_frontend.html', {
        'matcher_history': mark_safe(json.dumps(matcher_history))
    })
