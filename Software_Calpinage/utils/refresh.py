import tkinter as tk
from tkinter import ttk
from modules import compter,pieces
from tests import nameOfFunctionCalled as tst
from gui import buttonCommand 
from tkinter import messagebox

@tst.show_function_name
def refreshLabel(selectorFrame:tk,sharedVar):
    for widget in selectorFrame.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(text=sharedVar.catSelected)         

@tst.show_function_name
def refreshButtons(buttonFrame:tk,middleFrame:tk,bottomFrame:tk,infoPieceFrame:tk,sharedVar,buttonCommand):
    for child in buttonFrame.winfo_children():
        child.destroy()
    for piece in sharedVar.allPiecesAvailables:
        if piece["Cat"] == sharedVar.catSelected:
            button=tk.Button(buttonFrame , text = piece["Nom"],command= lambda namePiece=piece["Nom"]:  buttonCommand(middleFrame,bottomFrame,infoPieceFrame,sharedVar,namePiece))
            button.pack(pady=10,expand=False)
            print(f"Button created {piece['Nom']}")

@tst.show_function_name
def refreshPromptPiece(middleFrame:tk,infoPieceFrame:tk,bottomFrame:tk,sharedVar):
    middleFrame=sharedVar.tkinterObject["pieceFrame"]
    @tst.show_function_name(color="WARNING")
    def checkAvertissementPiece(thePiece,sharedVar):
        #il faut mettre la celulle en jaune
        #Contexte : if (sharedVar.rowSelect is not None and sharedVar.indexSelect is None) or  (sharedVar.indexSelect is not None and len(sharedVar.suiteMontageActuel[sharedVar.rowSelect])<=sharedVar.indexSelect+1)
        # On a une rowSelect mais pas de cell
        if (thePiece.typeWarning or thePiece.verWarning) and  (thePiece.typePiece is None or thePiece.verPiece is None):
            for row,index in thePiece.indicesPlace:
                sharedVar.labelRows[row][index].config(bg="yellow")

                if sharedVar.paramMontageActuel[row][index] is None:
                    sharedVar.paramMontageActuel[row][index]={}
                sharedVar.paramMontageActuel[row][index]["warning"]={}

        if thePiece.typeWarning:
            sharedVar.paramMontageActuel[row][index]["warning"]["typePiece"]=thePiece.typePiece
        if thePiece.verWarning:
            sharedVar.paramMontageActuel[row][index]["warning"]["verPiece"] = thePiece.verPiece
 
    @tst.show_function_name
    def on_row_click(event,isTheMaster):
        rowClick = event.widget.grid_info()['row'] if isTheMaster else event.widget.master.grid_info()['row']
        sharedVar.set_variable("rowSelect",rowClick)
        sharedVar.set_variable("indexSelect",None)
        for row,row_labels in enumerate(sharedVar.labelRows):
            for index,label in enumerate(row_labels):
                label.config(relief=tk.RIDGE,borderwidth=2,bg='white')
        for label in sharedVar.labelRows[rowClick]:
            label.config(relief=tk.SOLID, borderwidth=2)
        checkAvertissementPiece(sharedVar.suiteMontageActuel[row][index],sharedVar)
        for widget in infoPieceFrame.winfo_children():
            if isinstance(widget, ttk.Treeview):
                for child in widget.get_children():
                    widget.delete(child)

    @tst.show_function_name
    def on_label_double_click(event):
        ##mettre a jour la celulle select
        try:
            sharedVar.set_variable("indexSelect",sharedVar.labelRows[sharedVar.rowSelect].index(event.widget))
        except IndexError:
            eventLabelPiece = event.widget.winfo_children()[-1]
            sharedVar.set_variable("indexSelect",sharedVar.labelRows[sharedVar.rowSelect].index(eventLabelPiece))
        if len(sharedVar.suiteMontageActuel[sharedVar.rowSelect][sharedVar.indexSelect].indicesPlace)>1:
            ##Alors cette piece est responsable d'une autre connexion
            for row,index in sharedVar.suiteMontageActuel[sharedVar.rowSelect][sharedVar.indexSelect].indicesPlace:
                sharedVar.labelRows[row][index].config(bg='grey')
        else :
            sharedVar.labelRows[sharedVar.rowSelect][sharedVar.indexSelect].config(bg='grey')
        sharedVar.set_variable('backSpace', None)
        refreshInfoPieceFrame(infoPieceFrame,sharedVar)

    @tst.show_function_name
    def delete_selected_piece(event):
        if sharedVar.indexSelect is not None and sharedVar.backSpace is None: #On a lier cela a un bind_all donc il faut verifier
            montage=sharedVar.suiteMontageActuel.copy()
            label= sharedVar.labelRows.copy()
            pieceSelect=montage[sharedVar.rowSelect][sharedVar.indexSelect] #On enleve la piece de la copie du montage

            #on modifie les connexions des pieces en amont et en avale
            try :
                connPieceBefore=montage[sharedVar.rowSelect][sharedVar.indexSelect-1].find_connection_of_piece(pieceSelect)
                montage[sharedVar.rowSelect][sharedVar.indexSelect-1].__dict__[f"{connPieceBefore}Link"]=None
                print(f"\033[94m{montage[sharedVar.rowSelect][sharedVar.indexSelect-1].name} EN CONNEX {connPieceBefore}: VIDÉ\033[0m")
            except IndexError:
                print("Pas de pieceBefore a vidé")
                pass
            try :
                connPieceNext=montage[sharedVar.rowSelect][sharedVar.indexSelect+1].find_connection_of_piece(pieceSelect)
                montage[sharedVar.rowSelect][sharedVar.indexSelect+1].__dict__[f"{connPieceNext}Link"]=None
                print(f"\033[94m{montage[sharedVar.rowSelect][sharedVar.indexSelect+1].name} EN CONNEX {connPieceNext}: VIDÉ\033[0m")
            except IndexError:
                print("Pas de pieceNext a vidé")
                pass
            for row,index in pieceSelect.indicesPlace:
                #Pour toute les places ou se situe la piece
                if index==0 and len(montage[row])>1: #Existe il d'autres piece sur cette ligne
                    #Alors on avertis qu'on va tout supprimer
                    response=messagebox.askyesnocancel("Suppression d'une pièce","Voulez-vous supprimer cette pièce car elle sera à l'origine de la suppression de toute la branche du montage ?")
                    if response:
                        montage.pop(row)
                        label.pop(row)
                    else: 
                        return
                else:
                    if len(montage[row][index:])>1:
                        #Si la piece qui est selectionnée est au milieu d'une rangée de piece
                        #On modifie le registre des piece suivante
                        for pieceStillHere in montage[row][index:]:
                            pieceStillHere.indicesPlace[1]-=1
                    montage[row].pop(index)
                    label[row].pop(index)
                    if len(montage[row])==0:    ##En cas d'extinction d'une ligne on nettoie les registres
                        montage.pop(row)
                        label.pop(row)
                        if sharedVar.indexSelect-1>0:
                            sharedVar.set_variable("indexSelect",sharedVar.indexSelect-1)
                        else :
                            sharedVar.set_variable("indexSelect",None)
            sharedVar.set_variable("suiteMontageActuel",montage)
            sharedVar.set_variable("labelRows",label)
            refreshPromptPiece(middleFrame,infoPieceFrame,bottomFrame,sharedVar)
            refreshTree(bottomFrame,sharedVar)

    for child in middleFrame.winfo_children():
        if isinstance(child,tk.Label):
            child.destroy()
    labelRows=[]
    for row in range(len(sharedVar.suiteMontageActuel)):
        rowObj=[]
        for col,piece in enumerate(sharedVar.suiteMontageActuel[row]):
            #Container de toute la cellule
            containerPieceParamFrame=tk.Label(middleFrame)
            containerPieceParamFrame.grid(row=row,column=col,pady=(40,0),sticky="nsew")

            #Container de la partie info piece
            containerLabelFrame = tk.Label(containerPieceParamFrame)
            containerLabelFrame.grid(row=0,column=0,sticky="nsew")
            if sharedVar.paramMontageActuel[row][col]:
                ##Remplissage de la partie info piece si necessaire 
                for index,(key,value) in enumerate(flatten_dict(sharedVar.paramMontageActuel[row][col]).items()):
                    label_column = index * 2
                    entry_column = index * 2 + 1

                    paramLabelFrame=tk.Label(containerLabelFrame,text=str(key))
                    paramLabelFrame.grid(row=0,column=label_column)
                    paramEntryFrame = tk.Label(containerLabelFrame,text=str(value),width=3)
                    paramEntryFrame.grid(row=0,column=entry_column)
            ##Creation des label des pieces
            pieceLabel = tk.Label(containerPieceParamFrame,text=str(piece.name),relief=tk.RIDGE,width=15,height=1,bg='white')
            pieceLabel.grid(row=1,column=0,sticky="s")

            rowObj.append(pieceLabel)

            containerPieceParamFrame.bind('<Button-1>',lambda event:on_row_click(event,isTheMaster=True))
            pieceLabel.bind('<Button-1>',lambda event:on_row_click(event,isTheMaster=False))
            containerPieceParamFrame.bind('<Double-Button-1>',on_label_double_click)
            pieceLabel.bind('<Double-Button-1>',on_label_double_click)
            pieceLabel.bind_all('<BackSpace>',lambda event :delete_selected_piece(event))
            #containerLabelFrame.bind_all('<Return>',entryParam) 
        labelRows.append(rowObj)
    sharedVar.set_variable("labelRows",labelRows)
     
    try:
        checkAvertissementPiece(piece,sharedVar)
    except UnboundLocalError:pass

