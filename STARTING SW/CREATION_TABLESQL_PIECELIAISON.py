import pandas as pd
import sqlite3

filepath = "./PIECES_LIAISON.db"
open(filepath, 'w').close() #crée un fichier vide
DataBase = sqlite3.connect(filepath)

QueryCurs = DataBase.cursor()
# On définit une fonction de création de table

def CreateTable(nom_bdd):
    QueryCurs.execute('''CREATE TABLE IF NOT EXISTS ''' + nom_bdd + '''
    (id INTEGER PRIMARY KEY, TYPELIAISON TEXT,MATERIAU TEXT, DNMIN INTEGER,DNMAX INTEGER, PIECENAME TEXT)''')

# On définit une fonction qui permet d'ajouter des observations dans la table

def AddEntry(nom_bdd, TYPEL,MAT,DNMIN,DNMAX,nomPiece):
    QueryCurs.execute('''INSERT INTO ''' + nom_bdd + '''
    (TYPELIAISON,MATERIAU,DNMIN,DNMAX,PIECENAME) VALUES (?,?,?,?,?)''',(TYPEL,MAT,DNMIN,DNMAX,nomPiece))

def AddEntries(nom_bdd, data):
    """ data : list with (Name,City,Country,Price) tuples to insert
    """
    QueryCurs.executemany('''INSERT INTO ''' + nom_bdd + '''
    (TYPELIAISON, MATERIAU ,DNMIN,DNMAX ,PIECENAME ) VALUES (?,?,?,?,?)''',data)

### On va créer la table clients
CreateTable("PIECES_DE_LIAISON")

########## LIAISON BU-BU ##########
ULTRALINK = [("BU-BU","FONTE FGS",51,348,"ULTRA LINK"),
            ("BU-BU","FONTE FGL",51,348,"ULTRA LINK"),
            ("BU-BU","PVC PRESSION",51,348,"ULTRA LINK"),
            ("BU-BU","ACIER",51,348,"ULTRA LINK"),
            ("BU-BU","FIBRES CIMENT",51,348,"ULTRA LINK"),]

LINKGS =    [("BU-BU","FONTE FGS",40,600,"LINK GS"),
            ("BU-BU","FONTE FGL",40,600,"LINK GS"),]
LINKGSGRANDDN =    [("BU-BU","FONTE FGS",700,2000,"LINK GS GRAND DN"),
            ("BU-BU","FONTE FGL",700,2000,"LINK GS GRAND DN"),]
MANCHONEXPRESS =    [("BU-BU","FONTE FGS",60,1200,"MANCHON EXPRESS"),
            ("BU-BU","FONTE FGL",60,1200,"MANCHON EXPRESS"),]

AddEntries("PIECES_DE_LIAISON",ULTRALINK)
AddEntries("PIECES_DE_LIAISON",LINKGS)
AddEntries("PIECES_DE_LIAISON",LINKGSGRANDDN)
AddEntries("PIECES_DE_LIAISON",MANCHONEXPRESS)
########## LIAISON BU-BRIDE ##########
ULTRAQUICK = [("BU-BRIDE","FONTE FGS",51,348,"ULTRA QUICK"),
            ("BU-BRIDE","FONTE FGL",51,348,"ULTRA QUICK"),
            ("BU-BRIDE","PVC PRESSION",51,348,"ULTRA QUICK"),
            ("BU-BRIDE","ACIER",51,348,"ULTRA QUICK"),
            ("BU-BRIDE","FIBRES CIMENT",51,348,"ULTRA QUICK"),]
QUICKFONTE =    [("BU-BRIDE","FONTE FGS",60,300,"QUICK FONTE"),
            ("BU-BRIDE","FONTE FGL",60,300,"QUICK FONTE"),]
ADAPTBRIDE =    [("BU-BRIDE","FONTE FGS",350,2000,"ADAPTEUR DE BRIDES"),
            ("BU-BRIDE","FONTE FGL",350,2000,"ADAPTEUR DE BRIDES"),]
BEEXPRESS =    [("BU-BRIDE","FONTE FGS",60,1200,"BRIDE EMBOITEMENT EXPRESS"),
            ("BU-BRIDE","FONTE FGL",60,1200,"BRIDE EMBOITEMENT EXPRESS"),]
QUICKPVC =    [("BU-BRIDE","PVC PRESSION",40,225,"QUICK PVC")]
BEKILSKO =    [("BU-BRIDE","PVC PRESSION",63,225,"QUICK PVC"),
               ("BU-BRIDE","PE",63,225,"QUICK PVC")]

AddEntries("PIECES_DE_LIAISON",ULTRAQUICK)
AddEntries("PIECES_DE_LIAISON",QUICKFONTE)
AddEntries("PIECES_DE_LIAISON",ADAPTBRIDE)
AddEntries("PIECES_DE_LIAISON",BEEXPRESS)
AddEntries("PIECES_DE_LIAISON",QUICKPVC)
AddEntries("PIECES_DE_LIAISON",BEKILSKO)
########## LIAISON BU-EMBOITURE ##########
BRIDEUNI=[("BU-EMBOITURE","FONTE FGS",60,2000,"BRIDE UNI"),
          ("BU-EMBOITURE","FONTE FGL",60,2000,"BRIDE UNI")]
AddEntries("PIECES_DE_LIAISON",BRIDEUNI)

# on va "commit" c'est à dire qu'on va valider la transaction.
# > on va envoyer ses modifications locales vers le référentiel central - la base de données SQL
DataBase.commit()


df1 = pd.read_sql_query('SELECT * FROM PIECES_DE_LIAISON', DataBase)
print("En utilisant la méthode read_sql_query \n", df1, "\n")

