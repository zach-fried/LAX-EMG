import pandas as pd

# Refactor to only have one import_emg function
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

# Takes in MVC files and dynamic trial file and parses data into
# a dictionary. Keys are equal to the muscle name and values are
# equal to the raw EMG data.
def parse_emg(emg_MVC_RQuad, emg_MVC_RHam, emg_MVC_LQuad, 
emg_MVC_LHam, emg_dynamic):

    muscles_key = {'RVM': 19, 'RRec': 20, 'RVL': 21, 'RSemi': 22, 
    'RBic': 23, 'LVM': 24, 'LRec': 25, 'LVL': 26, 'LSemi': 27, 
    'LBic': 28}

    emg_MVC_dict = dict()
    emg_dynamic_dict = dict()

    time_dynamic = emg_dynamic['File_Type:'][10:]
    time = len(time_dynamic)

    for k, v in muscles_key.items():
        #print(k)
        if any(['RVM' in k, 'RRec' in k, 'RVL' in k]):
            #print('R QUAD MVC FILE')
            emg_MVC_dict[k] = emg_MVC_RQuad[f'Unnamed: {v}'][10:(time + 10)]
        elif any(['RSemi' in k, 'RBic' in k]):
            #print('R HAM MVC FILE')
            emg_MVC_dict[k] = emg_MVC_RHam[f'Unnamed: {v}'][10:(time + 10)]
        elif any(['LVM' in k, 'LRec' in k, 'LVL' in k]):
            #print('L QUAD MVC FILE')
            emg_MVC_dict[k] = emg_MVC_LQuad[f'Unnamed: {v}'][10:(time + 10)]
        else:
            #print('L HAM MVC FILE')
            emg_MVC_dict[k] = emg_MVC_LHam[f'Unnamed: {v}'][10:(time + 10)]

        emg_dynamic_dict[k] = emg_dynamic[f'Unnamed: {v}'][10:]
    
    return emg_MVC_dict, emg_dynamic_dict, time_dynamic

"""
TESTING

emg_MVC_RQuad = import_MVC('LX1511MVCRQuad01.xlsx')
emg_MVC_RHam = import_MVC('LX1511MVCRHam01.xlsx')
emg_MVC_LQuad = import_MVC('LX1511MVCLQuad01.xlsx')
emg_MVC_LHam = import_MVC('LX1511MVCLHam01.xlsx')
emg_dynamic = import_dynamic('Trimmed_LX1511eT08R1.xlsx')

emg_MVC_dict, emg_dynamic_dict, time = parse_emg(emg_MVC_RQuad, emg_MVC_RHam, emg_MVC_LQuad, emg_MVC_LHam, emg_dynamic)
"""

    
    

    