@tst.show_function_name
def refreshTree(bottomFrame,sharedVar):
    for widget in bottomFrame.winfo_children():
        if isinstance(widget, ttk.Treeview):
            widget.destroy()
    tree = ttk.Treeview(bottomFrame)
    if sharedVar.stateOfButtons["Pieces"]:
        listComptage=compter.comptPieces(sharedVar)
    elif sharedVar.stateOfButtons["Liaisons"]:
        listComptage=compter.comptLiaison(sharedVar)
    else:
        listComptage=[]
    def on_item_click(event):
        item = tree.focus()# Récupérer l'élément (item) sélectionné
        values = tree.item(item,"values")# Récupérer les valeurs de cet élément

    if len(listComptage)>0:
        allColumns=[f"col{i}" for i in range(len(listComptage[0])-1)] 
        tree["columns"] = tuple(allColumns)
        tree.heading("#0", text="id") 
        tree.column("#0",width=5)  
        ##Creation en-tete
        for i in range(len(listComptage[0])-1): 
            tree.heading(f"col{i}", text=str(list(listComptage[0].keys())[i]))
            tree.column(f"col{i}") if i!=4 else tree.column(f"col{i}",width=15)  # Configurer les colonnes pour qu'elles s'ajustent automatiquement
        ##Remplissage des lignes
        valuesOfComptage=[dictComptage.values() for dictComptage in listComptage]
        for indicBifurc,_ in enumerate(listComptage):
            tree.insert("", "end", text=str(indicBifurc), values= tuple(valuesOfComptage[indicBifurc]))#("Valeur 1.1", "Valeur 1.2")
    tree.bind("<Button-1>", on_item_click)
    # Ajouter l'arbre à la fenêtre
    tree.pack(fill="both", expand=True)

