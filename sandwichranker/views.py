from django.shortcuts import render
from django.http import HttpResponse
import requests
import random
from .models import Sandwich


sandwich = None

# Create your views here.
def show_sandwich(request):
    import requests

    url = 'https://query.wikidata.org/sparql'
    query = '''SELECT ?sandwich ?image ?sandwichLabel WHERE {
        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
        ?sandwich wdt:P279 wd:Q28803.
        ?sandwich wdt:P18 ?image.
        }
        '''
    r = requests.get(url, params = {'format': 'json', 'query': query})
    data = r.json()
    sandwiches = data["results"]["bindings"]
    sandwich = random.choice(sandwiches)
    return render(request, 'index.html', {'sandwiches': [sandwich]})

def next_sandwich(request):
    if request.method == 'POST':
        rating = request.POST.get('rating')

        rating = int(rating)
        
        if (rating < 0) or (rating > 10):
            return HttpResponse(" You cannot enter a number other than 0-10")

        url = 'https://query.wikidata.org/sparql'
        query = '''SELECT ?sandwich ?image ?sandwichLabel WHERE {
        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
        ?sandwich wdt:P279 wd:Q28803.
        ?sandwich wdt:P18 ?image.
        }
        '''
        r = requests.get(url, params = {'format': 'json', 'query': query})
        data = r.json()

        sandwiches = data["results"]["bindings"]
        #update db

        for sandwich in sandwiches:
            sandwich_id = sandwich['sandwich']['value'].split('/')[-1]
            if Sandwich.objects.filter(sandwich_id=sandwich_id).exists():
                Sandwich.objects.filter(sandwich_id=sandwich_id).update(
                sandwich_name=sandwich["sandwichLabel"]["value"],
                sandwich_image=sandwich["image"]["value"]
            )
            else:
                Sandwich.objects.create(
                    sandwich_id=sandwich_id,
                    sandwich_name=sandwich["sandwichLabel"]["value"],
                    sandwich_image=sandwich["image"]["value"]
                )


        mysandwich = Sandwich.objects.get(sandwich_id=sandwich['sandwich']['value'].split('/')[-1])
        mysandwich.total_score += int(rating)
        mysandwich.total_submissions +=1
        mysandwich.average_rating = mysandwich.total_score/mysandwich.total_submissions
        mysandwich.percentage = mysandwich.average_rating * 10
        mysandwich.save()

        sandwich = random.choice(sandwiches)
        return render(request, 'index.html', {'sandwiches': [sandwich]})
    else:
        return HttpResponse("Invalid request method")

def leaderboard(request):
    if request.method == 'GET':
        top_sandwiches = Sandwich.objects.all().order_by('-average_rating')[:10]
        
        return render(request, 'leaderboard.html', {'sandwiches': top_sandwiches})