class Trainer:
	def __init__(self,t_id,username,level,coin,vl_id,hl_id,primary_cap):
		self.t_id = t_id
		self.username = username
		self.level = level
		self.coin = coin
		self.vl_id = vl_id #visit location
		self.hl_id = hl_id #hometown location
		self.primary_cap = primary_cap
	def getLevel(self):
		return '{}'.format(self.level)
	captured_pokemon = list()