def flatten_dict(input_dict):
    output_dict = {}
    if input_dict is not None:
        for key, value in input_dict.items():
            if key == "warning":
                for keyW, valueW in value.items():
                    output_dict[keyW]=valueW
            else:
                output_dict[key] = value
        return output_dict
    return ""

@tst.show_function_name
def refreshInfoPieceFrame(infoPieceFrame,sharedVar,stateRefresh=False):
    for widget in infoPieceFrame.winfo_children():
        if isinstance(widget, ttk.Treeview):
            tree= widget
            if stateRefresh:
                tree.destroy()
                tree = ttk.Treeview(infoPieceFrame)
    if 'tree' not in locals() :
        tree = ttk.Treeview(infoPieceFrame)
    tree["columns"] = ("col0")
    tree.heading("#0", text="Caractéristiques")
    tree.column("#0", stretch=tk.YES)
    tree.heading("col0", text="Valeurs")
    tree.column("col0", stretch=tk.YES)
    tree.tag_configure("modifiable", foreground="blue")
    tree.tag_configure("unmodifiable", foreground="black")
    tree.tag_configure("warning",foreground="red")
    tree.pack(fill="both", expand=True)

    if len(sharedVar.suiteMontageActuel) > 0:
        if len(sharedVar.suiteMontageActuel[sharedVar.rowSelect]) > 0:
            pieceSelect = sharedVar.suiteMontageActuel[sharedVar.rowSelect][sharedVar.indexSelect]
            infoPieceFrame.update_idletasks()
            pieceSelect.refreshInfo()
            if len(tree.get_children())<=0:
                for index,(key, value) in enumerate(pieceSelect.displayInfo.items()):
                    keyForSearchAttr = key if key not in pieceSelect.translateGUItoVar else pieceSelect.translateGUItoVar[key]
                    try:
                        isModifiable=key in flatten_dict(sharedVar.paramMontageActuel[sharedVar.rowSelect][sharedVar.indexSelect]) or keyForSearchAttr in flatten_dict(sharedVar.paramMontageActuel[sharedVar.rowSelect][sharedVar.indexSelect]) or ("COUDE" in pieceSelect.name and keyForSearchAttr == "angle")
                        if sharedVar.paramMontageActuel[sharedVar.rowSelect][sharedVar.indexSelect] is not None:
                            isWarning = "warning" in sharedVar.paramMontageActuel[sharedVar.rowSelect][sharedVar.indexSelect] and keyForSearchAttr in sharedVar.paramMontageActuel[sharedVar.rowSelect][sharedVar.indexSelect]["warning"] and sharedVar.paramMontageActuel[sharedVar.rowSelect][sharedVar.indexSelect]["warning"][keyForSearchAttr] is None or ("COUDE" in pieceSelect.name and keyForSearchAttr == "angle")
                        else:
                            isWarning = ("COUDE" in pieceSelect.name and keyForSearchAttr == "angle")
                        if isModifiable:
                            #Si la variable est dans le param qui change
                            if isWarning:
                                #Si le key est aussi dans le warning alors
                                tree.insert("", "end", text=str(key), values=(f"{value}"), tags=("warning"))
                            else:
                                #sinon c'est qu'on a seulement la possibilite de modifier
                                tree.insert("", "end", text=str(key), values=(f"{value}"), tags=("modifiable",))
                        else:
                            if isWarning:
                                #Si le key est aussi dans le warning alors
                                tree.insert("", "end", text=str(key), values=(f"{value}"), tags=("unmodifiable","warning",))
                            else:
                                tree.insert("", "end", text=str(key), values=(f"{value}"), tags=("unmodifiable",))
                        
                    except TypeError:
                        tree.insert("", "end", text=str(key), values=(f"{value}"), tags=("unmodifiable",))
            
            # Lier l'événement double-clic pour permettre l'édition des cellules
            tree.bind("<Double-1>", lambda event: edit_treeview_cell(event, tree,sharedVar))
    
    
    @tst.show_function_name
    def edit_treeview_cell(event, tree,sharedVar):
        sharedVar.set_variable('backSpace', "treeview")
        item = tree.selection()[0]
        column_hastag = tree.identify_column(event.x)
        column = int(column_hastag.replace("#", ""))  # Convertir "#1" en 0-based index

        selected_iid=tree.focus()
        
        if column_hastag == '#1' and not "unmodifiable" in tree.item(item, "tags") :
            column_box= tree.bbox(selected_iid,column_hastag)
            current_value = tree.item(item, "values")[column-1]
            entry_edit = tk.Entry(tree,width=column_box[2])
            entry_edit.place(x=column_box[0],y=column_box[1],w=column_box[2],h=column_box[3])

            @tst.show_function_name
            def save_edit(event,item,sharedVar):
                new_value = entry_edit.get()
                tree.item(item, values=(new_value,))
                pieceModifiable= sharedVar.suiteMontageActuel[sharedVar.rowSelect][sharedVar.indexSelect]

                for cell in tree.get_children():
                    varToChange=tree.item(cell,"text")
                    varToChange = varToChange if varToChange not in pieceModifiable.translateGUItoVar else pieceModifiable.translateGUItoVar[varToChange]
                    pieceModifiable.__dict__[varToChange] = tree.item(cell,"values")[0]
                    if sharedVar.paramMontageActuel[sharedVar.rowSelect][sharedVar.indexSelect] is not None:
                        if varToChange in sharedVar.paramMontageActuel[sharedVar.rowSelect][sharedVar.indexSelect]:
                            sharedVar.paramMontageActuel[sharedVar.rowSelect][sharedVar.indexSelect][varToChange] = tree.item(cell,"values")[0]
                    sharedVar.set_variable("suiteMontageActuel",sharedVar.suiteMontageActuel)
                pieceModifiable.refreshInfo()
                sharedVar.set_variable("paramMontageActuel",sharedVar.paramMontageActuel)
                entry_edit.destroy()
                checkPropagParam(sharedVar)
                refreshInfoPieceFrame(infoPieceFrame,sharedVar,stateRefresh=True)
                refreshAll(sharedVar)
           
            entry_edit.bind("<FocusOut>", lambda event :save_edit(event,item, sharedVar))
            entry_edit.bind("<Return>", lambda event :save_edit(event,item,sharedVar))
            
            entry_edit.insert(0,current_value)
            entry_edit.select_range(0,tk.END)
            entry_edit.focus_set()
          
