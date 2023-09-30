from json import *
import pandas as pd
import sqlite3
###########################################################################################################################################
"""CONNEXION DE LA BASE DE DONNE SQL AVEC LE PROGRAMME PYTHON"""
###########################################################################################################################################
filepath = "./PIECES_LIAISON.db"
open(filepath, 'r').close() #crée un fichier vide
DataBase = sqlite3.connect(filepath)
QueryCurs = DataBase.cursor()

df1 = pd.read_sql_query('SELECT * FROM PIECES_DE_LIAISON', DataBase)
print(df1, "\n")
###########################################################################################################################################
"""CREATION DES INSTANCIATIONS DU PROGRAMMES. """
###########################################################################################################################################

class PIECE :
    def __init__(self,REF,NAME,TYPE,MATERIAU,LONGUEUR,listConn):
        self.root = {}
        self.root["ADDR"]=self
        self.root["REF"]=REF
        self.root["NAME"]=NAME
        self.root["TYPE"]=TYPE
        self.root["MATERIAU"]=MATERIAU
        self.root["LONGUEUR"]=LONGUEUR
        self.root["TYPE"]=TYPE
        self.root["CONNEXIONS"]={}
        for i in range(len(listConn)):
            self.root["CONNEXIONS"]["CONN"+str(i+1)]={}
            self.root["CONNEXIONS"]["CONN"+str(i+1)]["CATC"]=listConn[i][1] ##Emboiture(=BU?),Bride,BU
            self.root["CONNEXIONS"]["CONN"+str(i+1)]["TYPEC"]=listConn[i][0] ##MALE, FEMELLE
            self.root["CONNEXIONS"]["CONN"+str(i+1)]["DN"]=listConn[i][2]
            self.root["CONNEXIONS"]["CONN"+str(i+1)]["PN"]=listConn[i][3]
            self.root["CONNEXIONS"]["CONN"+str(i+1)]["LINK"]={}
            self.root["CONNEXIONS"]["CONN"+str(i+1)]["LINK"]["PIECE_LINK"] = None
            self.root["CONNEXIONS"]["CONN"+str(i+1)]["LINK"]["CONNEXION_LINK"] = None

ThePIECE1 = PIECE(1,"TÉ","RESEAUX","FONTE FGS",1,[["F",("BRIDE",False),50,16],['M',("BU",False),80,16],['F',("EXPR",False),80,10]])
ThePIECE2 = PIECE(2,"TUBE","RESEAUX","FONTE FGS",6,[["F",("BU",False),80,16],["M",("EXPR",True),80,16]])
ThePIECE3 = PIECE(3,"TUBE","RESEAUX","FONTE",6,[["F",("BRIDE",False),50,16],['M',("EXPR",False),80,16]])
ThePIECE4 = PIECE(4,"VANNE","RESEAUX","FONTE",1,[["F",("EXPR",True),80,16]])
ThePIECE5 = PIECE(5,"PP","RESEAUX","FONTE",1,[["F",("EXPR",False),80,16]])
#ThePIECE1.root["ADDR"] = ThePIECE1
PIECE1 = ThePIECE1.root
PIECE2= ThePIECE2.root
PIECE3=ThePIECE3.root
PIECE4 = ThePIECE4.root
PIECE5= ThePIECE5.root
"""DETERMINER QUELLE CONNEXION EST COMPATIBLE"""
paramValidant = ["PN","DN","CATC"]


