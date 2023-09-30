from MAIN import EXCEL_DATA,STORAGE_PIECE

###########################################################################################################################################
"""--------------------------------------------CREATION COMPLÈTE DE L'ASSOCIATION DE PIÈCES--------------------------------------------"""
###########################################################################################################################################

###########################################################################################################################################
"""---------------------------------------------------------GESTION DES ASSETS---------------------------------------------------------"""
###########################################################################################################################################
data=EXCEL_DATA()
db_Jonctions = data.db_Jonctions
db_Pieces = data.db_Pieces
db_Connexions = data.db_Connexions


###########################################################################################################################################
"""---------------------------------------------CREATION DE L'OBJET PIECE.---------------------------------------------"""
###########################################################################################################################################
class PIECE :   
    def __init__(self,NAME:str,ListTYPEC:list,*propaConn,ANGLE=0)->None:
        from MAIN import STORAGE_PIECE

        ##Création des pieces : ref(autom),
        #propaConnI: propagation des attributs de la connexion I: list de Booléen concernant la propagation attributs à la pièce connectée dans l'ordre suivant: Mat,Dn,Pn
        listPropagationConn=[propaConn[i] for i in range(len(propaConn))][0]
        _listPropagationType=['mat','dn','pn']
        self.ref=len(STORAGE_PIECE.piecesObj)
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