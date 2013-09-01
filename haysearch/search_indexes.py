from models import *
from django.db.models import Count
from haystack import indexes

class DoubanMovieIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(boost=4.0)
    tags = indexes.MultiValueField()
    doc_score = indexes.IntegerField(stored=True, indexed=False)
    #auto complete
    title_auto = indexes.EdgeNgramField()

    def get_model(self):
        return DoubanMovie

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(id__lte=16000).annotate(cnt=Count('movielink')).filter(cnt__gt=0).order_by('-cnt')

    def prepare_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]
   
    def prepare_title(self,obj):
        if obj.from_type <= 64:
            return obj.title
        else:
            return ""

    def prepare_title_auto(self, obj):
        str = obj.title+' '+obj.info
        return str.strip()

    def prepare_doc_score(self, obj):
        score = 10
        try:
            movie_link = MovieLink.objects.filter(douban_id=obj.id).order_by('-score')[0]
            #Origin score
            score = movie_link.score
            if score >= 80:
                score = 100
            elif movie_link.size > 3*1000*1000:
                score = 70
            elif movie_link.size > 1*1000*1000:
                score = 60
            elif movie_link.size > 600*1000:
                score = 50
            elif movie_link.size > 200*1000:
                score = 40
            elif movie_link.size > 50*1000:
                score = 20
            else:
                score = 10
        except:
            pass
        #if obj.rating > 0:
        #    score = float(score*(1+obj.rating/20))
        self.prepared_data['_boost'] = score*0.05
        return score

    def prepare(self, obj):
        self.prepared_data = super(DoubanMovieIndex, self).prepare(obj)
        self.prepared_data['_title_boost'] = 4.0

        return self.prepared_data
