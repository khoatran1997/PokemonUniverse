class Item:
    def __init__(self,i_id):
    # Input: i_id
    # Get varible from DB: iname, price, function
        self.i_id = i_id


    def getName(self):
        return '{}'.format(self.name)


class Pocket:
    def _init_(self,t_id):
        self.t_id=t_id

    def itemNumChange(self,i_id,num):
    # Input t_id, i_id, num
    #Funtion: Make number of item i_id in t_id's bag change
        pass

    def getNameAndNum(self, i_id):
    # Return item  name and num
        pass
