from siteModel.models import News
from math import log

class Ranking(object):
	rankingObjectList = []
	totalWeight = 0;
	
	def __init__(self, rankingObjectList):
		self.rankingObjectList = rankingObjectList
		for rankingObj in self.rankingObjectList
			totalWeight += rankingObj.weight;

	def evaluate(self, news):
		if totalWeight == 0:
			return 0
		score = 0.0
		for rankingObj in rankingObjectList:
			score += rankingObj.weight/self.totalWeight * rankingObj.algo.evaluate(news)
		return score

class RankingObject(object):
	weight = 0.0f
	algo = None
	
	def __init__(self, fWeight, rankingAlgo):
		if (fWeight < 0):
			fWeight = 0
		self.weight = fWeight
		self.algo = rankingAlgo

class RankingAlgo(object):
	MAX_SCORE = 100
	MIN_SCORE = 0
	
	def evaluate(self, news):
		score = self._evaluateNews(news)
		if (score > self.MAX_SCORE):
			score = self.MAX_SCORE
		if (score < self.MIN_SCORE):
			score = self.MIN_SCORE
		return score
		

	def _evaluateNews(self, news):
		raise NotImplemented
	
	def _getNewsLifeSinceNowInSeconds(self, news):
		return (timezone.now - news.date_created).total_seconds()

class DateRankingAlgo(RankingAlgo):

	CUTOFF_FACTOR = 12.0

	def _evaluateNews(self, news):
		lifeSeconds = self._getNewsLifeSinceNowInSeconds(news)
		lifeHours = lifeSeconds / 60.0 / 60.0;
		return ( 1.0/log(lifeHours/self.CUTOFF_FACTOR) ) * 100

class RatingRankingAlgo(RankingAlgo):
	def _evaluateNews(self, news):
		return news.upvotes - news.downvotes

class CommentRankingAlgo(RankingAlgo):
	MAX_SCORE_COMMENTS_PER_HOUR = 100

	def _evaluateNews(self, news):
		lifeSeconds = self._getNewsLifeSinceNowInSeconds(news)
		lifeHours = lifeSeconds / 60.0 / 60.0;
		if (lifeHours == 0)
			lifeHours = 0.1
		commentsPerHour = news.num_comments / lifeHours
		return (commentsPerHour / self.MAX_SCORE_COMMENTS_PER_HOUR) * 100

class ViewRankingAlgo(RankingAlgo):
	MAX_SCORE_VIEWS_PER_HOUR = 500

	def _evaluateNews(self, news):
		lifeSeconds = self._getNewsLifeSinceNowInSeconds(news)
		lifeHours = lifeSeconds / 60.0 / 60.0;
		if (lifeHours == 0)
			lifeHours = 0.1
		viewsPerHour = news.num_comments / lifeHours
		return (viewsPerHour / self.MAX_SCORE_VIEWS_PER_HOUR) * 100
		

