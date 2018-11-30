import sqlite3
from trainer import Trainer
from pokemon import Pokemon, Captured
import sys

con=sqlite3.connect('pokemon_world.db')
# con = sqlite3.connect(':memory:')
db = con.cursor()

# Create tables
db.execute(""" CREATE TABLE Pokemon(
    p_id    integer not null,
    pname    text not null,
    basic_HP integer not null,
    basic_ATK integer not null,
    type    text not null,
    r_id integer,
    r_lv integer,
    primary key (p_id),
    foreign key (r_id) references Pokemon(p_id)
    );""")

db.execute("""
    CREATE TABLE Location(
    l_id integer not null,
    lname text,
    lon not null ,          -- longitude
    lat not null,           -- latitude
    primary key (l_id)
    );""")

db.execute("""CREATE TABLE Wild(
    p_id integer not null,
    w_id integer not null,
    level integer default 1,
    l_id integer not null,
    primary key (w_id),
    foreign key (p_id) references Pokemon(p_id)
    foreign key (l_id) references Location(l_id)
    );""")

db.execute("""
    CREATE TABLE Captured(
    p_id integer not null,
    c_id integer not null,
    level integer default 1,
    t_id integer not null,
    primary key (c_id),
    foreign key (p_id) references Pokemon(p_id)
    foreign key (t_id) references Trainer(t_id)
    );""")

db.execute("""
    CREATE TABLE Skill(
    s_id integer not null,
    sname    text not null,
    type    text not null,
    damage integer,
    primary key (s_id)
    );""")

db.execute("""
    CREATE TABLE Can_Learn(
    s_id integer not null,
    p_id integer not null,
    foreign key (p_id) references Pokemon(p_id),
    foreign key (s_id) references Skill(s_id),
    primary key (s_id,p_id)
    );""")

db.execute("""
    CREATE TABLE Captured_Learned_Skill(
    s_id integer not null,
    c_id integer not null,
    foreign key (s_id) references Skill(s_id),
    foreign key (c_id) references Captured(c_id),
    primary key (s_id,c_id)
    );""")


db.execute("""
    CREATE TABLE Trainer(
    t_id integer not null,
    username text,
    level integer default 1,
    coin integer default 0,
    vl_id integer,
    hl_id integer,
    primary_cap integer not null,
    primary key (t_id),
    foreign key (primary_cap) references Captured(c_id),
    foreign key (vl_id) references Location(l_id),
    foreign key (hl_id) references Location(l_id)
    );""")

db.execute("""
    CREATE TABLE Item(
    i_id integer not null,
    iname text,
    price integer,
    funct text,
    primary key (i_id)
    );""")

db.execute("""
    CREATE TABLE Own_Item(
    i_id integer not null,
    t_id integer not null,
    num integer default 1,
    primary key (i_id,t_id),
    foreign key (i_id) references Item(i_id),
    foreign key (t_id) references Trainer(t_id)
    );""")

db.execute("""
    CREATE TABLE Gym(
    g_id integer not null,
    Gname text,
    l_id integer not null,
    leader_id integer default null,
    primary key (g_id),
    foreign key (leader_id) references Trainer(t_id),
    foreign key (l_id) references Location(l_id)
    );""")

db.execute("""
    CREATE TABLE Refresh_Item(
    l_id integer not null,
    i_id integer not null,
    foreign key (i_id) references Item(i_id),
    foreign key (l_id) references Location(l_id),
    primary key (l_id,i_id)
    );""")

db.execute("""
    CREATE TABLE Battle(
    trainer_id integer not null,
    b_id integer not null,
    outcome text,
    foreign key (trainer_id) references Trainer(t_id),
    primary key (trainer_id,b_id)
    );""")

db.execute("""
    CREATE TABLE Battle_Prize(
    trainer_id integer not null,
    b_id integer not null,
    prize_type text not null,
    num integer default 1,
    foreign key (trainer_id,b_id) references Battle(trainer_id,b_id),
    primary key (trainer_id,b_id,prize_type)
    );""")

