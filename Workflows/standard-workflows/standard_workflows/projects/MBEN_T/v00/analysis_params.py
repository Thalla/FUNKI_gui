""" Analysis Parameters 
Definition of default parameters and dataset specific parameters in a python dictionary that is saved as yaml file. 
This is a non redundant representation of all analysis paths. 

"""
import yaml
from os import path
# Caution: Do not split paths and analysis_params on the level of Analysis Obj. 
# Splitting leads to problems with merging and replacing. 
# 1. Execute additions and replacements
# 2. merge_dicts: proj_params are merged with the params of a specific dataset (dataset_params/organism/seq_type/datasetname)
# 3. Extend dataset specific paths

# Implement use_pickle_data
analysis_params = {
    'proj_params': { 
        'proj_id': path.basename(path.normpath(path.abspath("../"))),    # always the folder above, should be 2 to 8 capital letters or underscores
        'version': path.basename(path.normpath(path.abspath("./"))), 
        'paths': {
            'analysis_path': path.abspath('../../'),   # path to 'projects' folder or the folder where the proj results shall be saved
            'data_root_path': path.abspath('../../../example_data/<default>')   # for example path to SDS mounted location: .../mounted/projects/
        },
        'use_pickle_data': True,    # h5ad files are read and then saved as pickle, the pickle files are used from there on
        'priorKnowledge':{
            'dorothea':{   # levels
                'levels': [('A', 'B', 'C')]
            } 
        }
    },
    'dataset_params': {
        'human': {
            'sn': {
                'priorKnowledge':{
                    #'progeny': 
                        #{   # topvalues
                        #    'topvalues':['100', '50']
                        #},
                    'dorothea': 
                        {   # levels
                            'levels': [('D', 'ADD')]
                        }  
                },
                'all_cnvsNormal':{

                }
            },
        'REPLACEMENTS': {
                'use_pickle_data': False
            },
            'atac':{
                'all_cnvsNormal_2':{
                    'paths':{
                        'data_root_path': path.abspath('../../') # same as analysis_path
                    },
                    'use_pickle_data': True
                },
                'REPLACEMENTS': {
                    'paths': {
                      'data_root_path': path.abspath('../../../example_data/')
                    }
                },
                'all_cnvsNormal':{
                    'paths':{
                        'data_root_filename': 'all_cnvsNormal_atac.h5ad' 
                    },
                    'use_pickle_data': True
                }
            }
        }
    }  
}

def init():
    with open('./analysis_params.yaml', 'w+') as file: 
        yaml.dump(analysis_params, file, sort_keys=False)

if __name__ == '__main__':
    init()


# def update(analysis):
#     """ Updates analysis_params values of the analysis obj according to the values above saves a copy of them as a yaml file. """

#     with open(path.join(analysis_params['default']['basepaths']["basepath_local"], 'projects', analysis.proj, 'analysis_params.yaml'), 'w+') as file:
#         yaml.dump(analysis_params, file)

#     """ with open(self.paths['analysis_params'], 'r') as stream:
#             try:
#                 analysis_params=yaml.safe_load(stream)
#                 print(analysis_params)
#             except yaml.YAMLError as exc:
#                 print(exc)   """
#     from copy import deepcopy
#     return deepcopy()