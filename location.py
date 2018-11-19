class Location:
	def __init__(self,l_id,lname,coordinate):
		self.l_id = l_id
		self.lname = lname
		self.coordinate = coordinate
	
	def getCoordinate(self):
		return '{}'.format(self.coordinate)
	