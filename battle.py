class Battle:
	def __init__(self,trainer_id,b_id,outcome):
		self.trainer_id = trainer_id
		self.b_id = b_id
		self.outcome = outcome
	
	def getBattleId(self):
		return '{}'.format(self.b_id)
	