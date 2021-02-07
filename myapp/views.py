from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from myapp.models import Search
from django.utils import timezone

# Create your views here.


def index(request):
    return render(request, 'myapp/index.html')


def newsearch(request):

    CRAIGSLIST_URL = "https://losangeles.craigslist.org/search/sss?query={}&min_price={}&max_price={}"

    search = request.POST.get('search')
    min_price = request.POST.get('min_price')
    max_price = request.POST.get('max_price')

    if search:
        s = Search(search=search,created=timezone.now())
        s.save()

    r = requests.get(CRAIGSLIST_URL.format(search, min_price, max_price))
    r = r.text

    r = BeautifulSoup(r, "lxml")
    results = r.select(".result-info")
    names = []
    prices = []
    urls = []

    for x in results:
        names.append(x.select(".hdrlnk")[0].text)
        prices.append(x.select(".result-price")[0].text)
        urls.append(x.select(".hdrlnk")[0]['href'])

    context = {
        "zipped": zip(names, prices, urls),
        'search': search,
        "min_price": min_price,
        "max_price": max_price,
    }

    return render(request, 'myapp/newsearch.html', context=context)
