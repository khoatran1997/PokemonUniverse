import os
import random
import sqlite3

class Battle:
	def __init__(self,t_id_c,t_id_d,mode):
		# Challenger id, defender id, battle mode T/F T:auto F:pvp, database pointer
		self.t_id_c = t_id_c
		self.t_id_d = t_id_d
		self.mode = mode
		self.b_id=-1	
		db.execute('SELECT primary_cap FROM Trainer WHERE t_id=?',(t_id_c,))
		cL = db.fetchone()
		self.c_id_c= cL[0]	
		self.cPoke = bCaptured(self.c_id_c)
		db.execute('SELECT primary_cap FROM Trainer WHERE t_id=?',(t_id_d,))
		self.c_id_d = db.fetchone()[0]
		self.dPoke = bCaptured(self.c_id_d)
		self.turn=True
		self.cSkill1 = bSkill(self.cPoke.s1_id)
		self.cSkill2 = bSkill(self.cPoke.s2_id)
		self.dSkill1 = bSkill(self.dPoke.s1_id)
		self.dSkill2 = bSkill(self.dPoke.s2_id)
		self.cHP = self.cPoke.HP
		self.dHP = self.dPoke.HP
		self.header()
		
	def battle(self):
		while self.cHP>0 and self.dHP>0:
			#clear()
			
			if self.turn == True :
				self.hpBar()
				self.battlePanel(self.t_id_c, self.cPoke, self.cSkill1, self.cSkill2, self.dPoke)
				self.turn=False
			elif self.turn ==False and self.mode == False:
				self.hpBar()
				self.battlePanel(self.t_id_d, self.dPoke, self.dSkill1, self.dSkill2, self.cPoke)
				self.turn=True
			elif self.turn ==False and self.mode == True:
				self.autoBattle()	
				self.turn=True
			
	def getBattleId(self):
		return '{}'.format(self.b_id)
	
	def battlePanel(self,at_id, aPoke, skill1, skill2, dPoke):
		# 1 skill 2 item
		# 1-select skill- damage calculation
		# 2-select item- recovery
		while True:
			db.execute(""" SELECT username FROM TRAINER WHERE t_id={};
			""".format(at_id))
			print("{}'s turn.".format(db.fetchone()[0]))
			print("1-Skill 2-Item")
			in1=input("Your Choice:")
			if in1=='1':
				while True:
					print("1-{} {}".format(skill1.sname,skill1.type))
					print("2-{} {}".format(skill2.sname,skill2.type))
					print("0-Cancle")
					in2=input("Your Choice:")
					if in2=='1':
						if self.turn==True: self.dHP-=self.cal(aPoke,skill1,dPoke)
						else: self.cHP-=self.cal(aPoke,skill1,dPoke)
						print("You create Dmg:{}".format(self.cal(aPoke,skill1,dPoke)))
						return
					elif in2=='2':
						if self.turn==True: self.dHP-=self.cal(aPoke,skill2,dPoke)
						else: self.cHP-=self.cal(aPoke,skill2,dPoke)
						print("You create Dmg:{}".format(self.cal(aPoke,skill2,dPoke)))
						return	
					elif in2=='0':
						break
					else:
						print("Error: Wrong Input")	
					break						
			elif in1=='2':
				p=bPack(at_id)
				while True:
					for i in range(1,4):
						p.getNameAndNum(i)
					print("0-Cancle")
					in3=input("Your Choice:")
					if in3=='1':
						if p.num[int(in3)-1]>0:
							if self.turn==True: 
								#print("Before: {}".format(self.cHP))
								self.cHP=self.cHP+20
								#print("After: {}".format(self.cHP))
								if self.cHP>self.cPoke.HP: 
									self.cHP=self.cPoke.HP
									#print("Saturation: {}".format(self.cHP))							
							else: 
								self.dHP+=20
								if self.dHP>self.dPoke.HP: 
									self.dHP=self.dPoke.HP
								
							p.itemNumChange(int(in3), -1)
							return
						else:
							print("No portion")
							continue
					elif in3=='2':
						if p.num[int(in3)-1]>0:
							if self.turn==True: 
								self.cHP+=50
								if self.cHP>self.cPoke.HP: 
									self.cHP=self.cPoke.HP								
							else: 
								self.dHP+=50
								if self.dHP>self.dPoke.HP: 
									self.dHP=self.dPoke.HP
								
							p.itemNumChange(int(in3), -1)
							return
						else:
							print("No portion")
							continue
					elif in3=='3':
						if p.num[int(in3)-1]>0:
							if self.turn==True: 
								self.cHP+=100
								if self.cHP>self.cPoke.HP: 
									self.cHP=self.cPoke.HP
							else: 
								self.dHP+=100
								if self.dHP>self.dPoke.HP: 
									self.dHP=self.dPoke.HP
							p.itemNumChange(int(in3), -1)
							return
						else:
							print("No portion")
							continue	
					elif in3=='0':
						break
					else:
						print("Error: Wrong Input")	
					break
			else:
				print("Error: Wrong Input")
			
		
	def autoBattle(self):
		r=random.randint(0,1)
		l1=[self.dSkill1,self.dSkill2]
		self.cHP-=self.cal(self.dPoke, l1[r], self.cPoke)
		print("Enemy creates Dmg:{}".format(self.cal(self.dPoke, l1[r], self.cPoke)))
		
	def hpBar(self):
		length=50
		cLen=round(length*self.cHP/self.cPoke.HP)
		dLen=round(length*self.dHP/self.dPoke.HP)
		print("{} LV.{} {}{} {}/{}".format(self.cPoke.pname, self.cPoke.level, "#"*cLen, " "*(length-cLen), self.cHP, self.cPoke.HP),end="\n")
		print("{} LV.{} {}{} {}/{}".format(self.dPoke.pname, self.dPoke.level, "#"*dLen, " "*(length-dLen), self.dHP, self.dPoke.HP),end="\n")
		
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
		return round(((apoke.level*0.4+2)*skill.damage/50+2)*self.modifer(skill.type,dPoke.type))
	
	def battleResult(self):
		db.execute("SELECT b_id FROM Battle ORDER BY b_id DESC")
		idList=db.fetchone()
		self.b_id=idList[0]
		self.b_id+=1
		if self.cHP>0:
			db.execute("""INSERT INTO Battle VALUES
			('{0}','{2}','w'),
			('{1}','{2}','l');
			""".format(self.t_id_c,self.t_id_d,self.b_id))
			db.execute(""" SELECT username FROM TRAINER WHERE t_id={};
			""".format(self.t_id_c))
			name1=db.fetchone()[0]
			db.execute(""" SELECT username FROM TRAINER WHERE t_id={};
			""".format(self.t_id_d))
			name2=db.fetchone()[0]
			self.cPoke.level+=1
			db.execute("""UPDATE Captured
			SET level={}
			WHERE c_id={}
			""".format(self.cPoke.level,self.c_id_c))
			db.execute("""UPDATE Trainer
			SET level=level+1
			WHERE t_id={}
			""".format(self.t_id_c))			
			print("{} Wins. {} loses.".format(name1,name2))
			self.evo(self.cPoke)
		else:
			db.execute("""INSERT INTO Battle VALUES
			('{1}','{2}','w'),
			('{0}','{2}','l');
			""".format(self.t_id_c,self.t_id_d,self.b_id))	
			db.execute(""" SELECT username FROM TRAINER WHERE t_id={};
			""".format(self.t_id_c))
			name1=db.fetchone()[0]
			db.execute(""" SELECT username FROM TRAINER WHERE t_id={};
			""".format(self.t_id_d))
			name2=db.fetchone()[0]
			print("{} Wins. {} loses.".format(name2,name1))		
			if self.mode==False:
				self.dPoke.level+=1
				db.execute("""UPDATE Captured
				SET level={}
				WHERE c_id={}
				""".format(self.dPoke.level,self.c_id_d))
				db.execute("""UPDATE Trainer
				SET level=level+1
				WHERE t_id={}
				""".format(self.t_id_d))	
				self.evo(self.dPoke)
		con.commit()		
		return self.b_id
	
	def evo(self,poke):
		if poke.r_lv== None: return
		if poke.level>= poke.r_lv:
			print("{} is evolvong!".format(poke.pname))
			while True:
				ch=input("Do you want to continue?(y/n)")
				if ch=='y' or ch=='Y':
					db.execute("""UPDATE Captured
					SET p_id={}
					WHERE c_id={};""".format(poke.r_id,poke.c_id))
					db.execute("""SELECT pname
					FROM Pokemon WHERE p_id={}""".format(poke.r_id))
					clist=db.fetchone()
					name=clist[0]
					print("Congratulations! Your {} evolved into {}".format(poke.pname,name))
					#print("Pokemon:{} {}\n".format(self.p_id,clist))
					break
				elif ch=='n' or ch=='N':
					break
				else:
					print("Error: Wrong Input")
				
	def header(self):
		db.execute(""" SELECT username FROM TRAINER WHERE t_id={};
		""".format(self.t_id_c))
		name1=db.fetchone()[0]
		db.execute(""" SELECT username FROM TRAINER WHERE t_id={};
		""".format(self.t_id_d))
		name2=db.fetchone()[0]	
		print("Battle: {} VS {}".format(name1,name2))
		
	
