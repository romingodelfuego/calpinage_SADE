import tkinter as tk
from utils import refresh 
from tests import nameOfFunctionCalled as tst

@tst.show_function_name
def createSelector(selectorFrame:tk,middleFrame:tk,bottomFrame:tk,infoPieceFrame:tk,sharedVar,varSetMethod,buttonFrame,buttonCommand) ->None:
    buttonPrevious=tk.Button(selectorFrame, text="<", command=lambda:select_previous(selectorFrame,middleFrame,bottomFrame,infoPieceFrame,sharedVar,varSetMethod,buttonFrame,buttonCommand), width=5)
    buttonPrevious.pack(side=tk.LEFT)

    buttonNext=tk.Button(selectorFrame, text=">", command=lambda:select_next(selectorFrame,middleFrame,bottomFrame,infoPieceFrame,sharedVar,varSetMethod,buttonFrame,buttonCommand), width=5)
    buttonNext.pack(side=tk.RIGHT)

    labelCat=tk.Label(selectorFrame,text=sharedVar.catSelected,width=20)
    labelCat.pack(pady=10)
    refresh.refreshButtons(buttonFrame,middleFrame,bottomFrame,infoPieceFrame,sharedVar,buttonCommand)

@tst.show_function_name 
def select_previous(selectorFrame:tk,middleFrame:tk,bottomFrame:tk,infoPieceFrame:tk,sharedVar,varSetMethod,buttonFrame,buttonCommand):
    varSetMethod("currentIndex",(int(sharedVar.currentIndex) - 1) % len(sharedVar.allCat))
    varSetMethod("catSelected", sharedVar.allCat[sharedVar.currentIndex])
    refresh.refreshLabel(selectorFrame,sharedVar)
    refresh.refreshButtons(buttonFrame,middleFrame,bottomFrame,infoPieceFrame,sharedVar,buttonCommand)

@tst.show_function_name
def select_next(selectorFrame:tk,middleFrame:tk,bottomFrame:tk,infoPieceFrame:tk,sharedVar,varSetMethod,buttonFrame,buttonCommand):
    varSetMethod("currentIndex",(int(sharedVar.currentIndex) + 1) % len(sharedVar.allCat))
    varSetMethod("catSelected", sharedVar.allCat[sharedVar.currentIndex])
    refresh.refreshLabel(selectorFrame,sharedVar)
    refresh.refreshButtons(buttonFrame,middleFrame,bottomFrame,infoPieceFrame,sharedVar,buttonCommand)

