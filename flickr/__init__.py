import urllib
import requests

from django.conf import settings

from flickr.querysets import FlickrPlacesQuerySet
from flickr.querysets import FlickrPhotosQuerySet

class BaseFlickrApi(object):

    def __init__(self, method='', format='json', *args, **kwargs):
        self.base_url = settings.FLICKR_API_URL
        self.api_key = settings.FLICKR_API_KEY
        self.method = method
        self.format = format
        self.nojsoncallback = 1
        self.non_query_params = ['non_query_params', 'base_url']

    def build_call_url(self):
        """
        """
        attrs = self.__dict__.copy()
        for param in self.non_query_params:
            attrs.pop(param)

        query_string = urllib.urlencode(attrs)

        return '%s?%s' % (self.base_url, query_string)

    def __call__(self):
        url = self.build_call_url()

        r = requests.get(url)

        return r


class FlickrPhotoSearch(BaseFlickrApi):

    def __init__(self, woe_id='', sort='interestingness-desc', page=1, per_page=100, *args, **kwargs):
        super(FlickrPhotoSearch, self).__init__(method='flickr.photos.search', *args, **kwargs)

        self.woe_id = woe_id
        self.sort = sort
        self.per_page = per_page
        self.page = page

    def __call__(self):
        response = super(FlickrPhotoSearch, self).__call__()

        content = response.json()

        return FlickrPhotosQuerySet(content=content)

class FlickrPlacesFind(BaseFlickrApi):

    def __init__(self, query='', *args, **kwargs):
        super(FlickrPlacesFind, self).__init__(method='flickr.places.find', *args, **kwargs)

        self.query = query

    def __call__(self):
        response = super(FlickrPlacesFind, self).__call__()

        content = response.json()

        return FlickrPlacesQuerySet(content=content)