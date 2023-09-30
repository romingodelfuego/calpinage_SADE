import copy
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
        self.listProp = [{_listPropagationType[param]:listPropagationConn[conn][param] for param in range(len(_listPropagationType))} for conn in range(len(listPropagationConn))]
        self.nbConnex = len(ListTYPEC)
        self.typeWarning=False
        self.verWarning=False
        self.designation = None
        self.indicesPlace=[] # (row1,index1),(row2,index2) 2indices max
        self.translateGUItoVar={"matériau":"mat","type":"typePiece","verrouillage":"verPiece",}
        self.displayInfo={"name":self.name,"matériau":self.mat,"dn":self.dn,"pn":self.pn,"type":self.typePiece,"verrouillage":self.verPiece,"angle":self.angle}
        self.create_attr_propagation()
        for i in range(self.nbConnex):
            conn = "conn"+str(i+1)
            self.__dict__[conn+"Propag"] = self.listProp[i]
            self.__dict__[conn+"Cat"] =ListTYPEC[i]
            self.__dict__[conn+"Link"] = None
        else : self.statutReference = False

    def refreshInfo(self):
        temp={}
        for key, _ in self.displayInfo.items():
            keyValue=key
            if key in self.translateGUItoVar:
                keyValue=self.translateGUItoVar[key]
            temp[key] = getattr(self, keyValue)
        self.displayInfo=temp

    def find_connection_of_piece(self, target_piece):
        for i in range(self.nbConnex):
            conn = "conn" + str(i + 1)
            if self.__dict__[conn + "Link"] == target_piece:
                return conn
        return None
    
    def findIdemPiece(self,suiteMontageActuel):
        for row in range(len(suiteMontageActuel)):
            for col,piece in enumerate(suiteMontageActuel[row]):
                if piece == self and (row,col) not in self.indicesPlace:
                    return (row,col)
                
    def set_denominationPiece(self):
        components= [f"{self.name} DN{self.dn} PN{self.pn}"]
        for intConnex in range(1, self.nbConnex + 1): 
                if False in self.__dict__[f"conn{intConnex}Propag"].values():##Cas du TÉ
                    if self.__dict__[f"conn{intConnex}Link"] is not None:
                        itemsData = self.__dict__[f"conn{intConnex}Link"] 
                        component = f"DN{itemsData.dn} PN{itemsData.pn}"
                        components.append(component)
        self.designation="-".join(components)

    def create_attr_propagation(self):
        dictPropConnCopy=copy.deepcopy(self.listProp)
        for index,dictPropConn in enumerate(self.listProp):
            for key,value in dictPropConn.items():
                if not value:
                    
                    dictPropConnCopy[index][str(key)]=True
                    dictPropConnCopy[index][str(key)+"_second"]=False
                    self.__dict__[str(key)+"_second"] = None
                    if key in self.displayInfo:
                        self.displayInfo[str(key)+"_second"] = None

        self.listProp=dictPropConnCopy
