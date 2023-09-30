from modules import pieces as pc
from tests import nameOfFunctionCalled as tst
from utils import refresh
import tkinter as tk
import copy

@tst.show_function_name
def command(middleFrame:tk,bottomFrame:tk,infoPieceFrame:tk,sharedVar,namePiece):
    thePiece=createPiece(namePiece,sharedVar.db_Resume) ##type:PIECE
    if (sharedVar.rowSelect is not None and sharedVar.indexSelect is None) or  (sharedVar.indexSelect is not None and len(sharedVar.suiteMontageActuel[sharedVar.rowSelect])<=sharedVar.indexSelect+1): 
    #Si on a selectionner une ligne mais pas une celulle precise ou si on est en bout de ligne 
        if len(sharedVar.suiteMontageActuel)==0:
        ##Si c'est la toute premiere pièce posée
            checkCommandFirst(thePiece,sharedVar)
            checkNewRow(thePiece,sharedVar)
        else:
        ##Si c'est une autre piece que la toute premiere
            if len(sharedVar.suiteMontageActuel[sharedVar.rowSelect])!=0 :
            ###Si c'est une autre piece que la premiere d'une rangée
                lastPiece=sharedVar.suiteMontageActuel[sharedVar.rowSelect][-1]
                if not association(sharedVar,lastPiece,thePiece):
                     return 
                checkNewRow(thePiece,sharedVar)
    elif sharedVar.indexSelect is not None:
    #Si une celulle precise est selectionnée
        ##On ajoute les pieces a gauche de la suite
        pieceRef=sharedVar.suiteMontageActuel[sharedVar.rowSelect][sharedVar.indexSelect]
        pieceRefCopy=copy.copy(pieceRef)
        #find la piece connecte a pieceRef
        pieceRefNext=sharedVar.suiteMontageActuel[sharedVar.rowSelect][sharedVar.indexSelect+1]
        pieceRefNextCopy=copy.copy(pieceRefNext)

        connRefToRemove=pieceRef.find_connection_of_piece(pieceRefNextCopy)
        connNextToRemove=pieceRefNext.find_connection_of_piece(pieceRefCopy)
        if connRefToRemove:
             pieceRefCopy.__dict__[str(connRefToRemove)+"Link"]=None
             print(f"Removed {connRefToRemove} from pieceRef")
        if connNextToRemove:
             pieceRefNextCopy.__dict__[str(connNextToRemove)+"Link"]=None
             print(f"Removed {connNextToRemove} from pieceRefNext")

        if associablePieces(sharedVar,pieceRefCopy,thePiece):
            oldIndice=pieceRefNextCopy.indicesPlace[0]
            pieceRefNextCopy.indicesPlace[0]=(oldIndice[0],oldIndice[1]+1)

            sharedVar.suiteMontageActuel[sharedVar.rowSelect][sharedVar.indexSelect] = pieceRefCopy
            sharedVar.suiteMontageActuel[sharedVar.rowSelect][sharedVar.indexSelect+1] = pieceRefNextCopy

            thePiece.indicesPlace.append((sharedVar.rowSelect,sharedVar.indexSelect+1))
            sharedVar.paramMontageActuel[sharedVar.rowSelect].insert(sharedVar.indexSelect+1,update_paramMontage(thePiece))
            sharedVar.suiteMontageActuel[sharedVar.rowSelect].insert(sharedVar.indexSelect+1,thePiece)

            for pieces in sharedVar.suiteMontageActuel[sharedVar.rowSelect][sharedVar.indexSelect:]:
                 print(pieces)

            sharedVar.set_variable("suiteMontageActuel",sharedVar.suiteMontageActuel)
            sharedVar.set_variable("paramMontageActuel",sharedVar.paramMontageActuel)
            checkNewRow(thePiece,sharedVar)

    
    
    refresh.refreshPromptPiece(middleFrame,infoPieceFrame,bottomFrame,sharedVar)
    refresh.refreshTree(bottomFrame,sharedVar)
        