db.execute("""
    INSERT INTO Pokemon VALUES
    ('15','Mew','64','210','Psychic',NULL,NULL),
    ('14','Mewtwo','82','300','Psychic',NULL,NULL),
    ('13','Persian','34','158','Normal',NULL,NULL),
    ('12','Meowth','14','99','Normal','13','20'),
    ('11','Raichu','44','201','Electric',NULL,NULL),
    ('10','Pikachu','18','112','Electric','11','30'),
    ('9','Blastoise','48','171','Water',NULL,NULL),
    ('8','Wartortle','28','126','Water','9','45'),
    ('7','Squirtle','18','94','Water','8','25'),
    ('6','Charizard','56','223','Fire',NULL,NULL),
    ('5','Charmeleon','32','158','Fire','6','45'),
    ('4','Charmander','18','116','Fire','5','25'),
    ('3','Venusaur','54','198','Grass',NULL,NULL),
    ('2','Ivysaur','32','151','Grass','3','45'),
    ('1','Bulbasaur','22','118','Grass','2','25');""")

db.execute("""
    INSERT INTO Location VALUES
    ('1', 'San Jose','1','1'),
    ('2', 'San Francisco','1','2'),
    ('3', 'Milpitas','1','3'),
    ('4', 'Los Angeles','1','4'),
    ('5', 'Seattle','1','5'),
    ('6', 'New York','1','6'),
    ('7', 'Oakland','1','7'),
    ('8', 'Santa Clara','1','8'),
    ('9', 'Fremont','1','9'),
    ('10', 'Palo Alto','1','10'),
    ('11', null,'2','1'),
    ('12', null,'2','2'),
    ('13', null,'2','3'),
    ('14', null,'2','4'),
    ('15', null,'2','5'),
    ('16', null,'2','6'),
    ('17', null,'2','7'),
    ('18', null,'2','8'),
    ('19', null,'2','9'),
    ('20', null,'2','10'),
    ('21', null,'3','1'),
    ('22', null,'3','2'),
    ('23', null,'3','3'),
    ('24', null,'3','4'),
    ('25', null,'3','5'),
    ('26', null,'3','6'),
    ('27', null,'3','7'),
    ('28', null,'3','8'),
    ('29', null,'3','9'),
    ('30', null,'3','10'),
    ('31', null,'4','1'),
    ('32', null,'4','2'),
    ('33', null,'4','3'),
    ('34', null,'4','4'),
    ('35', null,'4','5'),
    ('36', null,'4','6'),
    ('37', null,'4','7'),
    ('38', null,'4','8'),
    ('39', null,'4','9'),
    ('40', null,'4','10'),
    ('41', null,'5','1'),
    ('42', null,'5','2'),
    ('43', null,'5','3'),
    ('44', null,'5','4'),
    ('45', null,'5','5'),
    ('46', null,'5','6'),
    ('47', null,'5','7'),
    ('48', null,'5','8'),
    ('49', null,'5','9'),
    ('50', null,'5','10'),
    ('51', null,'6','1'),
    ('52', null,'6','2'),
    ('53', null,'6','3'),
    ('54', null,'6','4'),
    ('55', null,'6','5'),
    ('56', null,'6','6'),
    ('57', null,'6','7'),
    ('58', null,'6','8'),
    ('59', null,'6','9'),
    ('60', null,'6','10'),
    ('61', null,'7','1'),
    ('62', null,'7','2'),
    ('63', null,'7','3'),
    ('64', null,'7','4'),
    ('65', null,'7','5'),
    ('66', null,'7','6'),
    ('67', null,'7','7'),
    ('68', null,'7','8'),
    ('69', null,'7','9'),
    ('70', null,'7','10'),
    ('71', null,'8','1'),
    ('72', null,'8','2'),
    ('73', null,'8','3'),
    ('74', null,'8','4'),
    ('75', null,'8','5'),
    ('76', null,'8','6'),
    ('77', null,'8','7'),
    ('78', null,'8','8'),
    ('79', null,'8','9'),
    ('80', null,'8','10'),
    ('81', null,'9','1'),
    ('82', null,'9','2'),
    ('83', null,'9','3'),
    ('84', null,'9','4'),
    ('85', null,'9','5'),
    ('86', null,'9','6'),
    ('87', null,'9','7'),
    ('88', null,'9','8'),
    ('89', null,'9','9'),
    ('90', null,'9','10'),
    ('91', null,'10','1'),
    ('92', null,'10','2'),
    ('93', null,'10','3'),
    ('94', null,'10','4'),
    ('95', null,'10','5'),
    ('96', null,'10','6'),
    ('97', null,'10','7'),
    ('98', null,'10','8'),
    ('99', null,'10','9'),
    ('100', null,'10','10');""")

