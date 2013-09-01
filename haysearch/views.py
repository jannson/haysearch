# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django import forms
from django.shortcuts import render_to_response
from django.http import HttpResponse
#from django.views.generic.list_detail import object_list
from django.views.generic import ListView
from django.db.models import Count
from django.db.models import Q
from django.db import connection
from haystack.forms import SearchForm, ModelSearchForm
from haystack.query import SearchQuerySet
from haystack.inputs import AutoQuery, Exact, Clean
from haystack.views import SearchView, search_view_factory
import simplejson as json
from haysearch.models import *

class TitleSearchView(SearchView):
    def extra_context(self):
        extra = super(TitleSearchView, self).extra_context()
        extra['top_tags'] = Tag.objects.all().annotate(num_items=Count('doubanmovie')).order_by('-num_items')[0:33]
        return extra

class TitleSearchForm(SearchForm):
    def get_result_id(self, id):
        return id
    '''def __init__(self, *args, **kwargs):
        super(TitleSearchForm, self).__init__(*args, **kwargs)
        self.fields['q'].widget.attrs.update({'class' : 'autocomplete-me'})'''
    def search(self):
        #print 'test............'
        if not self.is_valid():
            return self.no_query_found()
        if not  self.cleaned_data.get('q'):
            return self.no_query.found()

        #print self.searchqueryset
        sqs = self.searchqueryset.filter(content=self.cleaned_data['q'])
        print 'search in form'
        #sqs.spelling_suggestion(self.cleaned_data['q'])
        #obj = sqs[0].object
        #sqs = SearchQuerySet()
        #sqs = sqs.more_like_this(obj)
        
        #if self.load_all:
        #    sqs = sqs.load_all()
        return sqs

def MovieSubject(request, id):
    try:
        obj = DoubanMovie.objects.get(pk=id)
        return render_to_response('movie_subject.html', {'entry':obj})
    except:
        return HttpResponse('No find!')

#def MovieHome(request):
#    movie_list = DoubanMovie.objects.annotate(cnt=Count('tag')).filter(Q(from_type=1) & (Q(cnt>=0)).order_by('-cnt')
#    return object_list(request, template_name='movie_home.html', queryset=movie_list, paginate_by=25)

class MovieListView(ListView):
    #object_list = DoubanMovie.objects.filter(Q(from_type=1)).order_by('-rating')
    #object_list = DoubanMovie.objects.extra(
    #    select={
    #        'entry_count': 'SELECT COUNT(*) FROM movielink WHERE movielink.douban_id = doubanmovie.id'
    #    },
    #)
    #object_list = object_list.filter(entry_count__gt=0).filter(from_type=1).order_by('-rating')
    queryset = DoubanMovie.objects.filter(from_type__lte=2).annotate(cnt=Count('movielink')).filter(cnt__gt=0).order_by('-cnt')
    #queryset[0]
    #print connection.queries[-1]['sql']
    paginate_by = 25
    template_name = 'movie_home.html'
    #return object_list(request, template_name='movie_home.html', queryset=movie_list, paginate_by=25)
    #def get_queryset(self):
     #   return DoubanMovie.objects.values('movielink').filter(from_type=1).annotate(cnt=Count('movielink')).filter(cnt__gt=0).order_by('-cnt')
    
    ## Override get_context_data to add the class number to the context for use by the template
    def get_context_data(self, **kwargs):
        context = super(MovieListView, self).get_context_data(**kwargs)
        context['top_tags'] = Tag.objects.all().annotate(num_items=Count('doubanmovie')).order_by('-num_items')[0:33]
        return context

class TagListView(ListView):
    queryset = DoubanMovie.objects.filter(from_type__lte=2).annotate(cnt=Count('movielink')).filter(cnt__gt=0).order_by('-cnt')
    paginate_by = 25
    template_name = 'movie_home.html'
    
    def get_context_data(self, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        context['top_tags'] = Tag.objects.all().annotate(num_items=Count('doubanmovie')).order_by('-num_items')[0:33]
        return context

    def get_queryset(self, **kwargs):
        queryset = super(TagListView, self).get_queryset()
        return queryset.filter(tags__name__exact=self.kwargs['tags'])

def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(title_auto=request.GET.get('q', ''))[:5]
    suggestions = [result.title for result in sqs]

    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    the_data = json.dumps({
        'results': suggestions
    })
    return HttpResponse(the_data, content_type='application/json')

class NewsListView(ListView):
    queryset = MovieNews.objects.all().order_by('-id')
    paginate_by = 25
    template_name = 'news_list.html'

def NewsSubject(request, id):
    try:
        obj = MovieNews.objects.get(pk=id)
        return render_to_response('news_subject.html', {'entry':obj})
    except:
        return HttpResponse('No find!')
