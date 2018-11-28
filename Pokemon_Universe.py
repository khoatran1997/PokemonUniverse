import sqlite3
from trainer import Trainer
from pokemon import Pokemon, Captured
from battle import Battle
import sys
from random import randint
# from battle import Battle

con=sqlite3.connect('pokemon_world.db')
# con = sqlite3.connect(':memory:')
db = con.cursor()

def addTrainer(trnr):
    try:
        with con:
            db.execute("""INSERT INTO Trainer VALUES
                       (:t_id,:username,:level,:coin,:vl_id,:hl_id,:primary_cap)"""
                       , {'t_id': trnr.t_id,    'username': trnr.username,
                          'level': trnr.level,  'coin': trnr.coin,
                          'vl_id': trnr.vl_id,  'hl_id': trnr.hl_id,
                          'primary_cap': trnr.primary_cap})
    except sqlite3.IntegrityError as e:
        con.rollback()
        con.close()
        raise e

def getAllTrainernames():
    db.execute("SELECT username,t_id FROM Trainer")
    return db.fetchall()

def getTrainerInfo(trnr):
    db.execute("SELECT t_id, username, level, coin FROM Trainer")
    return db.fetchall()

def addPokemon(pkm):
    with con:
        db.execute("""INSERT INTO Pokemon VALUES
            (:p_id,:pname,:basic_HP,:basic_ATK,:type,:r_id,:r_lv)"""
            ,{'p_id': pkm.p_id,    'pname': pkm.pname,
              'basic_HP': pkm.basic_HP,  'basic_ATK': pkm.basic_ATK,
              'type': pkm.type,  'r_id': pkm.r_id,
              'r_lv': pkm.r_lv})

def update_trainer(t):
    with con:
        db.execute("""UPDATE Trainer
                      SET level = :level, coin = :coin, vl_id = :vl_id
                      WHERE t_id = :t_id""",
                    {'level': t.level, 'coin': t.coin, 'vl_id': t.vl_id})

def add_wild(w):
    with con:
        db.execute("INSERT INTO Wild VALUES (:p_id, :w_id, :level, :l_id)",
            {'p_id': w.p_id, 'w_id': w.w_id, 'level': w.level, 'l_id': w.l_id})

def del_wild(wd):
	with con:
		db.execute("DELETE FROM Wild WHERE w_id = :w_id",
			{'w_id': wd.w_id})


def captured_pokemon_names(trainer):
    db.execute("""
               SELECT pname, c_id, level
               FROM Captured NATURAL JOIN Pokemon
               WHERE t_id = :t_id """,
               {'t_id': trainer.t_id})
    count = 1
    pokemon_list = db.fetchall()
    for row in pokemon_list:
        print("\t\t{0}. {1}: lvl - {2}".format(count, row[0], row[2]))
        count += 1
    return pokemon_list

def update_primary(trainer, c_id):
    db.execute("""
               UPDATE Trainer
               SET primary_cap = :c_id
               WHERE t_id = :t_id """,
               {'c_id': c_id, 't_id': trainer.t_id})
    trainer.primary_cap = c_id

def set_primary_pokemon(trainer):
    try:
        with con:
            while True:
                print("...Primary Pokemon Menu...\n")
                print("\tCurrent primary Pokemon:")
                display_primary_pokemon_name(trainer)
                print("\tSelect primary Pokemon:")

                pokemon_list = captured_pokemon_names(trainer)

                while True:
                    op = int(input("Enter Option: "))
                    if op > len(pokemon_list) or op < 1:
                        print("\n\tInvalid option, "
                              "choose a primary pokemon from the list\n")
                    else:
                        break

                c_id = pokemon_list[op - 1][1]

                update_primary(trainer, c_id)

                print("\n\tNew primary Pokemon:")
                display_primary_pokemon_name(trainer)

                print("\t1. Choose a different primary pokemon\n\t"
                      "2. Return to Player Menu ")
                op2 = int(input("Enter Option: "))
                if op2 == 1:
                    continue
                if op2 == 2:
                    break
                else:
                    print("\n\tInvalid option,"
                          "choose a primary pokemon from the list\n")

    except sqlite3.IntegrityError as e:
        con.rollback()
        raise e


