import pandas as pd

###########################################################################################################################################
"""--------------------------------------------CREATION COMPLÈTE DE L'ASSOCIATION DE PIÈCES--------------------------------------------"""
###########################################################################################################################################

###########################################################################################################################################
"""---------------------------------------------------------GESTION DES ASSETS---------------------------------------------------------"""
###########################################################################################################################################

db_Jonctions = pd.read_excel("BaseDonnée_Jonctions.xlsx",sheet_name=None)
db_Pieces = pd.read_excel("BaseDonnée_Pieces.xlsx",sheet_name=None)
db_Connexions = pd.read_excel("BaseDonnée_Connexions.xlsx")

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
    def __init__(self,NAME:str,ListTYPEC:list,*propaConn,ANGLE=0)->None:
        ##Création des pieces : ref(autom),
        #propaConnI: propagation des attributs de la connexion I: list de Booléen concernant la propagation attributs à la pièce connectée dans l'ordre suivant: Mat,Dn,Pn
        listPropagationConn=[propaConn[i] for i in range(len(propaConn))][0]
        _listPropagationType=['mat','dn','pn']
        self.ref=len(pieces)
        self.name = NAME
        self.mat,self.dn,self.pn,self.typePiece,self.verPiece=None,None,None,None,None
        self.angle = ANGLE
        self.tarif =0
        self.longueur =3
        self.dVerrouille = 0 
        self.listProp = [{_listPropagationType[param]:listPropagationConn[conn][param] for param in range(len(_listPropagationType))} for conn in range(len(listPropagationConn))]
        self.nbConnex = len(ListTYPEC)

        for i in range(self.nbConnex):
            conn = "conn"+str(i+1)
            self.__dict__[conn+"Propag"] = self.listProp[i]
            self.__dict__[conn+"Cat"] =ListTYPEC[i]
            self.__dict__[conn+"Link"] = None

        if self.ref == 0 : ## Si première pièce
            self.statutReference = True
            self.userQuestion("FIRST")
        else : self.statutReference = False
        pieces.append(self)

    def isCatConnexAuthorized(self,selfConn,autrePiece,autrePieceConn,listAuthorizedCatRef):
        ##Vérifie si la connexion peut être efffectuer entre telle et telle piece
        selfCat=self.__dict__["conn"+str(selfConn)+"Cat"]
        autrePieceCat= autrePiece.__dict__["conn"+str(autrePieceConn)+"Cat"]
        try :
            if autrePieceCat in listAuthorizedCatRef[selfCat]:  return True
            else:   return False
        except KeyError: return False
        
    def associatedPieces(self,selfConn,pieceRef,pieceRefConn,listAuthorizedCatRef):
        if pieceRef.statutReference : ##On vérifie que la pièce sur laquelle on se connecte est deja connecté
            #if self.isCatConnexAuthorized(selfConn,pieceRef,pieceRefConn,listAuthorizedCatRef):
            self.__dict__["conn"+str(selfConn)+"Link"] = pieceRef
            pieceRef.__dict__["conn"+str(pieceRefConn)+"Link"] = self
            self.statutReference = True
            self.__dataPropagation(selfConn,pieceRef,pieceRefConn)
            self.addLiaisonPiece(pieceRef,pieceRefConn)
            #else:print("PIECES INCOMPATIBLES")
        else: print("IL FAUT UNE PIECE AU MOINS CONNECTÉE")
   
    def __dataPropagation(self,selfConn,pieceRef,pieceRefConn):

        if pieceRef.__dict__["conn"+str(pieceRefConn)+"Cat"] !="BRIDE" : #si pieceRef n'est pas une bride
            self.typePiece = pieceRef.typePiece if pieceRef.typePiece else input("Quel type de piece: \tSTD \tEXPRESS\t")
            self.verPiece = pieceRef.verPiece if pieceRef.typePiece else input("Quel verrouillage de piece: \tVI \tVE\t None\t")    

        else : ##Si c'est une connexion entre BRIDE
            connexCat=["conn" + str(i) + "Cat" for i in range(1, self.nbConnex + 1) if i!= selfConn]
            for attr_name in connexCat: ## On vérifie si il existe des connexions sur la piece autre que bride
                if self.__dict__[attr_name]!="BRIDE": #Si il en existe il faut demander quelle type,ver
                    self.typePiece = input("Quel type de piece: \tSTD \tEXPRESS")
                    self.verPiece = input("Quel verrouillage de piece: \tVI \tVE\t None")

        for key,value in pieceRef.listProp[pieceRefConn-1].items():
            if value:
                self.__dict__[str(key)] = pieceRef.__dict__[str(key)]
            else :
                self.userQuestion("PROPAGATION",key)
        
    def addLiaisonPiece(self,pieceRef,pieceRefConn):
        typeLiaison = self.typePiece
        LIAISON(pieceRef,pieceRefConn,pieceRef.__dict__["conn"+str(pieceRefConn)+"Cat"],str(typeLiaison))
    
    def distanceVerouille(self,dn,hCouverture)->int:
        ##Pour l'instant on rentre a la main la distance mais a terme on utilisera les abaques
        distance=12
        return distance
    def userQuestion(self,strCheckWhat,key=None)->None:
        if strCheckWhat=="FIRST" :
            ##on demande le DN le MAT et le PN
            #user=input("PREMIERE PIECE :\n\t Respectivement et en séparant par une virgule, quels sont: le matériau | le diamètre nominal (DN) | la pression nominal (PN):\t").split(',')
            user=('FONTE',60,10)
            self.mat = str(user[0])
            self.dn = int(user[1])
            self.pn=int(user[2])
            return
        if strCheckWhat=="PROPAGATION":
            self.__dict__[str(key)] = UserNeeded.BackToFront(f"PIÈCE {self.name} #{self.ref} EST CONNECTEE A UNE PIECE QUI NE PROPAGE PAS SON ATTRIBUT:\t{key}\nVeuillez entrer sa nouvelle valeur\t")
    
