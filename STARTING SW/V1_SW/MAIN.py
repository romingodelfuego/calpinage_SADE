import pandas as pd
from FRONT import InterfaceUtilisateur

class STORAGE_PIECE:
    def __init__(self) -> None:
        self.piecesObj =[]
        self.piecesNames=[piece_Obj.name for piece_Obj in self.piecesObj]
    

class STORAGE_LIAISON:
    def __init__(self) -> None:
        self.liaisonsObj =[]
        self.liaisonsNames=[liaison_Obj.name for liaison_Obj in self.liaisonsObj]
    
    
class EXCEL_DATA:
    def __init__(self) -> None:
        self.db_Jonctions = pd.read_excel("BaseDonnée_Jonctions.xlsx",sheet_name=None)
        self.db_Pieces = pd.read_excel("BaseDonnée_Pieces.xlsx",sheet_name=None)
        self.db_Connexions = pd.read_excel("BaseDonnée_Connexions.xlsx") 

def main():
    general= ["BE","VANNE","BU","TÉ EMBOITEMENT","TÉ BRIDE","TUYAUX M-F","TUYAUX M-M","COUDE EMBOITEMENT","COUDE BRIDE","CONE EMBOITEMENT","CONE BRIDE","PLAQUE PLEINE","BRANCHEMENT","MANCHON","MANCHON TRANSITION","ADAPTATEUR DE BRIDE"]
    app = InterfaceUtilisateur(general,["TUYAUX M-M","TUYAUX M-F","TÉ EMBOITEMENT","BU","VANNE"])
    app.mainloop()

if __name__ == "__main__":
    main()