import pandas as pd

###########################################################################################################################################
"""--------------------------------------------CREATION COMPLÈTE DE L'ASSOCIATION DE PIÈCES--------------------------------------------"""
###########################################################################################################################################

###########################################################################################################################################
"""---------------------------------------------------------GESTION DES ASSETS---------------------------------------------------------"""
###########################################################################################################################################

db_Jonctions = pd.read_excel("BaseDonnée_Jonctions.xlsx",sheet_name=None)
db_Pieces = pd.read_excel("BaseDonnée_Pieces.xlsx",sheet_name=None)

def comptLiaison(liaisons):
    total, result, tarifGlobal = [], {}, 0
    
    for item in liaisons:
        total.append(item.ensemble)
        tarifGlobal+=item.tarif
    for item in total:
        for key, value in item.items():
            result.setdefault(key, 0)
            result[key] += int(value.strip())
        
    unique_list = [{key: str(value)} for key, value in result.items()]
    return [unique_list,{"Tarif Global" : tarifGlobal}]
def comptPieces(pieces):
    count_dict = {}
    
    for item in pieces:
        components = [f"{item.name} DN{item.dn} PN{item.pn}"]
        
        for intConnex in range(1, item.nbConnex + 1):
            if False in item.__dict__[f"conn{intConnex}Propag"].values():
                itemsData = item.__dict__[f"conn{intConnex}Link"]
                component = f"DN{itemsData.dn} PN{itemsData.pn}"
                components.append(component)
        
        result = " - ".join(components)
        count_dict[result] = count_dict.get(result, 0) + 1
    
    return count_dict

###########################################################################################################################################
"""---------------------------------------------CREATION DE L'OBJET PIECE.---------------------------------------------"""
###########################################################################################################################################
class PIECE :   
    def __init__(self,REF:int,NAME:str,ListTYPEC:list,ANGLE=0,propaConn1=[True,True,True],propaConn2=[True,True,True],propaConn3=[True,True,True])->None:
        ##Création des pieces : ref(autom),
        #propaConnI: propagation des attributs de la connexion I: list de Booléen concernant la propagation attributs à la pièce connectée dans l'ordre suivant: Mat,Dn,Pn
        listPropagationConn=[propaConn1,propaConn2,propaConn3]
        _listPropagationType=['mat','dn','pn']
        self.ref=REF
        self.name = NAME
        self.mat,self.dn,self.pn=None,None,None
        self.angle = ANGLE
        self.tarif =0
        self.listprop = [{_listPropagationType[param]:listPropagationConn[conn][param] for param in range(len(_listPropagationType))} for conn in range(len(listPropagationConn))]
        self.nbConnex = len(ListTYPEC)

        for i in range(self.nbConnex):
            self.__dict__["conn"+str(i+1)+"Propag"] = self.listprop[i]
            self.__dict__["conn"+str(i+1)+"Cat"] =ListTYPEC[i]
            self.__dict__["conn"+str(i+1)+"Link"] = None
        if REF == 0 : ## Si première pièce
            self.statutReference = True
            self.userQuestion("FIRST")
        else : self.statutReference = False

        pieces.append(self)

    def __isCatConnexAuthorized(self,selfConn,autrePiece,autrePieceConn,listAuthorizedCatRef):
        ##Vérifie si la connexion peut être efffectuer entre telle et telle piece
        selfCat=self.__dict__["conn"+str(selfConn)+"Cat"]
        autrePieceCat= autrePiece.__dict__["conn"+str(autrePieceConn)+"Cat"]
        try :
            if autrePieceCat in listAuthorizedCatRef[selfCat]:  return True
            else:   return False
        except KeyError: return False
        
    def associatedPieces(self,selfConn,pieceRef,pieceRefConn,listAuthorizedCatRef):
        if pieceRef.statutReference : ##On vérifie que la pièce sur laquelle on se connecte est deja connecté
            if self.__isCatConnexAuthorized(selfConn,pieceRef,pieceRefConn,listAuthorizedCatRef):
                self.__dict__["conn"+str(selfConn)+"Link"] = pieceRef
                pieceRef.__dict__["conn"+str(pieceRefConn)+"Link"] = self
                self.statutReference = True
                self.__dataPropagation(selfConn,pieceRef,pieceRefConn)
                typeLiaison=self.addLiaisonPiece(pieceRef,pieceRefConn)
            else:print("PIECES INCOMPATIBLES")
        else: print("IL FAUT UNE PIECE AU MOINS CONNECTÉE")

    def userQuestion(self,strCheckWhat,listRefToCheck=[None],key=None):
        if strCheckWhat=="FIRST" :
            ##on demande le DN le MAT et le PN
            #user=input("PREMIERE PIECE :\n\t Respectivement et en séparant par une virgule, quels sont: le matériau | le diamètre nominal (DN) | la pression nominal (PN):\t").split(',')
            user=('FONTE',60,10)
            self.mat = str(user[0])
            self.dn = int(user[1])
            self.pn=int(user[2])
            return
        if strCheckWhat =="NAME":
            if self.name in listNameToCheck: ## Cas préparé, par ex:on sait que sur la liaison manchon a besoin d'info
                self.__dict__[str(listRefToCheck[self.name][0])] = input(str(listRefToCheck[self.name][1]))
        if strCheckWhat=="PROPAGATION":
            self.__dict__[str(key)] = input(f"PIÈCE {self.name}{self.ref} EST CONNECTEE A UNE PIECE QUI NE PROPAGE PAS SON ATTRIBUT:\t{key}\nVeuillez entrer sa nouvelle valeur")
    
    def __dataPropagation(self,selfConn,pieceRef,pieceRefConn):
       for key,value in pieceRef.listprop[pieceRefConn-1].items():
            if value:
                self.__dict__[str(key)] = pieceRef.__dict__[str(key)]
            else :
                self.userQuestion("PROPAGATION",self.listprop[pieceRefConn-1],key)
    
    def addLiaisonPiece(self,pieceRef,pieceRefConn):
        ## Problème avec les changements d'attribut, les pièce ce font selon la piecereference
        if pieceRef.__dict__["conn"+str(pieceRefConn)+"Cat"] != "BRIDE":
            typeLiaison= input(f"PRECISION DE LIAISON:\nPIECE REFERENCE:{pieceRef.name},{pieceRef.ref+1} ET PIECE CONNECTÉE {self.name},{self.ref+1} \nCette liaison nécessite une précision\t STD,STD+VI,EXPRESS,EXPRESS+VI\n")
        else:
            typeLiaison=pieceRef.__dict__["conn"+str(pieceRefConn)+"Cat"]

        LIAISON(pieceRef,pieceRefConn,pieceRef.__dict__["conn"+str(pieceRefConn)+"Cat"],str(typeLiaison))
        return typeLiaison
