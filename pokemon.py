class Pokemon:
	def __init__(self,p_id,pname,basic_HP,basic_ATK,type):
		self.p_id = g_id
		self.pname = gname
		self.basic_HP = basic_HP
		self.basic_ATK = basic_ATK
		self.type = type
	
	def getType(self):
		return '{}'.format(self.type)

class Wild(Pokemon):
	def __init__(self,p_id,pname,basic_HP,basic_ATK,type,w_id,level,l_id):
		super().__init__(p_id,pname,basic_HP,basic_ATK,type)
		self.w_id = w_id
		self.level = level
		self.l_id = l_id

class Captured(Pokemon):
	def __init__(self,p_id,pname,basic_HP,basic_ATK,type,c_id,level,pw_id):
		super().__init__(p_id,pname,basic_HP,basic_ATK,type)
		self.c_id = c_id
		self.level = level
		self.pw_id = pw_id