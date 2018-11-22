class Skill:
	def __init__(self,s_id):# Get damage, type,name from db
		self.s_id = s_id

	
	def getName(self):
		return '{}'.format(self.name)
	