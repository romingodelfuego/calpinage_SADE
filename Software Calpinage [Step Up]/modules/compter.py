from modules.pieces import PIECE
from modules.liaisons import LIAISON

def comptPieces(sharedVar):
    def set_denominationPiece(piece):
        components= [f"{piece.name} DN{piece.dn} PN{piece.pn}"]
        for intConnex in range(1, piece.nbConnex + 1): 
                if False in piece.__dict__[f"conn{intConnex}Propag"].values():##Cas du TÉ
                    if piece.__dict__[f"conn{intConnex}Link"] is not None:
                        itemsData = piece.__dict__[f"conn{intConnex}Link"] 
                        component = f"DN{itemsData.dn} PN{itemsData.pn}"
                        components.append(component)
        return "-".join(components)
    

    listComptage,offset=[],0
    for indicBifurc,montageBifurc in enumerate(sharedVar.suiteMontageActuel):
        if indicBifurc>0:
            offset=1
        for piece in montageBifurc[offset:]:
            designation=set_denominationPiece(piece)
            piece.designation=designation
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
                    listComptage.append({"DESIGNATION":designation,"NAME":piece.name,"DN":piece.dn,"PN":piece.pn,"QUANTITE":1,"PRIX": piece.tarif,"PIECES":[piece]})
            else:
                listComptage.append({"DESIGNATION":designation,"NAME":piece.name,"DN":piece.dn,"PN":piece.pn,"QUANTITE":1,"PRIX": piece.tarif,"PIECES":[piece]})
    return listComptage



def comptLiaison(sharedVar):

    for montageBifurc in sharedVar.suiteMontageActuel:
        for i in range(len(montageBifurc)-1):
            pieceRef = montageBifurc[i]
            pieceNext=montageBifurc[i+1]
            LIAISON(pieceRef,pieceNext,sharedVar)

                