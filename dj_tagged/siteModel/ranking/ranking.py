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
			logger.info("Score of news " + str(score) + " " + news.title)
			news_dict[news] = score

		#http://stackoverflow.com/questions/613183/sort-a-python-dictionary-by-value
		#Apparently this is faster than news_dict, news_dict.key
		sorted_news_list_tuples = sorted(news_dict.items(), key=operator.itemgetter(1))
		sorted_news_list = [item[0] for item in sorted_news_list_tuples]

		for news in sorted_news_list:
			logger.info("Sorted news " + news.title)
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

'''
Ranking Algorithms
'''

#By time lived...
class DateRankingAlgo(RankingAlgo):

	CUTOFF_FACTOR = 12.0

	def _evaluate_news(self, news):
		logger = logging.getLogger("django");
                logger.info("Using date ranking");
                life_seconds = self._get_news_life_since_now_in_seconds(news)
		life_hours = life_seconds / 60.0 / 60.0;
		return ( 1.0/log(life_hours/self.CUTOFF_FACTOR) )

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
		
# i got no idea what this returns. XD
class WilsonScoreRankingAlgo(RankingAlgo):
	def _evaluate_news(self, news):
                logger = logging.getLogger("django")
                logger.info("USing wilson rankning")
		total_votes = news.upvotes + news.downvotes
		if (total_votes == 0):
			return 0
		z = 1.0 #1.0 = 85%, 1.6 = 95%
		phat = float(news.get_ups()) / total_votes
		return (phat+z*z/(2*total_votes)-z*sqrt((phat*(1-phat)+z*z/(4*total_votes))/total_votes)) / (1+z*z/total_votes)
		
