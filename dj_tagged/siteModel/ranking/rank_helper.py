from siteModel.ranking.ranking import *


# Create with a list of ranking algorithms + their weights as RankingObjects
class RankHelper(object):
	@staticmethod
	def parse_rank_style(rank_style):
		rankAlgo = None
		if (rank_style == 'Newest'):
			rankAlgo = DateRanking()
		elif (rank_style == 'Wilson'):
			rankAlgo = WilsonRanking()
		else:
			rankAlgo = HotRanking()
		return rankAlgo