###########################################################################################################################################
"""---------------------------------------------CREATION DE L'OBJET LIAISON.---------------------------------------------"""
###########################################################################################################################################
class LIAISON:
    def __init__(self, parentsLiaisonREF, parentsLiaisonREFConn, typeConnex, typeLiaison):
        self.ref = parentsLiaisonREF.ref
        self.parent = parentsLiaisonREF
        typeConnex = "EMBOITEMENT" if typeConnex == "BOUTMALE" else typeConnex

        dataBase_Adequat = db_Jonctions[str(typeConnex)]
        self.tarif = 0

        paramLiaison = self.checkPropagation(parentsLiaisonREF, parentsLiaisonREFConn)
        self.findPieceLiaison(paramLiaison[2], paramLiaison[1], dataBase_Adequat, typeLiaison)
        liaisons.append(self)


    def checkPropagation(self, parentsLiaisonREF, parentsLiaisonREFConn):
        return [parentsLiaisonREF.__dict__["conn" + str(parentsLiaisonREFConn) + "Link"].__dict__[str(key)]
                if not value else parentsLiaisonREF.__dict__[str(key)]
                for key, value in parentsLiaisonREF.listprop[parentsLiaisonREFConn - 1].items()]
    
    def findPieceLiaison(self, PN, DN, dataBasePandas, typeLiaison):
        # Filtrage par Pression
        if "PN" in dataBasePandas.columns:
            dataFiltre_PN = dataBasePandas[dataBasePandas['PN'] == PN]
        elif "PFA" in dataBasePandas.columns:
            dataFiltre_PN = dataBasePandas[dataBasePandas['PFA'] >= PN]
        else:
            return None

        # Filtrage par DN
        dataFiltre_DN = dataFiltre_PN[dataFiltre_PN['DN'] == int(DN)]
        if dataFiltre_DN.empty:
            return None

        # Filtrage par type de liaison (sauf pour "BRIDE")
        if typeLiaison != "BRIDE" and "TYPE" in dataBasePandas.columns:
            dataFiltre_Type = dataFiltre_DN[dataFiltre_DN['TYPE'] == typeLiaison]
            if dataFiltre_Type.empty:
                return None
            dataFiltre = dataFiltre_Type
        else:
            dataFiltre = dataFiltre_DN

        # Extraction des valeurs pertinentes
        self.tarif = dataFiltre["Prix"].tolist()[0]
        ensemble = dataFiltre["Ensemble"].tolist()[0]
        if ensemble is not None:
            temp = ensemble.split(' - ')
            valueCoeff = [data.split(':')[0] for data in temp]
            nameCat = [data.split(':')[1] for data in temp]
            self.ensemble = {nameCat[i]: valueCoeff[i] for i in range(len(temp))}

        return None

