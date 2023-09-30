##################################
### UTILISATION DE PYINSTALLER ###
##################################
Lignes de commande pour pouvoir passer du .py au .executable (dépendant du OS)

	pyinstaller --name sade_Calpinage --onefile --icon=sade.ico --windowed \
--add-data 'data':'data' \
--add-data 'gui':'gui' \
--add-data 'gui/menu':'gui/menu' \
--add-data 'modules':'modules' \
--add-data 'tests':'tests' \
--add-data 'utils':'utils' \
main.py


#############################
### UTILISATION DE DOCKER ###
#############################
Pour créer un exécutable indépendamment de l'OS de la machine (non fonctionnel encore)

	docker run -v "$(pwd):/src/" cdrx/pyinstaller-windows "pyinstaller --name sade_Calpinage --onefile --icon=sade.ico --windowed --add-data 'data':'data' --add-data 'gui':'gui' --add-data 'gui/menu':'gui/menu' --add-data 'modules':'modules' --add-data 'tests':'tests' --add-data 'utils':'utils' main.py"



