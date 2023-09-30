import os
import pandas as pd
from tests import nameOfFunctionCalled as tst

@tst.show_function_name
def read_database(nameDataBase,sheet_name=None)->pd:
    data_dir = os.path.dirname(__file__)
    database_file = os.path.join(data_dir, nameDataBase)
    if sheet_name is not None:
        # Si aucun nom de feuille n'est spécifié, on lit la première feuille
        return pd.read_excel(database_file, sheet_name=sheet_name)
    else:
        all_docs=pd.read_excel(database_file, sheet_name=None)
        return{sheet: data for sheet, data in all_docs.items()}
    
