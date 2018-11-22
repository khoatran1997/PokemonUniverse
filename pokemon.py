class Pokemon:
	def __init__(self,p_id):
		# Input: p_id
		# Get varible from DB: pname,basic_HP,basic_ATK,type
		self.p_id = p_id

	def getType(self):
		return '{}'.format(self.type)

class Wild(Pokemon):
	def __init__(self,p_id,pname,basic_HP,basic_ATK,type,w_id,level,l_id):
		super().__init__(p_id,pname,basic_HP,basic_ATK,type)
		self.w_id = w_id
		self.level = level
		self.l_id = l_id

class Captured(Pokemon):
	def __init__(self,c_id):
		# Input: c_id
		# Get veriable from DB: p_id, name, lv, type, s_id1, s_id2(Captured only has 2 skills),exp, t_id
		# Derive veriable: ATK=basic_ATK*(1+0.5*lv), HP=basic_HP*(1+0.7*lv)	
		self.c_id = c_id
		super().__init__(self.p_id)