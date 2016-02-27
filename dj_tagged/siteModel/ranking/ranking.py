from siteModel.models import News
from math import log
from math import sqrt
import operator
from datetime import datetime
from django.utils import timezone
import logging


'''
Base Classes
'''


# Create with a list of ranking algorithms + their weights as RankingObjects
class Ranking(object):
	ranking_object_list = []
	total_weight = 0;
	
	def __init__(self, ranking_object_list):
		self.ranking_object_list = ranking_object_list
		for ranking_obj in self.ranking_object_list:
			self.total_weight += ranking_obj.weight;

	def _evaluate(self, news):
		if self.total_weight == 0:
			return 0
		score = 0.0
		for ranking_obj in self.ranking_object_list:
			score += ranking_obj.weight/self.total_weight * ranking_obj.algo.evaluate(news)
		return score

		# highest news is first in the list

	def sort_list_of_news(self, news_list):
		news_dict = {}
		logger = logging.getLogger("django")
		for news in news_list:
			score = self._evaluate(news)
			#logger.info("Score of news " + str(score) + " " + news.title)
			news_dict[news] = score

		#http://stackoverflow.com/questions/613183/sort-a-python-dictionary-by-value
		#Apparently this is faster than news_dict, news_dict.key
		sorted_news_list_tuples = sorted(news_dict.items(), key=operator.itemgetter(1), reverse=True)
		sorted_news_list = [item[0] for item in sorted_news_list_tuples]

		#for news in sorted_news_list:
			#logger.info("Sorted news " + news.title)
		return sorted_news_list

#Composite of a weight + Ranking Algorithm
class RankingObject(object):
	weight = 0.0
	algo = None
	
	def __init__(self, fWeight, ranking_algo):
		if (fWeight < 0):
			fWeight = 0
		self.weight = fWeight
		self.algo = ranking_algo

#each one returns a score of 0->1, 0 means bad in category, 1 means very good
class RankingAlgo(object):
	
	def evaluate(self, news):
		score = self._evaluate_news(news)
		return score
		

	def _evaluate_news(self, news):
		raise NotImplemented
	
	#Not sure if this is correct. - should be converting both to UTC & then subtracting.
	def _get_news_life_since_now_in_seconds(self, news):
		return (datetime.utcnow() - news.get_creation_date().replace(tzinfo=None)).total_seconds()


'''

Examples of predefined ranking algorithm groups with weights

'''
class WilsonRanking(Ranking):
	def __init__(self):
		rank_algo = WilsonScoreRankingAlgo()
		wilson_rank = RankingObject(1.0, rank_algo)
		super(WilsonRanking, self).__init__([wilson_rank])

class NewestRanking(Ranking):
	def __init__(self):
		date_algo = RankingObject(0.9, DateRankingAlgo())
		comment_algo = RankingObject(0.1, CommentRankingAlgo())
		super(NewestRanking, self).__init__([date_algo, comment_algo])

class RisingRanking(Ranking):
	def __init__(self):
		date_algo = RankingObject(0.6, DateRankingAlgo())
		comment_algo = RankingObject(0.2, CommentRankingAlgo())
		view_algo = RankingObject(0.2, ViewRankingAlgo())
		super(RisingRanking, self).__init__([date_algo, comment_algo, view_algo])

class DateRanking(Ranking):
	def __init__(self):
		date_algo = RankingObject(1.0, DateRankingAlgo())
		super(DateRanking, self).__init__([date_algo, ])

class HotRanking(Ranking):
	def __init__(self):
		hot_algo = RankingObject(1.0, HotRankingAlgo())
		super(HotRanking, self).__init__([hot_algo, ])
'''
Ranking Algorithms
'''

#By time lived...
class DateRankingAlgo(RankingAlgo):

	CUTOFF_FACTOR = 12.0

	def _evaluate_news(self, news):
		life_seconds = self._get_news_life_since_now_in_seconds(news)
		life_hours = life_seconds / 60.0 / 60.0;
		#return ( 1.0/log(life_hours/self.CUTOFF_FACTOR) )
		return 1.0 / life_hours

class RatingRankingAlgo(RankingAlgo):
	def _evaluate_news(self, news):
		return news.get_ups() - news.get_downs()

#By comments per hr
class CommentRankingAlgo(RankingAlgo):
	MAX_SCORE_COMMENTS_PER_HOUR = 100

	def _evaluate_news(self, news):
		life_seconds = self._get_news_life_since_now_in_seconds(news)
		life_hours = life_seconds / 60.0 / 60.0;
		if (life_hours == 0):
			life_hours = 0.1
		comments_per_hour = news.num_comments / life_hours
		return (comments_per_hour / self.MAX_SCORE_COMMENTS_PER_HOUR)

