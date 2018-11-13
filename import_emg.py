import pandas as pd

def import_MVC(file):
    if 'MVC' in file:
        emg_MVC = pd.read_excel(file)
        print('SUCCESSFULLY IMPORTED MVC FILE.')
        return emg_MVC
    else:
        print('ERROR: This file does not contain the subject\'s MVC.')

def import_dynamic(file):
    if 'Trimmed' in file:
        emg_dynamic = pd.read_excel(file)
        print('SUCCESSFULLY IMPORTED DYNAMIC FILE.')
        return emg_dynamic
    else:
        print('ERROR: This file is not a dynamic trial.')


#import_MVC('LX1511MVCRQuad01.xlsx')

#import_dynamic('Trimmed_LX1511eT08R1.xlsx')