db.execute("""

INSERT INTO Trainer VALUES
(0, 'Admin', 0, 0, 0, 0, 0),
('1','Brian','6','7566','66','66','102'),
('2','Cristian','19','25419','19','19','201'),
('3','Khoa','2','6282','82','82','301'),
('4','Shiyan','2','13022','22','22','401');""")

db.execute("""

    INSERT INTO Wild VALUES
    ('6','1','6','1'),
    ('9','2','39','2'),
    ('12','3','27','3'),
    ('2','4','17','4'),
    ('13','5','43','5'),
    ('15','6','15','6'),
    ('13','7','13','7'),
    ('12','8','42','8'),
    ('15','9','34','9'),
    ('4','10','24','10'),
    ('9','11','40','9'),
    ('10','12','5','8'),
    ('5','13','33','7'),
    ('13','14','41','6'),
    ('3','15','45','5');""")

db.execute("""

    INSERT INTO Captured VALUES
    ('6','101','6','1'),
    ('9','102','15','1'),
    ('12','103','42','1'),
    ('2','201','50','2'),
    ('13','202','58','2'),
    ('15','203','15','2'),
    ('4','301','28','3'),
    ('10','302','42','3'),
    ('5','303','60','3'),
    ('3','401','49','4'),
    ('11','402','54','4'),
    ('14','403','40','4');""")

db.execute("""
    INSERT INTO Item VALUES
    ('1','20Hp','20','recover 20 Hp'),
    ('2','50Hp','50','recover 50 Hp'),
    ('3','100Hp','200','recover 100 Hp'),
    ('4','Poke Ball','100','Catch Pokemon'),
    ('5','Master Ball','100000','Catch Pokemon without failure');""")

db.execute("""
    INSERT INTO Own_Item VALUES
    ('1','1','5'),
    ('2','1','5'),
    ('3','1','5'),
    ('4','1','5'),
    ('5','1','1'),
    ('1','2','5'),
    ('2','2','5'),
    ('3','2','5'),
    ('4','2','5'),
    ('5','2','1'),
    ('1','3','5'),
    ('2','3','5'),
    ('3','3','5'),
    ('4','3','5'),
    ('5','3','1'),
    ('1','4','5'),
    ('2','4','5'),
    ('3','4','5'),
    ('4','4','5'),
    ('5','4','1');""")

db.execute("""
    INSERT INTO Gym VALUES
    ('1','The Downtown Gym','1','1'),
    ('2', 'SF Gym', '2', null),
    ('3', 'The LAG', '4', '3'),
    ('4', 'NYC Gym', '6', null)
    ;""")  # lcation_id: = location, gyms are predefined.

db.execute("""
    INSERT INTO Refresh_Item VALUES
    ('1','2'),
    ('2','3'),
    ('3','2'),
    ('4','2'),
    ('5','2'),
    ('6','3'),
    ('7','4'),
    ('8','2'),
    ('9','4'),
    ('10','1'),
    ('10','2'),
    ('11','4'),
    ('12','1'),
    ('13','3'),
    ('14','3');""")

