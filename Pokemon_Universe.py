import sqlite3
from trainer import Trainer
from pokemon import Pokemon, Captured
import sys
from battle import Battle

con=sqlite3.connect('pokemon_world.db')
# con = sqlite3.connect(':memory:')
db = con.cursor()


def addTrainer(trnr):
    with con:
        db.execute("""INSERT INTO Trainer VALUES
                   (:t_id,:username,:level,:coin,:vl_id,:hl_id,:primary_cap)"""
                   , {'t_id': trnr.t_id,    'username': trnr.username,
                      'level': trnr.level,  'coin': trnr.coin,
                      'vl_id': trnr.vl_id,  'hl_id': trnr.hl_id,
                      'primary_cap': trnr.primary_cap})


def getAllTrainernames():
    db.execute("SELECT username,t_id FROM Trainer")
    return db.fetchall()

# def getSpecificTrainername(input):
#     db.execute("SELECT * FROM Trainer WHERE t_id = input ")
#     temp = Trainer()
#     return db.fetchall()


def getTrainerInfo(trnr):
    pass


def addPokemon(pkm):
    pass


def captured_pokemon_names(trainer):
    db.execute("""
               SELECT pname, p_id
               FROM Captured NATURAL JOIN Pokemon
               WHERE t_id = :t_id """,
               {'t_id': trainer.t_id})
    count = 1
    pokemon_list = db.fetchall()
    for row in pokemon_list:
        print("\t\t{0}. {1}".format(count, row[0]))
        count += 1
    return pokemon_list


def update_primary(trainer, p_id):
    db.execute("""
               UPDATE Trainer
               SET primary_cap = :pokemon
               WHERE t_id = :t_id """,
               {'pokemon': p_id, 't_id': trainer.t_id})
    trainer.primary_cap = p_id


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

                p_id = pokemon_list[op - 1][1]

                update_primary(trainer, p_id)

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
               FROM Trainer NATURAL JOIN Pokemon
               WHERE t_id = :t_id AND
                     p_id = primary_cap""",
               {'t_id': trainer.t_id})
    pokemon = db.fetchone()
    print("\t\t{}\n".format(pokemon[0]))


def add_captured(p_id, c_id, t_id):
    db.execute("""
                INSERT INTO Captured(p_id, c_id, t_id)
                VALUES
                (?, ?, ?)""", (p_id, c_id, t_id))


ADMIN = Trainer(9999, 'Admin', 9999, 9999, 9999, 999, 9999)
addTrainer(ADMIN)

Brian = Trainer(1, 'Brian', 6, 7566, 66, 3, 101)
# Cristian = Trainer(2,'Cristian',19,25419,19,1,201)
# Khoa = Trainer(3,'Khoa',2,6282,82,1,301)
# Shiyan = Trainer(4,'Shiyan',2,13022,22,1,401)

addTrainer(Brian)
# addTrainer(Cristian)
# addTrainer(Khoa)
# addTrainer(Shiyan)

AllTrainers = getAllTrainernames()
print("Hello Pokemon Universe")
print(AllTrainers)

'''
MAIN MENU STARTS HERE
MAIN MENU STARTS HERE
MAIN MENU STARTS HERE

'''


def adminMenu():
    loggedIn = True
    while loggedIn:
        print('...Admin Menu...')
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


def signUp():
    print('...Sign Up...')
    done = False
    while done is False:
        userid = str(input('ID: '))
        username = str(input('Username: '))
        hometown = str(input('Hometown: '))
        done = True
    # Create new trainer object
    new_trainer = Trainer(userid, username, 1, 1000, None, hometown, None)
    # Add new trainer to table
    tutorial(new_trainer)
    addTrainer(new_trainer)
    signedInSuccessfully(new_trainer)


def visitLocation(trnr):
    db.execute('SELECT l_id, lname FROM Location WHERE lname IS NOT NULL')
    locList = db.fetchall()
    for x in locList:
        print(x)
    Goto = str(input('Enter Location ID: '))
    print('Current Location: ', Goto)
    db.execute("""SELECT p.p_id,pname,level FROM Wild AS w JOIN Pokemon AS p
                ON w.p_id = p.p_id AND l_id = ?""", (Goto,))
    # db.execute('SELECT p_id,w_id,level FROM Wild WHERE l_id = ?',(Goto,))
    wildList = db.fetchall()
    for x in wildList:
        print(x)
    # List Item
    # List Gym
    goBack = False
    while goBack is False:
        print("""
            1. Capture Pokemon
            2. Pick Up Item
            3. Take Over Gym
            4. Back to Player Menu
            """)
        op = int(input('Enter Option: '))
        if op == 1:
            pass
            # capture pokemon
        elif op == 2:
            pass
            # pick up item
        elif op == 3:
            start_battle()
            # take over gym
        elif op == 4:
            goBack = True


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
            add_captured(p_id, 1, trnr.t_id)
            trnr.primary_cap = p_id
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
        userid = int(input('ID: '))
        username = str(input('Username: '))
        if userid == 9999 and username == 'ADMIN':
            adminMenu()
        else:
            # authenticate trainer
            db.execute('SELECT * FROM Trainer WHERE t_id=? AND username=?',
                       (userid, username,))
            tempList = db.fetchall()    # temp list to hold result
            if not tempList:            # if list is empty then query yielded no results
                print('Invalid ID or Username')
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


def checkBag(trainer_id, trainer_username):
    db.execute('SELECT * FROM Trainer WHERE t_id = ? AND username = ?',
               (trainer_id, trainer_username,))
    print(db.fetchall())

def checkPokemon(trainer_id):
	db.execute('SELECT p.pname FROM Pokemon p INNER JOIN Captured c ON p.p_id = c.p_id WHERE c.t_id = ?', (trainer_id,))
	print(db.fetchall())

def signedInSuccessfully(trnr):
    # After sign up or sign in, the user will be directed here
    logOut = False
    while logOut is False:
        print('...Player Menu...')
        print("""
            1. Check Backpack (Items, Coin, etc)
            2. Check Pokemons
            3. Pick primary Pokemon
            4. Visit (location)
            5. Log Out

            """)
        op = int(input('Enter Option: '))
        if op == 1:
            checkBag(trnr.t_id, trnr.username)
        elif op == 2:
            checkPokemon(trnr.t_id)
        elif op == 3:
            set_primary_pokemon(trnr)
        elif op == 4:
            visitLocation(trnr)
        elif op == 5:
            logOut = True


def menu():
    print('Hello Pokemon Universe!')
    print('.......Main Menu.......')
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
        print('...Exiting Program...')
        sys.exit()
    else:
        print('Invalid Option!')


def start_battle:


# MAIN
menu()


con.close()
