import tkinter as tk
import V4_Visuel as vs


class BRAIN(vs.MainFrame):
    def __init__(self) -> None:
        super().__init__()
        self.piece_names=["BE","VANNE","BU","TÉ EMBOITEMENT","TÉ BRIDE","TUYAUX M-F","TUYAUX M-M","COUDE EMBOITEMENT","COUDE BRIDE","CONE EMBOITEMENT","CONE BRIDE","PLAQUE PLEINE","BRANCHEMENT","MANCHON","MANCHON TRANSITION","ADAPTATEUR DE BRIDE"]
        self.all_cat=["EMBOITEMENT","BRIDE","AUTRES"]
        self.listMotMontage=["BE","BE"]
        self.rowSelected=None

        self.mainFrame=vs.MainFrame
        self.leftFrame,self.selectMenu,self.buttonArea = vs.LeftFrame(self.mainFrame,self.piece_names)
        #self.middleFrame=vs.MiddleFrame(self)

    def MainPage(self,main):
        nom_fichier="Fichier test" ##A gerer avec le import plus tard
        main.title(f"Interface fichier: {nom_fichier}")
        window_width = main.winfo_screenwidth() // 2
        window_height = main.winfo_screenheight()
        main.geometry(f"{window_width-50}x{window_height}+0+0")

    def MiddleFunc(*listMotMontage,rowSelected):
        vs.MiddleFrame(*listMotMontage,rowSelected)

    
def main():
    app = BRAIN()
    app.mainloop()

if __name__ == "__main__":
    main()