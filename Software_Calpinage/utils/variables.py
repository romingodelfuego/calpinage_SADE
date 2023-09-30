import data
from tests import nameOfFunctionCalled as tst
import tkinter as tk
import datetime

class SharedVariables():
    @tst.show_function_name
    def __init__(self) -> None:
        self.default_filePath_db = {"Jonctions":"BaseDonnée_Jonctions.xlsx","Pieces":"BaseDonnée_Pieces.xlsx","Resume":"BaseDonnée_Resume.xlsx"}
        self.default_fileName=self.generate_default_filename()
        self.default_filePath="data//BackUp.sade"
        self.savable_variable()
        self.unsavable_variable()
        self.other_variable()

    
    def savable_variable(self) -> None:
        self.filePath = self.default_filePath 
        self.fileName = self.default_fileName 
        self.filePath_db= self.default_filePath_db

        self.refresh_db_excel()

        self.allCat= ["BRIDE","EMBOITEMENT","BOUT MALE"]
        self.allPiecesAvailables = [{"Nom":self.db_Resume["NOM"].tolist()[i],"Cat":self.db_Resume["CONNEXION 1"].tolist()[i]} for i in range(1,len(self.db_Resume["NOM"].tolist()))]
        
        self.listAuthorizedCatRef={"BRIDE":["BRIDE"],"EMBOITEMENT":["BOUT MALE"],"BOUT MALE":["EMBOITEMENT"]}
        
        self.suiteMontageActuel=[] ## [[piece1,piece2,piece3,cone],[]]
        self.paramMontageActuel=[] #[[{},None,None,None,{},None,None]] --> des que le param n'est pas none alors les param qui change
        self.montageForRaccord=[[]] #il faut fusionner les param et la suite : [[]]
        
    def unsavable_variable(self)->None:
        self.labelRows=[]
        self.stateOfButtons={"Pieces":True,"Liaisons":False}
        self.tkinterObject={}

    def other_variable(self)->None:
        self.raccordSelected=0
        self.currentIndex= 0  # Index initial sélectionné pour les catégorie
        self.rowSelect= 0
        self.catSelected=self.allCat[self.currentIndex]
        self.indexSelect=None
        self.backSpace=None

    
    @tst.show_function_name(color="OKCYAN",output=True,arg_name="variable_name")
    def set_variable(self, variable_name, value):
        # Vérifier si la variable existe dans l'objet
        if hasattr(self, variable_name):
            # Utiliser setattr pour mettre à jour la variable avec la nouvelle valeur
            setattr(self, variable_name, value)
            print(f"Variable {variable_name} is set. \t Value: {value}")
            return value
        else:
            print(f"Erreur : la variable {variable_name} n'existe pas dans l'objet SharedVariables.")
            return ValueError
        
    def dict_savable_variable(self):
        self.attrToSave = ["filePath","fileName","allCat","allPiecesAvailables","indexSelect","listAuthorizedCatRef","suiteMontageActuel","paramMontageActuel","montageForRaccord"]
        return {attr_name: getattr(self, attr_name) for attr_name in self.attrToSave}

    def generate_default_filename(self):
        now = datetime.datetime.now()
        formatted_date = now.strftime("%d.%m.%Y_%H.%M")
        return f"{formatted_date}"

    
    def refresh_db_excel(self):
        self.db_Jonctions = data.read_database(self.filePath_db["Jonctions"],sheet_name=None)
        self.db_Pieces = data.read_database(self.filePath_db["Pieces"],sheet_name=None)
        self.db_Resume = data.read_database(self.filePath_db["Resume"],sheet_name=0)
       
        