###########################################################################################################################################
"""LIAISON ENTRE PIECE DE LIAISON ET PIECE DE TUYAUTERIE. """
###########################################################################################################################################
"""def trouverPieceLiaison(dataBase,table,piece1,connPiece1,piece2,connPiece2):
    table= "PIECES_DE_LIAISON"
    typeConn1 = connPiece1["CATC"][0]
    typeConn2=connPiece2["CATC"][0]
    mat= connPiece1["LINK"]['PIECE_LINK'].root["MATERIAU"]
    dn = connPiece1["DN"]
    name = str(typeConn1)+"-"+str(typeConn2)
    data=dataBase.execute("SELECT PIECENAME FROM " + table + " WHERE MATERIAU= ? AND TYPELIAISON = ? AND DNMIN < ? AND ?<DNMAX  ", (mat,name,dn,dn)).fetchall()
    if len(data)>1:
        choices={i: data[i][0] for i in range(len(data))}
        iSol=input(f"Il faut choisir une pièce de liaison:\n\n {choices}")
        name=data[int(iSol)][0]
        pieceLiaison= PIECE(6,name,"MONTAGE","FONTE",0,[])NAME,TYPE,MATERIAU,LONGUEUR,listConn
    associated(connPiece1,connPiece2,pieceLiaison)
    return(data)
def associated(connPiece1,connPiece2,pieceLiaison):
    connPiece1["LINK"]["PIECE_LINK"] = pieceLiaison["ADR"]
    connPiece1["LINK"]["CONNEXION_LINK"] = "PIECELIAISON"
    connPiece2["LINK"]["PIECE_LINK"] = pieceLiaison["ADR"]
    connPiece2["LINK"]["CONNEXION_LINK"] = "PIECELIAISON"

"""
###########################################################################################################################################
"""PARTIE PRELIMINAIRE DU PROGRAMME. """
###########################################################################################################################################

def search_value(dictionary, target_key):
    results = []
    for key, value in dictionary.items():
        if isinstance(value, dict):
            result = search_value(value, target_key)
            results.append(result)
        elif key == target_key:
            results.append(value)
    return results

# Convertir les résultats en une liste plate
def flatten_list(lst):
    flattened = []
    for item in lst:
        if isinstance(item, list):
            flattened.extend(flatten_list(item))
        else:
            flattened.append(item)
    return flattened

def check_length(valueParam,max):
    ### On veut que toutes les 
    value= valueParam[0]
    for _ in range(max - len(valueParam)):
        valueParam.append(value)
    return valueParam

def search_values_flatten(dictionary, param_target_key):
    valueParam,valueParam_check,max=[],[],0
    for target_key in param_target_key:
        valueParam.append(flatten_list(search_value(dictionary,target_key)))
    
    for i in range(len(valueParam)):
        if len(valueParam[i])>max:
            max=len(valueParam[i])
        
    #print(f"Le max est {max}")

    for i in range(len(valueParam)):
        #print(f"Longueur de {valueParam[i]}",len(valueParam[i]))
        valueParam_check.append(check_length(valueParam[i],max))
        #print(f"Apres Check_length: {valueParam_check[i]}")

    return valueParam_check

#print( search_values_flatten(PIECE1, paramValidant),"  |   ",search_values_flatten(PIECE2, paramValidant))




def compatibiliter(Piece1,Piece2,paramList): 
    ##POSSIBLE OPTIMISATION EN NE REGARDANT QUE LES RESULTATS DE LA PIECE 2 SI ELLES SONT COMPATIBLE ALORS FORCEMENT LA PIECE 2 L'EST 
    valueParam1,valueParam2=search_values_flatten(Piece1,paramList),search_values_flatten(Piece2,paramList)
    iComp1=[]
    for i in range(len(paramList)):
        tempList1=[]
        for iparam1 in range(len(valueParam1[i])): ## On parcourt la premiere liste
            param1 = valueParam1[i][iparam1]
            findMatch,alreadyFind,tempList2= False,False,[]
            for iparam2 in range(len(valueParam2[i])): ## On parcourt la seconde
                param2 = valueParam2[i][iparam2]
                if  param1 == param2:
                    if alreadyFind:
                        firstTimeDoublon = type(tempList1[-1])==int ##La premire fois c'est toujours un int 
                        if firstTimeDoublon:
                            tempList1[-1]=[tempList1[-1]]
                        ##A ce stade on est sur que tempList1[-1] est un array
                        tempList1[-1].append(iparam2)##On stocke les indices de l'autre liste
                    else:
                        tempList1.append(iparam2)
                    findMatch,alreadyFind=True,True
            if not findMatch :
                tempList1.append(None)
        iComp1.append((tempList1))
    return iComp1

def trieIndicConn(iComp):
    listConnCat=[]
    for iconn in range(len(iComp[1])): ##Pas tres élégant
        listTemp=[]
        for icat in range(len(iComp)): ##=Nombre de paramtre a valider
            listTemp.append(iComp[icat][iconn])
        listConnCat.append(listTemp)    ##On se retrouve avec les indic de Comp de chaque cat par connexion Conn:[Mat,DN,TypeC]
    return listConnCat