def display_primary_pokemon_name(trainer):
    db.execute("""
              SELECT pname
              FROM Trainer T JOIN Captured C ON T.t_id = C.t_id
              JOIN Pokemon P ON P.p_id = C.p_id
              WHERE C.t_id = :t_id AND
              T.primary_cap = C.c_id""",
               {'t_id': trainer.t_id})
    pokemon = db.fetchone()
    print("\t\t{}\n".format(pokemon[0]))


def add_captured(p_id, c_id, t_id):
    db.execute("""
                INSERT INTO Captured(p_id, c_id, t_id)
                VALUES
                (?, ?, ?)""", (p_id, c_id, t_id))

def battle_prize(t_id, b_id):
    db.execute("""
                UPDATE Trainer
                SET Coin = Coin + 5000
                WHERE t_id = ?""", (t_id,))
    db.execute("""
                INSERT INTO Battle_Prize
                VALUES (?, ? ,? ,?)""", (t_id , b_id, "Coin", 5000))

AllTrainers = getAllTrainernames()
print("Hello Pokemon Universe")
print(AllTrainers)

def adminMenu():
    loggedIn = True
    while loggedIn:
        print('..............................................')
        print('...................Admin Menu.................')
        print("""
            1. View Trainer Table
            2. Remove A Trainer
            3. Log Out
            """)
        op = int(input('Enter Option: '))
        if op == 1:
            db.execute('SELECT * FROM Trainer')
            print(db.fetchall())
        elif op == 2:
            delete_trainer_id = int(input('Trainer ID: '))
            delete_trainer_name = str(input('Trainer Name: '))
            with con:
                db.execute("""DELETE FROM Trainer
                              WHERE t_id =?
                              AND username =?""",
                           (delete_trainer_id, delete_trainer_name, ))
        elif op == 3:
            loggedIn = False
        else:
            print('Invalid Option')

def isUniqueUsername(newusername):
    db.execute("SELECT * FROM Trainer WHERE username = ?",(newusername,))
    tempList = db.fetchone()
    if not tempList:    #username ok
        return True
    else:
        return False
def addItemToTrainer(trnr):
    randnum = randint(1,5)
    with con:
        for i in range(1,6):
            db.execute("""INSERT INTO Own_Item VALUES (:i_id,:t_id,:num)
                    """,{'i_id':i,'t_id':trnr.t_id,'num':randnum})

def signUp():
    print('..............................................')
    print('....................Sign Up...................')
    done = False
    while done is False:
        username = str(input('Username: '))
        if isUniqueUsername(username):
            db.execute("SELECT MAX(t_id) FROM Trainer")
            currentMaxTrainerID = db.fetchone()    #Use to calculate t_id when player sign up
            userid = int(currentMaxTrainerID[0]) + 1
            db.execute('SELECT l_id, lname FROM Location WHERE lname IS NOT NULL')
            locList = db.fetchall()
            for x in locList:
                print(x)
            hometown = str(input('Hometown: '))
            done = True
            # Create new trainer object
            new_trainer = Trainer(userid, username, 1, 1000, None, hometown, None)
            # Add new trainer to table
            tutorial(new_trainer)
            addTrainer(new_trainer)
            addItemToTrainer(new_trainer)
            signedInSuccessfully(new_trainer)
        else:
            print("Username Already Exists. Try Another One!")

def update_gymleader(tid, lid):
        db.execute("""UPDATE Gym
                      SET leader_id = :t_id
                      WHERE l_id = :loc_id""",
                    {'t_id': tid, 'loc_id': lid})

