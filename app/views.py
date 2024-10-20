from django.shortcuts import render
from django.http import HttpResponse
import requests
import random
from .models import Sandwich


sandwich = None

# Create your views here.
def fetch_sandwiches():
    url = 'https://query.wikidata.org/sparql'
    query = '''SELECT ?sandwich ?image ?sandwichLabel WHERE {
        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
        ?sandwich wdt:P279 wd:Q28803.
        ?sandwich wdt:P18 ?image.
    }'''
    
    try:
        r = requests.get(url, params={'format': 'json', 'query': query})
        r.raise_for_status()
        data = r.json()
        sandwiches = data["results"]["bindings"]
        return sandwiches
    except (requests.RequestException, ValueError) as e:
        return None

def show_sandwich(request):
    sandwiches = fetch_sandwiches()
    if sandwiches:
        sandwich = random.choice(sandwiches)
        print(sandwich)
        print()
        return render(request, 'index.html', {'sandwiches': [sandwich]})
    else:
        return HttpResponse("Error fetching sandwiches.")


def next_sandwich(request):
    if request.method == 'POST':
        try:
            rating = int(request.POST.get('rating', 0))
            if rating < 0 or rating > 10:
                return HttpResponse("Rating must be between 0 and 10.")
        except ValueError:
            return HttpResponse("Invalid rating. Please enter a number between 0 and 10.")

        sandwich_id = request.POST.get('sandwich_id')  # Get the sandwich ID from the form
        sandwiches = fetch_sandwiches()  # Fetch all sandwiches

        if sandwiches:

            for sandwich in sandwiches:
                if sandwich_id == sandwich["sandwich"]["value"]:
                    print("WE ARE DOING " + sandwich_id)
                    print(sandwich["image"]["value"])
                    sandwich_obj, created = Sandwich.objects.update_or_create(
                    sandwich_id=sandwich_id,
                    defaults={
                    'sandwich_name': sandwich["sandwichLabel"]["value"],
                    'sandwich_image': sandwich["image"]["value"]
                    }
                    )        
            
            print(sandwich_obj)

            sandwich_obj.total_score += rating
            sandwich_obj.total_submissions += 1
            sandwich_obj.average_rating = sandwich_obj.total_score / sandwich_obj.total_submissions
            sandwich_obj.percentage = sandwich_obj.average_rating * 10
            sandwich_obj.save()

            selected_sandwich = random.choice(sandwiches)  # Pick a random sandwich

            # Now render the randomly selected sandwich
            return render(request, 'index.html', {'sandwiches': [selected_sandwich]})
        else:
            return HttpResponse("Error fetching sandwiches.")

    return HttpResponse("Invalid request method.")





def leaderboard(request):
    if request.method == 'GET':
        top_sandwiches = Sandwich.objects.all().order_by('-average_rating')[:10]
        
        return render(request, 'leaderboard.html', {'sandwiches': top_sandwiches})