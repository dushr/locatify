
class BaseFlickrQuerySet(object):

	def __init__(self, content={}, *args, **kwargs):
		self.query_set = []

	def __getitem__(self, key):
		return self.query_set[key]

	def __iter__(self):
		for item in self.query_set:
			yield item

class FlickrPlacesQuerySet(BaseFlickrQuerySet):
	
	def __init__(self, content={}, *args, **kwargs):
		super(FlickrPlacesQuerySet, self).__init__(content, *args, **kwargs)

		for item in content.get('places', {}).pop('place', []):
			self.query_set.append(type('Place', (object,), item))

		for item, value in content.get('places', {}).iteritems():
			setattr(self, item, value)


class FlickrPhoto(object):

	IMG_URL = 'http://farm%(farm)s.staticflickr.com/%(server)s/%(id)s_%(secret)s.jpg'
	SIZE_IMG_URL = 'http://farm%(farm)s.staticflickr.com/%(server)s/%(id)s_%(secret)s_%(size)s.jpg'
	IMG_SIZE_VARS = ['s', 'q', 't', 'm', 'n']

	def __init__(self, content):
		for key, value in content.iteritems():
			setattr(self, key, value)

		for size_var in FlickrPhoto.IMG_SIZE_VARS:
			setattr(self, 'get_%s_img_url' % size_var, self._get_size_img_url(size_var))

	def get_img_url(self):
		"""
		http://farm{farm-id}.staticflickr.com/{server-id}/{id}_{secret}.jpg
		"""
		return FlickrPhoto.IMG_URL % self.__dict__

	def _get_size_img_url(self, size):
		"""
		"""
		url_attrs = self.__dict__.copy()
		url_attrs.update({'size': size})

		return FlickrPhoto.SIZE_IMG_URL % url_attrs

class FlickrPhotosQuerySet(BaseFlickrQuerySet):
	
	def __init__(self, content={}, *args, **kwargs):
		super(FlickrPhotosQuerySet, self).__init__(content, *args, **kwargs)

		for item in content.get('photos', {}).pop('photo', []):
			self.query_set.append(FlickrPhoto(item))

		for item, value in content.get('photos', {}).iteritems():
			setattr(self, item, value)

