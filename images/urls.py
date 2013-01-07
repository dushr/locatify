from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('images.views',
    # Examples:
    url(r'search/$', 'search', name='search'),
    url(r'^$', 'home', name='home'),

)
