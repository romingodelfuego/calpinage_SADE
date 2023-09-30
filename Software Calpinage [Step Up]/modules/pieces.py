class PIECE :   
    def __init__(self,NAME:str,ListTYPEC:list,*propaConn,ANGLE=0)->None:
        ##Création des pieces : ref(autom),
        #propaConnI: propagation des attributs de la connexion I: list de Booléen concernant la propagation attributs à la pièce connectée dans l'ordre suivant: Mat,Dn,Pn
        listPropagationConn=[propaConn[i] for i in range(len(propaConn))][0]
        _listPropagationType=['mat','dn','pn']
        self.name = NAME
        self.mat,self.dn,self.pn,self.typePiece,self.verPiece=None,None,None,None,None
        self.angle = ANGLE
        self.tarif =0
        self.longueur =3
        self.dVerrouille = 0 
        self.listProp = [{_listPropagationType[param]:listPropagationConn[conn][param] for param in range(len(_listPropagationType))} for conn in range(len(listPropagationConn))]
        self.nbConnex = len(ListTYPEC)

        self.designation = None
        self.indicesPlace=[] # (row1,index1),(row2,index2) 2indices max
        self.translateGUItoVar={"matériau":"mat","type":"typePiece","verrouillage":"verPiece",}
        self.displayInfo={"name":self.name,"matériau":self.mat,"dn":self.dn,"pn":self.pn,"type":self.typePiece,"verouillage":self.verPiece,"angle":self.angle,"designation":self.designation}
        for i in range(self.nbConnex):
            conn = "conn"+str(i+1)
            self.__dict__[conn+"Propag"] = self.listProp[i]
            self.__dict__[conn+"Cat"] =ListTYPEC[i]
            self.__dict__[conn+"Link"] = None
        else : self.statutReference = False

    def refreshInfo(self):
        self.displayInfo={"name":self.name,"matériau":self.mat,"dn":self.dn,"pn":self.pn,"type":self.typePiece,"verouillage":self.verPiece,"angle":self.angle,"designation":self.designation}
   
    def find_connection_of_piece(self, target_piece):
        for i in range(self.nbConnex):
            conn = "conn" + str(i + 1)
            if self.__dict__[conn + "Link"] == target_piece:
                return conn
        return None
