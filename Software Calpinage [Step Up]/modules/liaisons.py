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
                                                  
        paramLiaison = self.checkPropagation(pieceRef, connexRef)
        self.ensemble=self.findPieceLiaison(paramLiaison[2], paramLiaison[1], dataBase_Adequat, catConnex)


    def checkPropagation(self, parentsLiaisonREF, connexRef):
        numeroConnex=int(connexRef.split("conn")[-1])
        return [parentsLiaisonREF.__dict__[str(connexRef) + "Link"].__dict__[str(key)]
                if not value else parentsLiaisonREF.__dict__[str(key)]
                for key, value in parentsLiaisonREF.listProp[ numeroConnex - 1].items()]
    
    def findPieceLiaison(self, PN, DN, dataBasePandas, catConnex):
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
    