@tst.show_function_name
def checkCommandFirst(thePiece,sharedVar):
        thePiece.statutReference=True
        thePiece.indicesPlace.append((0,0))
        
        sharedVar.paramMontageActuel.append([{key:value for key,value in list(thePiece.displayInfo.items())[1:]}])
        sharedVar.set_variable("paramMontageActuel",sharedVar.paramMontageActuel)

        sharedVar.suiteMontageActuel.append([thePiece])
        sharedVar.set_variable("suiteMontageActuel",sharedVar.suiteMontageActuel) 

@tst.show_function_name
def association(sharedVar,lastPiece,thePiece):
    if associablePieces(sharedVar,lastPiece,thePiece):
    ## Si elles sont associables
        thePiece.indicesPlace.append((sharedVar.rowSelect,len(sharedVar.suiteMontageActuel[sharedVar.rowSelect])))
        if sharedVar.rowSelect == 0 and len(sharedVar.suiteMontageActuel[sharedVar.rowSelect])==0:
            sharedVar.paramMontageActuel.append({"mat":None,"dn":None,"pn":None})
        else:
            sharedVar.paramMontageActuel[sharedVar.rowSelect].append(update_paramMontage(thePiece))
        sharedVar.suiteMontageActuel[sharedVar.rowSelect].append(thePiece)
        sharedVar.set_variable("paramMontageActuel",sharedVar.paramMontageActuel)
        sharedVar.set_variable("suiteMontageActuel",sharedVar.suiteMontageActuel)
        return True
    else:
    ## Si elles sont incompatibles
        print(f"PIECE {thePiece.name} & {lastPiece.name} SONT INCOMPATIBLES")
        return False
@tst.show_function_name
def checkNewRow(thePiece,sharedVar):
    if thePiece.nbConnex>2:
        ##Alors il faut ajouter une nouvelle branch
        thePiece.indicesPlace.append((len(sharedVar.suiteMontageActuel),0))
        sharedVar.suiteMontageActuel.append([thePiece])

        if sharedVar.rowSelect == 0 and len(sharedVar.suiteMontageActuel[sharedVar.rowSelect])==0:
            sharedVar.paramMontageActuel.append({"mat":None,"dn":None,"pn":None})
        else:
            sharedVar.paramMontageActuel.append([update_paramMontage(thePiece,2)])

        sharedVar.set_variable("paramMontageActuel",sharedVar.paramMontageActuel)
        sharedVar.set_variable("suiteMontageActuel",sharedVar.suiteMontageActuel)    
@tst.show_function_name
def update_paramMontage(piece,indice=1):
    paramDictPiece={}
    if len(piece.listProp)>1:
        for key,value in piece.listProp[indice].items():
            if not value:
                paramDictPiece[key]=None
        return None if len(paramDictPiece)==0 else paramDictPiece
    else :
         #Permet de gérer le cas des pieces a 1 seule connexion
         return None

@tst.show_function_name
def associablePieces(sharedVar,lastPiece,thePiece):
        def methodToConnectPiece(lastPieceConn,thePieceConn):
            thePiece.__dict__["conn"+str(thePieceConn)+"Link"] = lastPiece
            lastPiece.__dict__["conn"+str(lastPieceConn)+"Link"] = thePiece
            thePiece.statutReference = True
            dataPropagation(lastPiece,lastPieceConn,thePiece,thePieceConn,sharedVar)
            print(f'PIECE {lastPiece.name} CONN{lastPieceConn} -to- PIECE {thePiece.name} CONN{thePieceConn}')
            #self.addLiaisonPiece(lastPiece,lastPieceConn)
        
        linkConn =findCorrectLinkPoint(sharedVar,lastPiece,thePiece) ##(3,1),(3,2)
        if linkConn:
            if sharedVar.indexSelect ==0:
            #Si on selectionne un début de ligne
                listForConnectLastPiece = [linkConn[i][0] for i in range(len(linkConn))]
                try:
                    indexFind=listForConnectLastPiece.index(lastPiece.nbConnex)
                    lastPieceConn,thePieceConn= listForConnectLastPiece[indexFind],linkConn[indexFind][1]
                        #Si la derniere connexion de lastPiece est dans les possibilité de connexion alors on déroule
                    if lastPiece.statutReference : ##On vérifie que la pièce sur laquelle on se connecte est deja connecté
                        methodToConnectPiece(lastPieceConn,thePieceConn)
                        return True
                except ValueError:
                    pass

            else:
                lastPieceConn,thePieceConn= linkConn[0]
                if lastPiece.statutReference : ##On vérifie que la pièce sur laquelle on se connecte est deja connecté
                    methodToConnectPiece(lastPieceConn,thePieceConn)
                    return True

                else: print("IL FAUT UNE PIECE AU MOINS CONNECTÉE")
        else :  
            print("PIECES INCOMPATIBLES") 
            return 
