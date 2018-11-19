class Gym:
	def __init__(self,g_id,gname,l_id,leader_id):
		self.g_id = g_id
		self.gname = gname
		self.l_id = l_id 				#location
		self.leader_id = leader_id		#leader
	
	def getGymName(self):
		return '{}'.format(self.name)
	