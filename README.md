# calpinage_SADE
Création d'un logiciel facilitant le calpinage des pièces lors de la création d'un devis ayant pour objectif finale de répondre à une offre de marché

## Comment utiliser le logiciel
Le logiciel a été développé sur MACOS et compiler sur MACOS, malheureusement je ne parvient pas a creer des executables sur différentes machines. 
\Je vous donne donc la marche à suivre.

### Utilisateur MACOS
Télécharger le dossier >> Rendez-vous dans le dossier "Software_Calpinage" >> Rendez-vous dans "dist" >> Trouvez l'executable avec le logo.

### Utilisateur WINDOWS / LINUX 
Télécharger le dossier >> Rendez-vous dans le dossier "Software_Calpinage" >> Ouvrez un terminal pour ce dossier >>

Sur ce terminal rentrez ces instructions: 
  pip install -U pyinstaller \
  pyinstaller --name sade_Calpinage --onefile --icon=sade.ico --windowed \
  --add-data 'data':'data' \
  --add-data 'gui':'gui' \
  --add-data 'gui/menu':'gui/menu' \
  --add-data 'modules':'modules' \
  --add-data 'tests':'tests' \
  --add-data 'utils':'utils' \
  main.py

L'éxecution de ces commandes prendra quelques instants.

Ensuite rendez-vous dans le dossier "Software_Calpinage" >> Rendez-vous dans "dist" >> Trouvez l'executable avec le logo.
  



