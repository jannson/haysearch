# -*- coding: utf-8 -*-

import re
from django.db import models
from django.contrib.auth.models import User
import yaha
from yaha.analyse import extract_keywords

beauty_re = re.compile(ur'[\0-9\u4E00-\u9FA5]+', re.I)
accepted_chars = re.compile(ur"[\u4E00-\u9FA5]+", re.I)
html_remove = re.compile('<.*?>')
size_re = re.compile(r'\s*-\s*(\d+\.?\d*)(K|G|M)', re.I|re.M|re.U);

def title_beauty(arg, len):
    size = ''
    try:
        size = size_re.search(arg).group()
    except:
        pass
    finds = beauty_re.findall(arg)
    str = ''
    for find_str in finds:
        if accepted_chars.search(find_str):
            str += find_str + ' '
    if str == '':
        return html_remove.sub('',arg)
    return str[0:len] + size

class Tag(models.Model):
    name=models.CharField(max_length=50, unique=True)

class DoubanMovie(models.Model):
    title=models.CharField(max_length=200)
    url=models.URLField(max_length=500, blank=True)
    movie_id=models.IntegerField(blank=True)
    year = models.IntegerField()
    rating = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    votes = models.IntegerField()
    info = models.CharField(max_length=1024, blank=True)
    description=models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    from_type = models.IntegerField()
    add_date=models.DateField(auto_now_add=True)
    update_date=models.DateField(auto_now=True,auto_now_add=True)

    def movie_link_set(self):
        return MovieLink.objects.filter(douban_id=self.id).order_by('-score', '-size')[0:18]

    def key_word_list(self):
        str = self.description
        if str.strip() == '':
            str = self.title
        return extract_keywords(str, topk=16)

    def tag_list(self):
        return [tag.name for tag in self.tags.all()]

    def __unicode__(self):
        return self.title

class MovieTitle(models.Model):
    title=models.CharField(max_length=200, unique=True)
    douban = models.ForeignKey(DoubanMovie)

class MovieLink(models.Model):
    title=models.CharField(max_length=200)
    douban = models.ForeignKey(DoubanMovie)
    url=models.URLField(max_length=1024)
    #size = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    size = models.IntegerField()
    from_type=models.IntegerField()
    score=models.IntegerField()
    add_date=models.DateField(auto_now_add=True)
    update_date=models.DateField(auto_now=True,auto_now_add=True)
    def __unicode__(self):
        return self.title

class Preview(models.Model):
    description=models.TextField(blank=True)

class MovieNews(models.Model):
    title=models.CharField(max_length=200)
    url=models.URLField(max_length=200, unique=True)
    info=models.CharField(max_length=400)
    summerize=models.CharField(max_length=400)
    content=models.TextField()
    preview=models.TextField()
    
    def key_word_list(self):
        return extract_keywords(self.content, topk=8)