def countInList(listConnCat,max):
    nconn=len(listConnCat)
    counts=[{i:0 for i in range(max)} for conn in range(nconn)] ##Pas sur de la longueur des listes
    #print(counts)
    for conn in range(len(listConnCat)):
        for val in listConnCat[conn]:
            if isinstance(val,list):
                for i in range(len(val)):
                    counts[conn][val[i]]+=1
            else: 
                if val!=None:
                    counts[conn][val]+=1
    return counts

def associated(PieceRef,PieceRapportee,paramList): ##On le fais pour les deux mais réellement aps utile
    iCompRef= compatibiliter(PieceRef,PieceRapportee,paramList)
    iCompRapportee= compatibiliter(PieceRapportee,PieceRef,paramList) 
    listConnCatRef=trieIndicConn(iCompRef)
    listConnCatRapportee=trieIndicConn(iCompRapportee)
    countsRef=countInList(listConnCatRef,len(listConnCatRapportee))

    compatible=False
    for i in range(len(countsRef)):
        for keys,value in countsRef[i].items():
            if value == len(paramList):
                compatible = True
                if PieceRef["CONNEXIONS"]["CONN"+str(i+1)]["LINK"]["PIECE_LINK"] is None:
                    print(f"PIECE {PieceRef['REF']}: CONNEXION {i+1} et PIECE {PieceRapportee['REF']}: CONNEXION {keys+1}")
                    PieceRef["CONNEXIONS"]["CONN"+str(i+1)]["LINK"]["PIECE_LINK"] = PieceRapportee["ADDR"]
                    PieceRef["CONNEXIONS"]["CONN"+str(i+1)]["LINK"]["CONNEXION_LINK"] = keys+1
                    PieceRapportee["CONNEXIONS"]["CONN"+str(keys+1)]["LINK"]["PIECE_LINK"] = PieceRef["ADDR"]
                    PieceRapportee["CONNEXIONS"]["CONN"+str(keys+1)]["LINK"]["CONNEXION_LINK"] = i+1
                else : 
                    print(f"Une pièce est déjà sur la connexion {i+1} de la piece {PieceRef['REF']}")
    if not compatible:
        print(f"Les pieces: {PieceRef['REF']},{PieceRapportee['REF']} sont incompatibles")
associated(PIECE1,PIECE2,paramValidant)
associated(PIECE1,PIECE3,paramValidant)
associated(PIECE2,PIECE4,paramValidant)
associated(PIECE3,PIECE5,paramValidant)

###########################################################################################################################################
##ON VEUT MAINTENANT EFFETCUER UN AGENCEMENT DE PIECE
#IDEE agencement(PIECE1,PIECE2,PIECE3,PIECE4) --> Sortir un tableau de listing + check si agencement possible + pouvoir retrouver le chemin
###########################################################################################################################################

def findAllPieces(PieceRef,linkAlreadyPass=None):
    listingPiece = [flatten_list(search_value(PieceRef,"NAME"))+flatten_list(search_value(PieceRef,"DN"))+flatten_list(search_value(PieceRef,"REF"))]
    listLink=flatten_list(search_value(PieceRef,"PIECE_LINK"))
    if linkAlreadyPass is None:
        linkAlreadyPass=[PieceRef["ADDR"]]

    for addr in listLink:
        if addr:
            if addr not in linkAlreadyPass :
                nextPiece= addr.root
                linkAlreadyPass.append(addr)
                nextListing=findAllPieces(nextPiece,linkAlreadyPass)
                listingPiece.extend(nextListing[0])

    return listingPiece,linkAlreadyPass

def countsListing(listing):
    counts ={}
    for elt in listing:
        key = elt[0]
        if key in counts:   counts[key]+=1
        else:   counts[key]=1
    return counts

PieceRef=PIECE4

def listing(PieceRef): ##Ce comptage d'occurence est indépendant de la pieceRef
    return countsListing(findAllPieces(PieceRef)[0])

print(listing(PieceRef))


#print(trouverPieceLiaison(DataBase,"PIECES_DE_LIAISON",PIECE1["CONNEXIONS"]["CONN2"],PIECE2["CONNEXIONS"]["CONN1"]))