def visitLocation(trnr):
    db.execute('SELECT l_id, lname FROM Location WHERE lname IS NOT NULL')
    locList = db.fetchall()
    for x in locList:
        print(x)
    Goto = str(input('Enter Location ID: '))
    print('..............................................')
    print('.............Current Location: ', Goto,'............')
    # List Wild Pokemons
    db.execute("""SELECT w_id,pname,level FROM Wild AS w JOIN Pokemon AS p
                ON w.p_id = p.p_id AND l_id = ?""", (Goto,))
    wildList = db.fetchall()
    for x in wildList:
        print(x)

    # List Item
    db.execute("""SELECT r.i_id,iname,funct FROM Item AS i JOIN Refresh_Item AS r
                ON i.i_id = r.i_id AND l_id = ?""", (Goto,))
    itemList = db.fetchall()
    for x in itemList:
        print(x)

    # List Gym
    goBack = False
    while goBack is False:
        print("Gym ID | Gym Name | Leader ID | Leader Name")
        db.execute("SELECT g.g_id, g.Gname, g.leader_id, t.username FROM gym g INNER JOIN location l ON g.l_id = l.l_id LEFT JOIN trainer t ON t.t_id = g.leader_id WHERE g.l_id = ?", (Goto,))
        gymName = db.fetchone()
        print(gymName)
        print("""
            1. Capture Pokemon
            2. Pick Up Item
            3. Take Over Gym
            4. Back to Player Menu
            """)
        op = int(input('Enter Option: '))
        if op == 1: # capture pokemon
            wildID = int(input("Enter Wild Pokemon Id: "))
            db.execute("SELECT num FROM Own_Item WHERE i_id=4 AND t_id=?",(trnr.t_id,))
            remainPokeBall = db.fetchone()
            db.execute("SELECT num FROM Own_Item WHERE i_id=5 AND t_id=?",(trnr.t_id,))
            remainMasterBall = db.fetchone()
            doneTrying = False
            while doneTrying is False:
                print("Remaining Items: ")
                print("1. Poke Ball Count: ",remainPokeBall[0])
                print("2. Master Ball Count: ",remainMasterBall[0])
                print("3. Exit Catching")
                op=int(input("Enter Item to use: "))
                if op == 2: #100% success rate
                    if int(remainMasterBall[0]) == 0:
                        print("You ran out of this item")
                    else:
                        decrementItemCount(5,trnr.t_id) #master ball
                        wild_to_captured(wildID,trnr.t_id)
                        print("Pokemon captured successfully")
                        doneTrying = True
                elif op == 1: #regular Poke Ball
                    while True:
                        if int(remainPokeBall[0]) <= 0:
                            print("You ran out of this item")
                            doneTrying = True
                            break
                        else:
                            decrementItemCount(4,trnr.t_id) #regular ball
                            chance = randint(0,1)           #50% chance
                            if chance == 1: #success
                                wild_to_captured(wildID,trnr.t_id)
                                print("Pokemon captured successfully")
                                doneTrying = True
                                break
                            elif chance == 0: #fail
                                keepTrying = str(input("Catching Attempt Failed! Continue?(Y/N)"))
                                if keepTrying == 'Y':
                                    continue
                                elif keepTrying == 'N':
                                    break
                elif op == 3:
                    doneTrying = True
                else:
                    print("Invalid Option!")
        elif op == 2: # pick up item
            itemID = int(input("Enter Item Id: "))
            pickUpItem(itemID,trnr.t_id, Goto)
            print("Item has been picked up")
        elif op == 3:
            if gymName is None:
                print("No Gym in this location")
            elif gymName[2] is None:
                print("You have been promoted to gym leader")
                update_gymleader(trnr.t_id, Goto) # if no gym leader, update to gym leader
            elif gymName[2] == trnr.t_id:
                print("You can't fight yourself!")
            else:
                gbat_id = start_battle(trnr.t_id, gymName[2])
                db.execute("SELECT outcome FROM Battle WHERE trainer_id = ? AND b_id = ?",(trnr.t_id, gbat_id))
                bat_result = db.fetchone()
                print(bat_result)
                if bat_result[0] == "w":
                    try:
                        with con:
                            print("You have been promoted to gym leader and earned 5000 coins")
                            update_gymleader(trnr.t_id, Goto) # if no gym leader, update to gym leader
                            battle_prize(trnr.t_id, gbat_id)
                    except Exception as e:
                        raise e
                else:
                    print("You have lost to the gym leader")

        elif op == 4:
            goBack = True
