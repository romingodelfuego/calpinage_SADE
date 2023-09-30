class LIAISON:
    def __init__(self, pieceRef, pieceNext,sharedVar):
        connexRef= pieceRef.find_connection_of_piece(pieceNext)
        catConnex = pieceRef.__dict__[str(connexRef) + "Cat"]
        if catConnex == "BOUT MALE" :
            catConnex = "EMBOITEMENT"

        self.liaisonCat=catConnex
        #self.ref = pieceRef.ref
        self.parent = pieceRef
        
        self.dn = pieceRef.dn
        self.pn =pieceRef.pn
        self.designation =None
        self.tarif = 0
        
        dataBase_Adequat = sharedVar.db_Jonctions[str(catConnex)]
                                                  
        try:
            self.ensemble=self.findPieceLiaison(int(pieceRef.pn), int(pieceRef.dn), dataBase_Adequat, catConnex)
        except TypeError:
            print("Renseigner toutes les valeurs necessaires avant d'avoir les pieces de liaisons")
            self.ensemble=[]
        except ValueError:
            print("Renseigner toutes les valeurs necessaires avant d'avoir les pieces de liaisons")
            self.ensemble=[]
    
    def findPieceLiaison(self, PN:int, DN:int, dataBasePandas, catConnex):
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
        if catConnex != "BRIDE" and "TYPE" in dataBasePandas.columns:
            dataFiltre_Type = dataFiltre_DN[dataFiltre_DN['TYPE'] == catConnex]
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
    
    def set_denominationLiaison(self):
        return self.ensemble