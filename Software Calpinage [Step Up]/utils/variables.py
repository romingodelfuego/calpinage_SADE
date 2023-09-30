from data import *
from tests import nameOfFunctionCalled as tst
import tkinter as tk

class SharedVariables():
    @tst.show_function_name
    def __init__(self) -> None:
        self.filePath_db = {"Jonctions":"BaseDonnée_Jonctions.xlsx","Pieces":"BaseDonnée_Pieces.xlsx","Resume":"BaseDonnée_Resume.xlsx"}

        self.db_Jonctions = read_database("BaseDonnée_Jonctions.xlsx",sheet_name=None)
        self.db_Pieces = read_database("BaseDonnée_Pieces.xlsx",sheet_name=None)
        self.db_Resume = read_database("BaseDonnée_Resume.xlsx",sheet_name=0)
        self.savable_variable()
        self.unsavable_variable()
        self.other_variable()
    
    def savable_variable(self) -> None:
        self.filePath = None # Ou le backup ? par defaut
        self.fileName = None # Comment modifier ce nom ? 

        self.allCat= ["BRIDE","EMBOITEMENT","BOUT MALE"]
        self.allPiecesAvailables = [{"Nom":self.db_Resume["NOM"].tolist()[i],"Cat":self.db_Resume["CONNEXION 1"].tolist()[i]} for i in range(1,len(self.db_Resume["NOM"].tolist()))]
        
        self.listAuthorizedCatRef={"BRIDE":["BRIDE"],"EMBOITEMENT":["BOUT MALE"],"BOUT MALE":["EMBOITEMENT"]}
        
        self.suiteMontageActuel=[] ## [[piece1,piece2,piece3,cone],[]]
        self.paramMontageActuel=[] #[[{},None,None,None,{},None,None]] --> des que le param n'est pas none alors on affiche un tkLabel+tk.Entry
        self.montageForRaccord=[[]] #il faut fusionner les param et la suite : [[]]
        
    def unsavable_variable(self)->None:
        self.labelRows=[]
        self.stateOfButtons={"Pieces":False,"Liaisons":False}
    def other_variable(self)->None:
        self.raccordSelected=0
        self.currentIndex= 0  # Index initial sélectionné pour les catégorie
        self.rowSelect= 0
        self.catSelected=self.allCat[self.currentIndex]
        self.indexSelect=None

    
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



    
        