#canlearn: s_id,p_id
#skill: s_id, sname, type, damage
#capturelearnedski: s_id, c_id

def wild_to_captured(wildID,trainerID):     #Move wild to captured & delete wild


    db.execute("SELECT p_id FROM Wild WHERE w_id=?",(wildID,))
    pokemonID = db.fetchone()
    db.execute("SELECT MAX(c_id) FROM Trainer AS t JOIN Captured AS c ON t.t_id=? AND c.t_id=?",(trainerID,trainerID,))
    maxCapturedID = db.fetchone()
    with con:
        db.execute("""INSERT INTO Captured VALUES
                   (:p_id,:c_id,:level,:t_id)"""
                   , {'p_id': pokemonID[0],    'c_id': int(maxCapturedID[0])+1,
                      'level': 1,  't_id': trainerID})

        db.execute("SELECT s_id FROM Can_Learn WHERE p_id=?",(pokemonID[0],))
        skillID = db.fetchall()
        skillIntList = [i[0] for i in skillID]
        randSkill = randint(0,len(skillIntList)-1)
        randSkill2 = 0
        if randSkill == 0:
            randSkill2 = randSkill+1
        elif randSkill == len(skillIntList)-1:
            randSkill2 = randSkill-1
        else:
            randSkill2 = randSkill+1

        db.execute("""INSERT INTO Captured_Learned_Skill VALUES
                    (:s_id, :c_id)"""
                    ,{'s_id':skillIntList[randSkill],'c_id':int(maxCapturedID[0])+1})
        db.execute("""INSERT INTO Captured_Learned_Skill VALUES
                    (:s_id, :c_id)"""
                    ,{'s_id':skillIntList[randSkill2],'c_id':int(maxCapturedID[0])+1})
        #delete wild
        db.execute("DELETE FROM Wild WHERE w_id=?",(wildID,))

def pickUpItem(itemID,trainerID, Goto):
    try:
        db.execute("begin")
        db.execute("UPDATE Own_Item SET num = num + 1 WHERE t_id=? AND i_id=?",(trainerID,itemID))
        db.execute("DELETE FROM Refresh_Item WHERE i_id=? AND l_id=?",(itemID, Goto))
        db.execute("commit")
    except sqlite3.IntegrityError as e:
        db.execute("rollback")
        raise e

def decrementItemCount(itemID,trainerID):
    with con:
        db.execute("UPDATE Own_Item SET num=num-1 WHERE i_id=? AND t_id=?",(itemID,trainerID))

def tutorial(trnr):  # capture fist pokemon
    print("Choose your first Pokemon:")
    print("\t1. Bulbasaur\n\t2. Charmander\n\t3. Squirtle ")
    op = int(input("Enter option: "))
    if op == 1:
        p_id = 1
    elif op == 2:
        p_id = 4
    elif op == 3:
        p_id = 7
    else:
        print('Invalid Option!')
        exit(-1)
    try:
        with con:
            add_captured(p_id, 100*trnr.t_id, trnr.t_id)
            trnr.primary_cap = 100*trnr.t_id
            #Khoa's Ghetto Fix
            db.execute("SELECT p_id FROM Captured WHERE c_id=?",(trnr.primary_cap,))
            pokemonID = db.fetchone()
            db.execute("SELECT s_id FROM Can_Learn WHERE p_id=?",(pokemonID[0],))
            skillID = db.fetchall()
            skillIntList = [i[0] for i in skillID]
            randSkill = randint(0,len(skillIntList)-1)
            randSkill2 = 0
            if randSkill == 0:
                randSkill2 = randSkill+1
            elif randSkill == len(skillIntList)-1:
                randSkill2 = randSkill-1
            else:
                randSkill2 = randSkill+1
            db.execute("""INSERT INTO Captured_Learned_Skill VALUES
                        (:s_id, :c_id)"""
                        ,{'s_id':skillIntList[randSkill],'c_id':100*trnr.t_id})
            db.execute("""INSERT INTO Captured_Learned_Skill VALUES
                        (:s_id, :c_id)"""
                        ,{'s_id':skillIntList[randSkill2],'c_id':100*trnr.t_id})
            #Khoa's Ghetto Fix Ends Here
    except sqlite3.IntegrityError as e:
        con.rollback()
        raise e

