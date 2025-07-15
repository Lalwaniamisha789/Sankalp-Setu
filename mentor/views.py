from .mentor_utils import process_mentor_chat
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import render
from .models import MentorChat  # ✅ Import your model
from django.shortcuts import render

def mentor_frontend(request):
    return render(request, 'mentor/mentor_frontend.html')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mentor_chatbot(request):
    if request.method != 'POST':
        return Response({'error': 'GET not allowed'}, status=405)

    query = request.data.get("query")
    if not query:
        return Response({"error": "Message is required."}, status=400)

    result = process_mentor_chat(query)

    MentorChat.objects.create(
        user=request.user,
        message=query,
        response=result
    )

    return Response({"response": result})