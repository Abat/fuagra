from siteModel.models import News
from math import log
import operator

#Composite of a weight + Ranking Algorithm
class RankingObject(object):
	weight = 0.0
	algo = None
	
	def __init__(self, fWeight, rankingAlgo):
		if (fWeight < 0):
			fWeight = 0
		self.weight = fWeight
		self.algo = rankingAlgo

# Create with a list of ranking algorithms + their weights as RankingObjects
class Ranking(object):
	rankingObjectList = []
	totalWeight = 0;
	
	def __init__(self, rankingObjectList):
		self.rankingObjectList = rankingObjectList
		for rankingObj in self.rankingObjectList:
			self.totalWeight += rankingObj.weight;

	def evaluate(self, news):
		if self.totalWeight == 0:
			return 0
		score = 0.0
		for rankingObj in self.rankingObjectList:
			score += rankingObj.weight/self.totalWeight * rankingObj.algo.evaluate(news)
		return score

		# highest news is first in the list

	def sortListOfNews(self, newsList):
		newsDict = {}
		for news in newsList:
			score = self.evaluate(news)
			newsDict[news] = score

		#http://stackoverflow.com/questions/613183/sort-a-python-dictionary-by-value
		#Apparently this is faster than newsDict, newsDict.key
		sortedNewsList = sorted(newsDict.items(), key=operator.itemgetter(1))
		return sortedNewsList

class WilsonRanking(Ranking):
	def __init__(self):
		rankAlgo = WilsonScoreRankingAlgo()
		wilsonRank = RankingObject(1.0, rankAlgo)
		super(WilsonRanking, self).__init__([wilsonRank])

#each one returns a score of 0->100, 100 meaning that obj is really good in that category
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

#By time lived...
class DateRankingAlgo(RankingAlgo):

	CUTOFF_FACTOR = 12.0

	def _evaluateNews(self, news):
		lifeSeconds = self._getNewsLifeSinceNowInSeconds(news)
		lifeHours = lifeSeconds / 60.0 / 60.0;
		return ( 1.0/log(lifeHours/self.CUTOFF_FACTOR) ) * 100

class RatingRankingAlgo(RankingAlgo):
	def _evaluateNews(self, news):
		return news.upvotes - news.downvotes

#By comments per hr
class CommentRankingAlgo(RankingAlgo):
	MAX_SCORE_COMMENTS_PER_HOUR = 100

	def _evaluateNews(self, news):
		lifeSeconds = self._getNewsLifeSinceNowInSeconds(news)
		lifeHours = lifeSeconds / 60.0 / 60.0;
		if (lifeHours == 0):
			lifeHours = 0.1
		commentsPerHour = news.num_comments / lifeHours
		return (commentsPerHour / self.MAX_SCORE_COMMENTS_PER_HOUR) * 100

#By views.
class ViewRankingAlgo(RankingAlgo):
	MAX_SCORE_VIEWS_PER_HOUR = 500

	def _evaluateNews(self, news):
		lifeSeconds = self._getNewsLifeSinceNowInSeconds(news)
		lifeHours = lifeSeconds / 60.0 / 60.0;
		if (lifeHours == 0):
			lifeHours = 0.1
		viewsPerHour = news.num_comments / lifeHours
		return (viewsPerHour / self.MAX_SCORE_VIEWS_PER_HOUR) * 100
		
# i got no idea what this returns. XD
class WilsonScoreRankingAlgo(RankingAlgo):
	def _evaluateNews(self, news):
		totalVotes = news.upvotes + news.downvotes
		if (totalVotes == 0):
			return 0
		z = 1.0 #1.0 = 85%, 1.6 = 95%
		phat = float(news.upvotes) / totalVotes
		return (phat+z*z/(2*n)-z*sqrt((phat*(1-phat)+z*z/(4*n))/n)) / (1+z*z/n)
		