@tst.show_function_name
def createPiece(nom,db_Resume)->pc.PIECE:
        nom,connexionType,propaConn= searchPiece(nom,db_Resume)
        return pc.PIECE(nom,connexionType,propaConn)
@tst.show_function_name
def searchPiece(nom,dataBaseForPiece)->tuple:
        rowNom = dataBaseForPiece[dataBaseForPiece["NOM"]==nom]
        connexionType=[]
        propaConn=[]
        for conn in range(1,4) :##3 connexions max
            if not rowNom["CONNEXION "+str(conn)].isnull().tolist()[0]:
                connexionType.extend(rowNom["CONNEXION "+str(conn)].tolist())
                connType_cell=rowNom.columns.get_loc("CONNEXION " + str(conn))
                propaConn.append(rowNom.iloc[0,1+connType_cell:4+connType_cell].isnull().tolist())
        return (nom,connexionType,propaConn)

@tst.show_function_name
def isConnexAuthorized(sharedVar,lastPiece,ilastPiece,thePiece,ithePiece)->bool:
        thePieceCat=thePiece.__dict__["conn"+str(ithePiece)+"Cat"]
        autrePieceCat= lastPiece.__dict__["conn"+str(ilastPiece)+"Cat"]
        try :
            if autrePieceCat in sharedVar.listAuthorizedCatRef[thePieceCat]:  return True
            else:   return False
        except KeyError: return False


@tst.show_function_name
def findCorrectLinkPoint(sharedVar,lastPiece,thePiece): #[Piece 1 Piece2, Te, Piece3,Piece4][te,Piee5,Piece6]...
            ## On stocke les point de connexions compatibles a la suivante
            lastPieceConnexCat=["conn" + str(i) + "Link" for i in range(1, lastPiece.nbConnex + 1)]
            thePieceConnexCat=["conn" + str(i) + "Link" for i in range(1, thePiece.nbConnex + 1)]
            
            listConn=[(ilastPiece, ithePiece) for ilastPiece in range(1,lastPiece.nbConnex+1) for ithePiece in range(1,thePiece.nbConnex+1) if isConnexAuthorized(sharedVar,lastPiece,ilastPiece,thePiece,ithePiece) and not lastPiece.__dict__[lastPieceConnexCat[ilastPiece-1]] and not thePiece.__dict__[thePieceConnexCat[ithePiece-1]]]
            print("Connexions possibles:",listConn)
            return listConn


@tst.show_function_name
def dataPropagation(lastPiece,lastPieceConn,thePiece,thePieceConn,sharedVar):
    if lastPiece.__dict__["conn"+str(lastPieceConn)+"Cat"] !="BRIDE" : #si lastPiece n'est pas une bride
        if lastPiece.typePiece:
            thePiece.typePiece = lastPiece.typePiece 
        else : thePiece.typeWarning = True 
        if lastPiece.typePiece:
            thePiece.verPiece = lastPiece.verPiece 
        else: thePiece.verWarning = True 
    else : ##Si c'est une connexion entre BRIDE
        connexCat=["conn" + str(i) + "Cat" for i in range(1, thePiece.nbConnex + 1) if i!= thePieceConn]
        for attr_name in connexCat: ## On vérifie si il existe des connexions sur la piece autre que bride
            if thePiece.__dict__[attr_name]!="BRIDE": #Si il en existe il faut demander quelle type,ver
                thePiece.typeWarning = True 
                thePiece.verWarning = True

    for key,value in lastPiece.listProp[lastPieceConn-1].items():
        if value:
                thePiece.__dict__[str(key)] = lastPiece.__dict__[str(key)]
        elif "second" in key:
                thePiece.__dict__[str(key[:-7])] = lastPiece.__dict__[str(key)]
