class Item:
	def __init__(self,i_id,iname,price,function):
		self.i_id = i_id
		self.iname = iname
		self.price = price
		self.function = function
	
	def getName(self):
		return '{}'.format(self.name)
	