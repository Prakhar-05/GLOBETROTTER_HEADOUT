import json
from django.shortcuts import render
from .models import Destination

def index(request):
    # Query the Destination model (fields: city, country, clues, fun_fact, trivia, image_url)
    dests = list(Destination.objects.all().values(
        'city', 'country', 'clues', 'fun_fact', 'trivia', 'image_url'
    ))
    context = {
        'destinations_json': json.dumps(dests)
    }
    return render(request, 'game/index.html', context)
