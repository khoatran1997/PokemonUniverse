class Battle_Prize:
	def __init__(self,trainer_id,b_id,prize_type,num):
		self.trainer_id = trainer_id
		self.b_id = b_id
		self.prize_type = prize_type
		self.num = num
	
	def getBattlePrizeType(self):
		return '{}'.format(self.prize_type)
	