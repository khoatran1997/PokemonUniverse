class Skill:
	def __init__(self,s_id,sname,element,damage):
		self.s_id = s_id
		self.sname = sname
		self.element = element
		self.damage = damage
	
	def getName(self):
		return '{}'.format(self.name)
	