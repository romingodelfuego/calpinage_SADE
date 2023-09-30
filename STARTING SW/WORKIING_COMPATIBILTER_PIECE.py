from json import *
"""DANS LA METHODE DE RECHERCHE ON CONSIDERES LA PIECE 1 ET LA PIECE 2. """
PIECE1 = {  "TYPE":"RESEAUX",##CHOIX ENRTRE BRANCHEMENT, RESEAUX,RACCORDEMENT
            "MATERIAU": "FONTE",##CHOIX ENTRE Plastiqe, Fonte
            "LONGUEUR": 1, ##METRES
            "CONNEXIONS":{
                            "CONN1":{   "TYPEC":("BRIDE",False),##(Kit express,Standard.., Verouillé ou Non Vérrouillé)
                                        "DN":50, ##CM
                                        "PN":16,
                                        "JEU":0, ##DEGRES, Sur le Connexion
                                        "ANGLE": "REF",#Angle entre la connexion précédente int ou str(REF)
                                    },
                            "CONN2":{   "TYPEC":("STD",False),##(Kit express,Standard.., Verouillé ou Non Vérrouillé)
                                        "DN":50, ##CM   
                                        "JEU":0, ##DEGRES, Sur le Connexion
                                        "ANGLE" : "REF",#Angle entre la connexion précédente int ou str(REF)
                                    },
                            "CONN3":{   "TYPEC":("EXPR",True),##(Kit express,Standard.., Verouillé ou Non Vérrouillé)
                                        "DN": 80, ##CM   
                                        "JEU":0, ##DEGRES, Sur le Connexion
                                        "ANGLE": "REF",#Angle entre la connexion précédente int ou str(REF)
                                    },
                        }
          }

PIECE2 = {  "TYPE":"RESEAUX",##CHOIX ENRTRE BRANCHEMENT, RESEAUX,RACCORDEMENT
            "MATERIAU": "FONTE",##CHOIX ENTRE Plastiqe, Fonte
            "LONGUEUR": 6, ##METRES
            "CONNEXIONS":{  "CONN1":{   "TYPEC":("STD",False),##(Kit express,Standard.., Verouillé ou Non Vérrouillé)
                                        "DN":50, ##CM   
                                        "JEU":0, ##DEGRES, Sur le Connexion
                                        "ANGLE" : "REF",#Angle entre la connexion précédente int ou str(REF)
                                    },
                            "CONN2":{   "TYPEC":("EXPR",True),##(Kit express,Standard.., Verouillé ou Non Vérrouillé)
                                        "DN":80, ##CM   
                                        "JEU":0, ##DEGRES, Sur le Connexion
                                        "ANGLE" : "REF",#Angle entre la connexion précédente int ou str(REF)
                            }
       
                    }
          }

"""DETERMINER QUELLE CONNEXION EST COMPATIBLE"""
paramValidant = ["MATERIAU", "DN", "TYPEC"]

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
    for _ in range( max - len(valueParam)):
        valueParam.append(value)
    return valueParam

def search_values_flatten(dictionary, param_target_key):
    valueParam,valueParam_check,max=[],[],0
    for target_key in param_target_key:
        #checkList=check_length(flatten_list(search_value(dictionary,target_key)))
        #valueParam.append(checkList)
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
    ##POSSIBLE OPTIMISATION EN NE REGARDANT QUE LES REUSLATST DE LA PIECE 2 SI ELLES SONT COMPATIBLE ALORS FORCEMENT LA PIECE 2 L'EST 
    valueParam1,valueParam2=search_values_flatten(Piece1,paramList),search_values_flatten(Piece2,paramList)
    print("Value paramètres 1",valueParam1)
    print("Value paramètres 2",valueParam2)

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
    print(counts)
    for conn in range(len(listConnCat)):
        for val in listConnCat[conn]:
            if isinstance(val,list):
                for i in range(len(val)):
                    counts[conn][val[i]]+=1
            else: 
                if val!=None:
                    counts[conn][val]+=1
    return counts

def isCompatible(Piece1,Piece2,paramList): ##On le fais pour les deux mais réellement aps utile
    iComp1= compatibiliter(Piece1,Piece2,paramList)
    iComp2= compatibiliter(Piece2,Piece1,paramList) 
    print("icomp1\t",iComp1)
    print("icomp2\t",iComp2)
    listConnCat1=trieIndicConn(iComp1)
    print("listConnCatt1 CHECK\n",listConnCat1)

    listConnCat2=trieIndicConn(iComp2)
    print("listConnCatt2 CHECK\n",listConnCat2)

    counts1=countInList(listConnCat1,len(listConnCat2))
    print("counts1 CHECK\n",counts1)
    counts2=countInList(listConnCat2,len(listConnCat1))
    print("counts2 CHECK\n",counts2)
    for i in range(len(counts1)):
        for keys,value in counts1[i].items():
            if value == len(paramList):
                #print(iComp1)
                print(f"PIECE 1: CONNEXION {i+1} et PIECE 2: CONNEXION {keys+1}")
    
    for i in range(len(counts2)):
        for keys,value in counts2[i].items():
            if value == len(paramList):
                #print(iComp2)
                print(f"PIECE 2: CONNEXION {i+1} et PIECE 1: CONNEXION {keys+1}")
 



#print(iComp1,iComp2)
#print(paramValidant[1:])
#print(listConnCat)
#print(countInList(listConnCat))

isCompatible(PIECE1,PIECE2,paramValidant)

