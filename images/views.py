import urllib

from django.shortcuts import render

from flickr import FlickrPlacesFind
from flickr import FlickrPhotoSearch

from images.forms import SearchForm

def home(request):
    template_context ={
        'form': SearchForm()
    }
    return render(request, 'home.html', template_context)

def search(request):
    form = SearchForm(request.GET.copy())
    template_context = {
        'form': form,
    }

    try:
        page = int(request.GET.get('page', 1))
    except ValueError, TypeError:
        page = 1

    if form.is_valid():
        places = FlickrPlacesFind(**form.cleaned_data)()
        try:
            photos = FlickrPhotoSearch(woe_id=places[0].woeid, page=page)()
        except IndexError:
            photos = []

        template_context.update({
            'places': places,
            'photos': photos,
            'query': urllib.urlencode(form.cleaned_data),
            'page': page,
        })

    return render(request, 'images/list.html', template_context)