###########################################################################################################################################
"""---------------------------------------------CREATION DE L'OBJET LIAISON.---------------------------------------------"""
###########################################################################################################################################
class LIAISON:
    def __init__(self, parentsLiaisonREF, parentsLiaisonREFConn, typeConnex, typeLiaison):
        self.ref = parentsLiaisonREF.ref
        self.parent = parentsLiaisonREF
        typeConnex = "EMBOITEMENT" if typeConnex == "BOUT MALE" else typeConnex

        dataBase_Adequat = db_Jonctions[str(typeConnex)]
        self.tarif = 0

        paramLiaison = self.checkPropagation(parentsLiaisonREF, parentsLiaisonREFConn)
        self.ensemble=self.findPieceLiaison(paramLiaison[2], paramLiaison[1], dataBase_Adequat, typeLiaison)
        liaisons.append(self)


    def checkPropagation(self, parentsLiaisonREF, parentsLiaisonREFConn):
        return [parentsLiaisonREF.__dict__["conn" + str(parentsLiaisonREFConn) + "Link"].__dict__[str(key)]
                if not value else parentsLiaisonREF.__dict__[str(key)]
                for key, value in parentsLiaisonREF.listProp[parentsLiaisonREFConn - 1].items()]
    
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
            return {nameCat[i]: valueCoeff[i] for i in range(len(temp))}

        return None
