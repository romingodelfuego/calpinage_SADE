from modules.pieces import PIECE
from modules.liaisons import LIAISON

def comptPieces(sharedVar):
    listComptage,offset=[],0
    for indicBifurc,montageBifurc in enumerate(sharedVar.suiteMontageActuel):
        if indicBifurc>0:
            offset=1
        for piece in montageBifurc[offset:]:
            piece.set_denominationPiece()
            statutAdd=False
            if len(listComptage)>0:
                for i in range(len(listComptage)):
                    if piece.designation in listComptage[i]["DESIGNATION"]:
                        listComptage[i]["QUANTITE"]+=1
                        listComptage[i]["PIECES"].append(piece)
                        listComptage[i]["PRIX"]+=piece.tarif
                        statutAdd = True
                        
                if not statutAdd:
                    ##On créer dans listComptage ce qu'il faut
                    listComptage.append({"DESIGNATION":piece.designation,"NAME":piece.name,"DN":piece.dn,"PN":piece.pn,"QUANTITE":1,"PRIX": piece.tarif,"PIECES":[piece]})
            else:
                listComptage.append({"DESIGNATION":piece.designation,"NAME":piece.name,"DN":piece.dn,"PN":piece.pn,"QUANTITE":1,"PRIX": piece.tarif,"PIECES":[piece]})
    return listComptage


def comptLiaison(sharedVar):
    listComptage=[]
    for indicBifurc,montageBifurc in enumerate(sharedVar.suiteMontageActuel):
        for index in range(len(montageBifurc)-1):
            statutAdd=False
            pieceRef = montageBifurc[index]
            pieceNext=montageBifurc[index+1]
            liaison=LIAISON(pieceRef,pieceNext,sharedVar)
            liaison.set_denominationLiaison()
            if len(listComptage)>0:
                for i in range(len(listComptage)):
                    if liaison.designation in listComptage[i]["DESIGNATION"]:
                                listComptage[i]["QUANTITE"]+=1
                                listComptage[i]["PIECES"].append(liaison)
                                listComptage[i]["PRIX"]+=liaison.tarif
                                statutAdd = True
                if not statutAdd:
                    ##On créer dans listComptage ce qu'il faut
                    for ss_ensemble in liaison.ensemble:    
                        listComptage.append({"DESIGNATION":ss_ensemble,"CHILD":"","DN":liaison.dn,"PN":liaison.pn,"QUANTITE":1,"PRIX": liaison.tarif,"PIECERef":[liaison.parent]})
            else:
                listComptage.append({"DESIGNATION":liaison.ensemble,"DN":liaison.dn,"PN":liaison.pn,"QUANTITE":1,"PRIX": liaison.tarif,"PIECERef":[liaison.parent]})
    return listComptage