@tst.show_function_name
def refreshNotebook(middleFrame,sharedVar):
    if len(middleFrame.tabs()) -2 >=len(sharedVar.montageForRaccord):
        for _ in range(len(middleFrame.tabs())-len(sharedVar.montageForRaccord)):
            last_tabs = middleFrame.tabs()[-2]
            middleFrame.forget(last_tabs)

@tst.show_function_name(color="HEADER")
def refreshMainWindowName(mainWindow,sharedVar):
    mainWindow.title(f"SADE - CALPINAGE - {sharedVar.fileName}")

@tst.show_function_name
def checkPropagParam(sharedVar):
    for bifurc in sharedVar.suiteMontageActuel:
        for prePiece,thePiece in zip(bifurc,bifurc[1:]):
            preConn = prePiece.find_connection_of_piece(thePiece)
            pieceConn=thePiece.find_connection_of_piece(prePiece)
            buttonCommand.dataPropagation(prePiece,int(preConn[-1]),thePiece,pieceConn,sharedVar)
            """for (preKey,preValue),(pieceKey,pieceValue) in zip(prePiece.displayInfo.items(),thePiece.displayInfo.items()):
                preKeyCheck = preKey if preKey not in prePiece.translateGUItoVar else prePiece.translateGUItoVar[preKey]
                pieceKeyCheck = pieceKey if pieceKey not in thePiece.translateGUItoVar else thePiece.translateGUItoVar[pieceKey]
                    
                if preValue != pieceValue and preKeyCheck in prePiece.listProp[int(preConn[-1])]:
                    thePiece.__dict__[pieceKeyCheck]= prePiece.__dict__[preKeyCheck]
                   
                


                if preVar:
                    #Si le param se propage pas
                    if preVar != pieceVar:
                        #Si il n'est pas deja propager alors on le fait
                        thePiece.__dict__[f"{pieceConn}Propag"]=prePiece.__dict__[f"{preConn}Propag"]
                else:
                    #Si il ne se propage pas 
                    pass
                """
@tst.show_function_name
def refreshAll(sharedVar):
    mainWindow=sharedVar.tkinterObject["mainWindow"]
    leftFrame=sharedVar.tkinterObject["leftFrame"]
    selectorFrame=sharedVar.tkinterObject["selectorFrame"]
    buttonFrame=sharedVar.tkinterObject["buttonFrame"]
    middleFrame=sharedVar.tkinterObject["middleFrame"]
    bottomFrame=sharedVar.tkinterObject["bottomFrame"]
    infoPieceFrame=sharedVar.tkinterObject["infoPieceFrame"]
    selectorFrame=sharedVar.tkinterObject["selectorFrame"]

    refreshLabel(selectorFrame,sharedVar)
    refreshButtons(buttonFrame,middleFrame,bottomFrame,infoPieceFrame,sharedVar,buttonCommand.command)
    refreshPromptPiece(middleFrame,infoPieceFrame,bottomFrame,sharedVar)
    refreshTree(bottomFrame,sharedVar)
    refreshNotebook(middleFrame,sharedVar)
    refreshInfoPieceFrame(infoPieceFrame,sharedVar)

    