#By views.
class ViewRankingAlgo(RankingAlgo):
	MAX_SCORE_VIEWS_PER_HOUR = 500

	def _evaluate_news(self, news):
		life_seconds = self._get_news_life_since_now_in_seconds(news)
		life_hours = life_seconds / 60.0 / 60.0;
		if (life_hours == 0):
			life_hours = 0.1
		views_per_hour = news.num_comments / life_hours
		return (views_per_hour / self.MAX_SCORE_VIEWS_PER_HOUR)
		
class WilsonScoreRankingAlgo(RankingAlgo):
	def _evaluate_news(self, news):
		total_votes = news.get_ups() + news.get_downs()
		if (total_votes == 0):
			return 0
		z = 1.0 #1.0 = 85%, 1.6 = 95%
		phat = float(news.get_ups()) / total_votes
		return (phat+z*z/(2*total_votes)-z*sqrt((phat*(1-phat)+z*z/(4*total_votes))/total_votes)) / (1+z*z/total_votes)



def time_since_epoch_seconds(date):
	epoch = datetime(1970, 1, 1)
	delta = date.replace(tzinfo=None) - epoch
	return delta.days * 86400 + delta.seconds + (float(delta.microseconds) / 1000000)

class HotRankingAlgo(RankingAlgo):
	def _evaluate_news(self, news):
		vote_score = news.get_ups() - news.get_downs()
		order = log(max(abs(vote_score), 1), 2)
		sign = 0
		if (vote_score > 0):
			sign = 1
		elif (vote_score == 0):
			sign = 0
		else:
			sign = -1
		seconds = time_since_epoch_seconds(news.get_creation_date()) - 1454102930
		return round(sign * order + seconds / 45000, 7)

		
# encoding: utf-8

import re
import urllib
try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup

global import_json
try:
    import json
    import_json = True
except ImportError:
    import_json = False

class WhyCantIImportOpenGraph(dict):
    """
    """

    required_attrs = ['title', 'type', 'image', 'url']
    scrape = False

    def __init__(self, url=None, html=None, scrape=False, **kwargs):
        # If scrape == True, then will try to fetch missing attribtues
        # from the page's body
        self.scrape = scrape
        self._url = url

        for k in kwargs.keys():
            self[k] = kwargs[k]
        
        dict.__init__(self)
                
        if url is not None:
            self.fetch(url)
            
        if html is not None:
            self.parser(html)

    def __setattr__(self, name, val):
        self[name] = val

    def __getattr__(self, name):
        return self[name]
            
    def fetch(self, url):
        """
        """
        raw = urllib.urlopen(url)
        html = raw.read()
        return self.parser(html)
        
    def parser(self, html):
        """
        """
        if not isinstance(html,BeautifulSoup):
            doc = BeautifulSoup(html)
        else:
            doc = html
        ogs = doc.html.head.findAll(property=re.compile(r'^og'))
        for og in ogs:
            self[og[u'property'][3:]]=og[u'content']

        # Couldn't fetch all attrs from og tags, try scraping body
        if not self.is_valid() and self.scrape:
            for attr in self.required_attrs:
                if not hasattr(self, attr):
                    try:
                        self[attr] = getattr(self, 'scrape_%s' % attr)(doc)
                    except AttributeError:
                        pass
        
    def is_valid(self):
        return all([hasattr(self, attr) for attr in self.required_attrs])
        
    def to_html(self):
        if not self.is_valid():
            return u"<meta property=\"og:error\" content=\"og metadata is not valid\" />"
            
        meta = u""
        for key,value in self.iteritems():
            meta += u"\n<meta property=\"og:%s\" content=\"%s\" />" %(key, value)
        meta += u"\n"
        
        return meta
        
    def to_json(self):
        # TODO: force unicode
        global import_json
        if not import_json:
            return "{'error':'there isn't json module'}"

        if not self.is_valid():
            return json.dumps({'error':'og metadata is not valid'})
            
        return json.dumps(self)
        
    def to_xml(self):
        pass

    def scrape_image(self, doc):
        images = [dict(img.attrs)['src'] 
            for img in doc.html.body.findAll('img')]

        if images:
            return images[0]

        return u''

    def scrape_title(self, doc):
        return doc.html.head.title.text

    def scrape_type(self, doc):
        return 'other'

    def scrape_url(self, doc):
        return self._url