class bCaptured:
	def __init__(self,c_id):
		self.c_id = c_id
		#self.level
		db.execute("""SELECT p_id,level FROM Captured Where c_id={};""".format(self.c_id))
		clist=db.fetchone()
		#print("Captured: {}\n".format(clist))
		#[(self.p_id,self.level)]=clist[0]
		self.p_id=clist[0]
		self.level=clist[1]
		
		db.execute("""SELECT s_id FROM Captured_Learned_Skill Where c_id={};""".format(self.c_id))
		clist=db.fetchall()	
		self.s1_id=clist[0][0]
		self.s2_id=clist[1][0]
		
		db.execute("""SELECT pname, basic_HP,basic_ATK, r_id,r_lv,type
		FROM Pokemon WHERE p_id={}""".format(self.p_id))
		clist=db.fetchone()
		#print("Pokemon:{} {}\n".format(self.p_id,clist))
		self.pname=clist[0]
		bHP=clist[1]
		bATK=clist[2]
		self.r_id=clist[3]
		self.r_lv=clist[4]
		self.ATK=int(bATK*(1+1*self.level))
		self.HP=int(bHP*(1+0.2*self.level))
		self.type=clist[5]

class bSkill:
	def __init__(self,s_id):
		db.execute("""SELECT sname, type ,damage FROM Skill WHERE s_id={}""".format(s_id))
		list=db.fetchone()
		self.sname=list[0]
		self.type=list[1]
		self.damage=list[2]
		