db.execute("""
    INSERT INTO Battle VALUES
    ('1','1','w'),
    ('2','1','l'),
    ('2','2','w'),
    ('3','2','l'),
    ('3','3','w'),
    ('4','3','l'),
    ('4','4','w'),
    ('2','4','l');""")

db.execute("""
    INSERT INTO Battle_Prize VALUES
    ('1','1','Coin','500'),
    ('2','2','Coin','500'),
    ('3','3','Coin','500'),
    ('4','4','Coin','500');""")

db.execute("""
    INSERT INTO Skill VALUES
    ('1','Tackle','Normal','5'),
    ('2','Vine Whip','Grass','8'),
    ('3','Power Whip','Grass','108'),
    ('4','Razor Leaf','Grass','55'),
    ('5','Solar Beam','Grass','216'),
    ('6','Petal Blizzard','Grass','132'),
    ('7','Scratch','Normal','6'),
    ('8','Ember','Fire','12'),
    ('9','Flame Burst','Fire','84'),
    ('10','Fire Fang','Fire','13'),
    ('11','Flamethrower','Fire','84'),
    ('12','Fire Spin','Fire','16'),
    ('13','Overheat','Fire','192'),
    ('14','Bubble','Water','14'),
    ('15','Water Pulse','Water','84'),
    ('16','Water Gun','Water','6'),
    ('17','Hydro Pump','Water','156'),
    ('18','Ice Beam','Ice','90'),
    ('19','Quick Attack','Normal','8'),
    ('20','Thunder Shock','Electric','6'),
    ('21','Thunderbolt','Electric','96'),
    ('22','Volt Switch','Electric','24'),
    ('23','Dark Pulse','Dark','80'),
    ('24','Feint Attack','Dark','10'),
    ('25','Confusion','Psychic','24'),
    ('26','Psychic','Psychic','120'),
    ('27','Focus Blast','Fighting','140');""")

db.execute("""
    INSERT INTO Can_Learn VALUES
    ('1','1'),
    ('2','1'),
    ('3','1'),
    ('1','2'),
    ('2','2'),
    ('3','2'),
    ('4','2'),
    ('5','2'),
    ('1','3'),
    ('2','3'),
    ('3','3'),
    ('4','3'),
    ('5','3'),
    ('6','3'),
    ('7','4'),
    ('8','4'),
    ('9','4'),
    ('11','4'),
    ('7','5'),
    ('8','5'),
    ('9','5'),
    ('10','5'),
    ('11','5'),
    ('7','6'),
    ('8','6'),
    ('9','6'),
    ('10','6'),
    ('11','6'),
    ('12','6'),
    ('13','6'),
    ('1','7'),
    ('14','7'),
    ('15','7'),
    ('1','8'),
    ('14','8'),
    ('15','8'),
    ('16','8'),
    ('1','9'),
    ('14','9'),
    ('15','9'),
    ('16','9'),
    ('17','9'),
    ('19','10'),
    ('20','10'),
    ('21','10'),
    ('19','11'),
    ('20','11'),
    ('21','11'),
    ('22','11'),
    ('7','12'),
    ('23','12'),
    ('7','13'),
    ('23','13'),
    ('24','13'),
    ('25','14'),
    ('26','14'),
    ('27','14'),
    ('12','15'),
    ('13','15'),
    ('17','15'),
    ('22','15'),
    ('26','15'),
    ('27','15');""")

db.execute("""
    INSERT INTO Captured_Learned_Skill VALUES
    ('12','101'),
    ('8','101'),
    ('1','102'),
    ('16','102'),
    ('23','103'),
    ('7','103'),
    ('1','201'),
    ('3','201'),
    ('24','202'),
    ('23','202'),
    ('27','203'),
    ('17','203'),
    ('8','301'),
    ('9','301'),
    ('21','302'),
    ('20','302'),
    ('7','303'),
    ('10','303'),
    ('6','401'),
    ('3','401'),
    ('20','402'),
    ('21','402'),
    ('27','403'),
    ('26','403');""")
con.commit()
con.close()