def extractTuple_to_List(tuple):
    t_id, username, level, coin, vl_id, hl_id, primary_cap = tuple
    aNewList = [t_id, username, level, coin, vl_id, hl_id, primary_cap]
    return aNewList

def signIn():
    TrainerAuthenticated = False
    while TrainerAuthenticated is False:
        #userid = int(input('ID: '))
        username = str(input('Username: '))
        if username == 'Admin':
            adminMenu()
            menu()
        else:
            # authenticate trainer
            db.execute('SELECT * FROM Trainer WHERE username=?',
                       (username,))
            tempList = db.fetchall()    # temp list to hold result
            if not tempList:            # if list is empty then query yielded no results
                print('Invalid Username')
            else:                       # account exists
                # tb.fetchall() returns a list
                # In this case it returns a list with 1 tuple
                # For example, [(1,'Brian',6,7566,66,66,101)]
                # We need to extract this tuple to
                # initialize tempTrainer object to pass around
                newlist = extractTuple_to_List(tempList[0])
                tempTrainer = Trainer(newlist[0], newlist[1], newlist[2],
                                      newlist[3], newlist[4], newlist[5],
                                      newlist[6])
                TrainerAuthenticated = True
            signedInSuccessfully(tempTrainer)

def checkBag(trainer_object):
    db.execute('SELECT Coin FROM Trainer WHERE t_id = ?',(trainer_object.t_id,))
    coin = db.fetchone()
    db.execute("""SELECT DISTINCT iname, num FROM Item i INNER JOIN Own_Item o ON i.i_id=o.i_id WHERE t_id=?
            """,(trainer_object.t_id,))
    itemList = db.fetchall()
    print("Coin: ",coin[0])
    print("Item: ")
    for x in itemList:
        print('\t',x)

#refresh_item: l_id, i_id
#own_item: i_id,t_id, num
#item: i_id, iname, price, funct

def checkPokemon(trainer_id):
	db.execute('SELECT p.pname FROM Pokemon p INNER JOIN Captured c ON p.p_id = c.p_id WHERE c.t_id = ?', (trainer_id,))
	print(db.fetchall())

def signedInSuccessfully(trnr):
    # After sign up or sign in, the user will be directed here
    logOut = False
    while logOut is False:
        print('..............................................')
        print('..................Player Menu.................')
        print("""
    1. Check Backpack (Items, Coin, etc)
    2. Check Pokemons
    3. Pick primary Pokemon
    4. Visit (location)
    5. Log Out

            """)
        op = int(input('Enter Option: '))
        if op == 1:
            checkBag(trnr)
        elif op == 2:
            checkPokemon(trnr.t_id)
        elif op == 3:
            set_primary_pokemon(trnr)
        elif op == 4:
            visitLocation(trnr)
        elif op == 5:
            logOut = True


def menu():
    print('\t    Hello Pokemon Universe!')
    print('..............................................')
    print('..................Main Menu...................')
    print("""
            1. Sign Up
            2. Sign In
            3. Exit
        """)
    op = int(input('Enter Option: '))
    if op == 1:
        signUp()
    elif op == 2:
        signIn()
    elif op == 3:
        print('..............................................')
        print('................Exiting Program...............')
        sys.exit()
    else:
        print('Invalid Option!')


def start_battle(trnr1, trnr2):
	b = Battle(trnr1, trnr2, True)
	b.battle()
	return b.battleResult()

# MAIN
menu()


con.close()
