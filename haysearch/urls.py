from django.conf.urls import patterns, include, url
from haysearch.views import MovieListView
from haysearch.views import *
from haystack.views import SearchView, search_view_factory

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'haysearch.views.home', name='home'),
    # url(r'^haysearch/', include('haysearch.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', MovieListView.as_view()),
    url(r'^news/$$', NewsListView.as_view()),
    url(r'^new/(\d+)/$', NewsSubject),
    url(r'^tag/(?P<tags>.+)/$', TagListView.as_view()),
    url(r'^subject/(\d+)/$', MovieSubject),
    url(r'^autocomplete/$', autocomplete),
    #url(r'^search/', include('haystack.urls')),
    url(r'^search/$', search_view_factory(view_class=TitleSearchView, load_all=False, template='search/stitle.html', form_class=TitleSearchForm), name='haystack_search'),
)