##############################################################################################################################################
"""-----------------------------------------------------------------CORTEX-----------------------------------------------------------------"""
#############################################################################################################################################
class BRAIN :   
    def constructor(*listMotMontage):
        listMontage=([BRAIN.createPiece(nom,db_Connexions) for nom in montageMot] for montageMot in listMotMontage)
        BRAIN.associator(listAuthorizedCatRef,listMontage)
    
    def createPiece(nom,dataBasePandas):
        nom,connexionType,propaConn= BRAIN.searchPiece(nom,dataBasePandas)
        return PIECE(nom,connexionType,propaConn)
    
    def searchPiece(nom,dataBasePandas):
        rowNom = dataBasePandas[dataBasePandas["NOM"]==nom]
        connexionType=[]
        propaConn=[]
        for conn in range(1,4) :##3 connexions max
            print(rowNom["CONNEXION "+str(conn)])
            if not rowNom["CONNEXION "+str(conn)].isnull().tolist()[0]:
                connexionType.extend(rowNom["CONNEXION "+str(conn)].tolist())
                connType_cell=rowNom.columns.get_loc("CONNEXION " + str(conn))
                propaConn.append(rowNom.iloc[0,1+connType_cell:4+connType_cell].isnull().tolist())
        return (nom,connexionType,propaConn)
    def associator(listAuthorizedCatRef,*listMontage:list): #[Piece 1 Piece2, Te, Piece3,Piece4][te,Piee5,Piece6]...
        #Pour toute les bifurcation qui il y a 
        noeudPiece,repriseNoeud,offset=[],False,0
        #print("listMontage :",listMontage)
        for listPieces in listMontage[0]:
            #print("listPieces :",listPieces)
            ## Si on a une piece dans la liste de bifurcation il faut poser la lquestion de qui est la piece precedente
            if len(noeudPiece)>=1:
                #print("Noeud disponible: ",noeudPiece) ##Noeud disponible
                indexSelect=int(input(f"Sur quel piece se connecte-t-on?\nNoeud disponible: \t{[{index:item.name} for index,item in enumerate(noeudPiece)][0]}"))
                repriseNoeud,offset=True,-1
                pieceActive=noeudPiece[indexSelect]
                noeudPiece.pop(indexSelect)## Il faut supprimer le noeud utiliser
            #Pour toute les pieces on check ou elle peuvent se connecter
            for i in range(offset,len(listPieces)-1):
                if not repriseNoeud:
                    pieceActive,pieceNext = listPieces[i],listPieces[i+1]
                else:
                    pieceNext,repriseNoeud,offset = listPieces[0],False,0
                if pieceActive.nbConnex>2:
                    ##On stocke la piece (ou la connexion) dans une liste
                    noeudPiece.append(pieceActive)

                ## On stocke les point de connexions compatibles a la suivante
                pieceConnexCat=["conn" + str(i) + "Link" for i in range(1, pieceActive.nbConnex + 1)]
                pieceNextConnexCat=["conn" + str(i) + "Link" for i in range(1, pieceNext.nbConnex + 1)]
                
                listConn=[(ipieceActive, ipieceNext) for ipieceActive in range(1,pieceActive.nbConnex+1) for ipieceNext in range(1,pieceNext.nbConnex+1) if pieceActive.isCatConnexAuthorized(ipieceActive,pieceNext,ipieceNext,listAuthorizedCatRef) and not pieceActive.__dict__[pieceConnexCat[ipieceActive-1]] and not pieceNext.__dict__[pieceNextConnexCat[ipieceNext-1]]]
                print("Connexions possibles:",listConn)
                ##On prend seulement le premier couple dispo
                listConn=listConn[0]
                
                pieceNext.associatedPieces(listConn[1],pieceActive,listConn[0],listAuthorizedCatRef)
                
                ##TEST
                print(f'PIECE {pieceActive.name} CONN{listConn[0]} -to- PIECE {pieceNext.name} CONN{listConn[1]}')
                ##
##############################################################################################################################################
"""---------------------------------------------INTERACTION UTILISATEUR REQUISE-----------------------------------------------------------------"""
#############################################################################################################################################
    
class UserNeeded:
    def __init__(self) -> None:
        ##Data from Back
        self.titleQuestionBack = "testeur"
        self.repPossibleBack = None
        ##Data for Back
        self.repFrontForBack = None        
        pass
    def BackToFront(self,titleQuestion:str,repPossibleFromBack):
        self.titleQuestionBack=titleQuestion
        self.repPossibleBack=repPossibleFromBack
        ##Module de Visuel pour afficher et attendre la reponse de l'ut
      


###########################################################################################################################################
"""---------------------------------------------CREATION DES PARAMETRES ET DES ZONES TESTS.---------------------------------------------"""
###########################################################################################################################################
listAuthorizedCatRef={"BRIDE":["BRIDE"],
                      "EMBOITEMENT":["BOUT MALE"],
                      "BOUT MALE":["EMBOITEMENT"]}


pieces=[] ##A DECLARER DANS UNE CLASS SETUP
liaisons=[] ##A DECLARER DANS UNE CLASS SETUP