class bPack:
	def __init__(self,t_id):
		db.execute("""SELECT i.i_id, i.iname,o.num
		FROM Item as i NATURAL JOIN Own_Item as o
		WHERE t_id={}
		ORDER BY i.i_id
		""".format(t_id))
		self.t_id=t_id
		self.num=[]
		self.iname=[]
		clist=db.fetchall()
		#print(clist)
		for line in clist:
			self.iname.append(line[1])
			self.num.append(line[2])
	
	def itemNumChange(self,i_id,num):
		self.num[i_id-1]+=num
		db.execute("""UPDATE Own_Item
		SET num={}
		WHERE i_id={} AND t_id={}
		""".format(self.num[i_id-1],i_id,self.t_id))
		
	def getNameAndNum(self,i_id):
		if self.num[i_id-1]>0:
			print("{}: {}-{}".format(i_id,self.iname[i_id-1],self.num[i_id-1]))
		
def clear():
	if os.name == 'nt': 
		os.system('cls')
	else: 
		os.system('clear') 



#===============================================================================
con=sqlite3.connect('pokemon_world.db')
# con=sqlite3.connect(':memory:')
db=con.cursor()
# 
# 
# #===============================================================================
# # Example
# #===============================================================================
# for i in range(1,4):
# 	b=Battle(1,2,True)
# 	b.battle()
# 	print("Battle id is {}".format(b.battleResult()))
# 
# con.close()
#===============================================================================
