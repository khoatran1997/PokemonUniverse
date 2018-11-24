from skill import Skill
from pokemon import Captured
from item import Pocket
import os
import random

class Battle:
	def __init__(self,t_id_c,t_id_d,mode,db):
		# Challenger id, defender id, battle mode T/F T:auto F:pvp, database pointer
		self.t_id_c = t_id_c
		self.t_id_d = t_id_d
		self.mode = mode
		self.b_id=-1
		self.db=db		
		#=======================================================================
		# db.excute('SELECT primary_cap FROM Trainer WHERE t_id=?',(t_id_c,))
		# self.c_id_c = db.fatchall()
		# self.cPoke = Captured(self.c_id_c)
		# db.excute('SELECT primary_cap FROM Trainer WHERE t_id=?',(t_id_d,))
		# self.c_id_d = db.fatchall()
		# self.dPoke = Captured(self.c_id_d)
		# self.turn=True
		# db.excute('SELECT s_id FROM Captured_Learned_Skill WHERE c_id=?',(self.c_id_c,))
		# self.cSkill1 = Skill(db.fatchone())
		# self.cSkill2 = Skill(db.fatchone())
		# db.excute('SELECT s_id FROM Captured_Learned_Skill WHERE c_id=?',(self.c_id_d,))
		# self.dSkill1 = Skill(db.fatchone())
		# self.dSkill2 = Skill(db.fatchone())
		#=======================================================================
		self.c_id_c=self.t_id_c.primary_cap
		self.c_id_d=self.t_id_d.primary_cap
		# How to get pure value
		self.cSkill1 = Skill(db.fatchone())
		self.cSkill2 = Skill(db.fatchone())		
		self.cHP = self.cPoke.HP
		self.dHP = self.dPoke.HP
		
	def battle(self):
		while self.cHP>0 and self.dHP>0:
			clear()
			self.hpBar()
			if self.turn == True :
				self.battlePanel(self.t_id_c, self.cPoke, self.cSkill1, self.cSkill2, self.dPoke)
			
			elif self.turn ==False and self.mode == False:
				self.battlePanel(self.t_id_d, self.dPoke, self.dSkill1, self.dSkill2, self.cPoke)
			
			elif self.turn ==False and self.mode == True:
				self.autoBattle()	
			
	def getBattleId(self):
		return '{}'.format(self.b_id)
	
	def battlePanel(self,at_id, aPoke, skill1, skill2, dPoke):
		# 1 skill 2 item
		# 1-select skill- damage calculation
		# 2-select item- recovery
		while True:
			print("1-Skill 2-Item\n")
			in1=input("Your Choice:")
			if in1==1:
				while True:
					print("1-{} {}\n".format(skill1.name,skill1.type))
					print("2-{} {}\n".format(skill2.name,skill2.type))
					print("0-Cancle\n")
					in2=input("Your Choice:")
					if in2==1:
						if self.turn==True: self.dHP-=self.cal(aPoke,skill1,dPoke)
						else: self.cHP-=-self.cal(aPoke,skill1,dPoke)
						break
					elif in2==2:
						if self.turn==True: self.dHP-=self.cal(aPoke,skill2,dPoke)
						else: self.cHP-=-self.cal(aPoke,skill2,dPoke)
						break	
					elif in2==0:
						break
					else:
						print("Error: Wrong Input\n")							
			elif in1==2:
				p=Pocket(at_id)
				while True:
					for i in range(1,3):
						p.getNameAndNum(i)
					print("0-Cancle\n")
					in3=input("Your Choice:")
					if in3==1:
						if self.turn==True: self.cHP+=20
						else: self.dHP+=20
						p.itemNumChange(in3, -1)
						break
					elif in3==2:
						if self.turn==True: self.cHP+=50
						else: self.dHP+=50
						p.itemNumChange(in3, -1)
						break
					elif in3==3:
						if self.turn==True: self.cHP+=100
						else: self.dHP+=100
						p.itemNumChange(in3, -1)
						break		
					elif in3==0:
						break
					else:
						print("Error: Wrong Input\n")	
			else:
				print("Error: Wrong Input\n")
		
	def autoBattle(self):
		r=random.randint(0,1)
		l1=[self.dSkill1,self.dSkill2]
		self.cHP-=self.cal(self.dPoke, l1[r], self.cPoke)
		
	def hpBar(self):
		length=50
		cLen=round(length*self.cHP/self.cPoke.HP)
		dLen=round(length*self.dHP/self.dPoke.HP)
		print("{} LV.{} {}{} {}/{}".format(self.cPoke.name, self.cPoke.lv, "#"*cLen, " "*(length-cLen), self.cHP, self.cPoke.HP),end="\n")
		print("{} LV.{} {}{} {}/{}".format(self.dPoke.name, self.dPoke.lv, "#"*dLen, " "*(length-dLen), self.dHP, self.dPoke.HP),end="\n")
		
	def modifer(self, aT, dT):
		mod=1
		if aT=="Grass" and (dT=="Water" or dT=="Electric"): mod=1.5
		if aT=="Grass" and (dT=="Fire" or dT=="Grass"): mod=0.5
		if aT=="Fire" and (dT=="Grass"): mod=1.5
		if aT=="Fire" and (dT=="Water" or dT=="Fire"): mod=0.5
		if aT=="Water" and (dT=="Fire"): mod=1.5
		if aT=="Water" and (dT=="Grass" or dT=="Water"): mod=0.5
		if aT=="Ice" and (dT=="Grass"): mod=1.5
		if aT=="Ice" and (dT=="Fire" or dT=="Water"): mod=0.5
		if aT=="Electric" and (dT=="Water"): mod=1.5
		if aT=="Electric" and (dT=="Grass" or dT=="Electric"): mod=0.5
		if aT=="Dark" and (dT=="Psychic"): mod=1.5
		if aT=="Psychic" and (dT=="Psychic"): mod=0.5
		if aT=="Fighting" and (dT=="Normal"): mod=1.5
		if aT=="Fighting" and (dT=="Psychic"): mod=0.5
		return mod
	
	def cal(self,apoke,skill,dPoke):		
		return round(((apoke.lv*0.4+2)*skill.damage/50+2)*self.modifer(skill.type,dPoke.type))
	
	def battleResult(self):
		self.db.execute("SELECT b_id FROM Battle")
		idList=self.db.fatchall()
		self.b_id=max(idList)
		self.b_idb_id+=1
		if self.cHP>0:
			self.db.execute("""INSERT INTO Battle VALUES
			('{0}','{2}','w'),
			('{1}','{2}','l');
			""".format(self.t_id_c,self.t_id_d,self.b_id))
		else:
			self.db.execute("""INSERT INTO Battle VALUES
			('{1}','{2}','w'),
			('{0}','{2}','l');
			""".format(self.t_id_c,self.t_id_d,self.b_id))			
		self.db.commit()
		return self.b_id
		
def clear():
	if os.name == 'nt': 
		os.system('cls')
	else: 
		os.system('clear') 
		
		
b=Battle()
b.battle()
b.battleResult()	