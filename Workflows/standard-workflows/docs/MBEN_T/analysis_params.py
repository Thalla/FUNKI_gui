analysis_params = {
            'proj_details': {
                'proj_id': 'MBEN_T',
                'version': 'v00'
            },
            'default': {
                'basepaths':{
                    # path from which all needed files can be reached
                    'basepath_local': './', 
                    'basepath_bioq': '',
                    'basepath_binac': '',
                    'storagedir': '',
                    'localdir': ''
                }
            }, 
            'other': {
            }  
        }


import os, yaml
ap_file = open(os.path.join(analysis_params['default']['basepaths']['basepath_local'], 'analysis_params.yaml'), 'w+')
yaml.dump(analysis_params, ap_file)
