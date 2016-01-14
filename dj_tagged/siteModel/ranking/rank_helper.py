from siteModel.ranking.ranking import *


# Create with a list of ranking algorithms + their weights as RankingObjects
class RankHelper(object):
	@staticmethod
	def parse_rank_style(rank_style):
		rankAlgo = None
		if (rank_style == 'Newest'):
			rankAlgo = DateRanking()
		else:
			rankAlgo = WilsonRanking()
			return rankAlgo