###########################################################################################################################################
"""---------------------------------------------CREATION DES PARAMETRES ET DES ZONES TESTS.---------------------------------------------"""
###########################################################################################################################################
listAuthorizedCatRef={"BRIDE":["BRIDE"],
                      "EMBOITEMENT":["BOUTMALE"],
                      "BOUTMALE":["EMBOITEMENT"]}

listNameToCheck={"MANCHON":["mat","Quelle materiau"]}

pieces=[] ##A DECLARER DANS UNE CLASS SETUP
liaisons=[] ##A DECLARER DANS UNE CLASS SETUP
def addPiece(Name,ANGLE=0):
    ref = len(pieces)
    match Name: 
        case "BE":
            return PIECE(ref,Name,("EMBOITEMENT","BRIDE"))
        case "VANNE":
            return PIECE(ref,Name,("BRIDE","BRIDE"))
        case "BU":
            return PIECE(ref,Name,("BOUTMALE","BRIDE"))
        case "TÉ EMBOITEMENT":
            return PIECE(ref,Name,("EMBOITEMENT","EMBOITEMENT","BRIDE"),propaConn3=[True,False,True])
        case "TÉ BRIDE":
            return PIECE(ref,Name,("BRIDE","BRIDE","BRIDE"),propaConn3=[True,False,True])
        case "TUYAUX M-F":
            return PIECE(ref,Name,("BOUTMALE","EMBOITEMENT"))
        case "TUYAUX M-M": #COUPE
            return PIECE(ref,Name,("BOUTMALE","BOUTMALE"))
        case "COUDE EMBOITEMENT": 
            return PIECE(ref,Name,("EMBOITEMENT","EMBOITEMENT"),ANGLE=ANGLE)
        case "COUDE EMBOITEMENT": 
            return PIECE(ref,Name,("BRIDE","BRIDE"),ANGLE=ANGLE)
        case "CONE EMBOITEMENT":
            return PIECE(ref,Name,("EMBOITEMENT","EMBOITEMENT"),propaConn2=[True,False,True])
        case "CONE BRIDE":
            return PIECE(ref,Name,("BRIDE","BRIDE"),propaConn2=[True,False,True])
        case "TERMINAISON":
            return PIECE(ref,Name,(["BRIDE"]))
        case "BRANCHEMENT":
            return PIECE(ref,Name,("EMBOITEMENT","EMBOITEMENT","BOUTMALE"),propaConn3=[True,False,False])
        case "MANCHON":
            return PIECE(ref,Name,("EMBOITEMENT","EMBOITEMENT"))
        case "MANCHON TRANSITION":
            return PIECE(ref,Name,("EMBOITEMENT","EMBOITEMENT"),propaConn2=[False,True,True])
        case "ADAPTATEUR DE BRIDE":
                return PIECE(ref,Name,("EMBOITEMENT","BRIDE"),propaConn2=[False,True,True])

def setuptemp():
    Piece1=addPiece("TUYAUX M-M")
    Piece2 =addPiece("TUYAUX M-F")
    Piece3=addPiece("TÉ EMBOITEMENT")
    Piece4=addPiece("TERMINAISON")
    Piece5=addPiece("BU")
    Piece6=addPiece("CONE BRIDE")
    Piece7=addPiece("VANNE") 
    Piece8=addPiece("TERMINAISON")
    Piece9=addPiece("VANNE") 
    Piece10=addPiece("BE") 
    return Piece1,Piece2,Piece3,Piece4,Piece5,Piece6,Piece7,Piece8,Piece9,Piece10
Piece1,Piece2,Piece3,Piece4,Piece5,Piece6,Piece7,Piece8,Piece9,Piece10=setuptemp()

Piece2.associatedPieces(2,Piece1,2,listAuthorizedCatRef)

Piece3.associatedPieces(1,Piece2,1,listAuthorizedCatRef) 
Piece4.associatedPieces(1,Piece3,3,listAuthorizedCatRef) 
Piece5.associatedPieces(1,Piece3,2,listAuthorizedCatRef) 

Piece6.associatedPieces(1,Piece5,2,listAuthorizedCatRef)
Piece7.associatedPieces(1,Piece6,2,listAuthorizedCatRef)
Piece8.associatedPieces(1,Piece7,2,listAuthorizedCatRef)

Piece9.associatedPieces(1,Piece3,3,listAuthorizedCatRef)
Piece10.associatedPieces(1,Piece9,2,listAuthorizedCatRef)
comptLiaison(liaisons),comptPieces(pieces)

