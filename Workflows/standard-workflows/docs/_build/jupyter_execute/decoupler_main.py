#!/usr/bin/env python
# coding: utf-8

# # MBEN & Decoupler
# Decoupler is an ensemble of methods to infer biological activity. 
# 
# Used prior knowledge: 
# - Dorothea for transcription factor analysis
# - Progeny for pathway analysis
# 
# 
# 
#   
# 

# ## Init Script

# In[1]:


import sys
from standard_workflows import *
import os
from copy import deepcopy
from pathlib import Path
from IPython.display import display, Markdown, Latex # to display Markdown in code chunk
import sys, logging, logging.config, random, re, json, yaml
import scanpy as sc, numpy as np, matplotlib.pyplot as plt, seaborn as sns, matplotlib as mpl, pandas as pd


# turn off warnings
import warnings

warnings.filterwarnings("ignore")


# In[2]:


def print_info(analysis):
    """ Prints basic informatin about the analysis. """
    display(Markdown('**Analysis Parameters**  '))
    print(json.dumps(analysis.analysis_params['default']['decoupler'], indent=4, sort_keys=True, default=str))
    display(Markdown('**Paths**  '))
    print(json.dumps(analysis.get_paths(), indent=4, sort_keys=True, default=str))


# ## Init Analysis

# In[3]:


# Create Dataset class. It inherits from other classes dynamically.
dc_dataset = sc_classes.Analysis.new_dataset(sc_classes.Baseanalysis, dcu.Decoupler) 
dc_dataset = sc_classes.Analysis.new_dataset(sc_classes.Baseanalysis)
# CAUTION: decoupler use_raw = True


# In[7]:


# Init Analysis object
"""
            ('all_cnvsNormal', 'sn', 'human', dc_dataset)        
"""

analysis = sc_classes.Analysis(proj='MBEN_T', datasets=[
            ('all_cnvsNormal', 'sn', 'human', dc_dataset)
            ], version = 'v01', proj_path= os.path.abspath('./'))
#print_info(analysis)
scl.analysis = analysis


# In[30]:


# Missing Features: relAb/norm & loop over all obs of interest
# scl.plot_meta_barplots('seurat_clusters', None)

k = a.data.obsm_keys()
k


# In[6]:


a = analysis.datasets[1]
a._paths
a.analysis_params


# In[7]:


#import decoupler as d

#d.decouple(analysis.datasets[2].data, model, methods=['mlm'])

#d.decouple(analysis.datasets[0].data, model, methods=['mlm'], consensus = False, use_raw = True)
#analysis.datasets[0].data.obsm['mlm_pvals'].loc[:, ['GLI1']]


# In[8]:


#d.decouple(analysis.datasets[0].data, model, methods=['mlm'], consensus = False, use_raw = False)
#analysis.datasets[0].data.obsm['mlm_pvals'].loc[:, ['GLI1']]


# In[9]:


#d.decouple(analysis.datasets[0].data, model, methods=['mlm'], consensus = False, use_raw = False, min_n=2)
#analysis.datasets[0].data.obsm['mlm_pvals'].loc[:, ['GLI1']]


# In[10]:


#ds = analysis.datasets[0]
#act = ds.acts[1]
#act = act.data.obsm['dorotheaabc_mlm_pvals']
#act
#act.loc[:, ['GLI3']]


# In[11]:


#'GLI1' in list(model.source)
#model.loc[model['source'] == 'GLI1']


# # Get_subsets

# In[12]:


#scl.get_subsets(dc_dataset)


# # Save Paths

# In[13]:


def save_paths(self):
    """ Saves analysis params together with paths to yaml file. """
    self.analysis_params['default']['paths'] = self.get_paths()
    with open(self.get_paths()['analysispath_local'] / 'analysis_params_paths.yaml', 'w+') as file:
        yaml.dump(self.analysis_params, file)
    for data in self.datasets:
        data.analysis_params['paths'] = data._paths
        print(data._paths)
        with open(data._paths['analysispath_local'] / data._paths['datasetpath'] / 'analysis_params.yaml', 'w+') as file:
            yaml.dump(data.analysis_params, file)



# In[14]:


save_paths(analysis)


# In[52]:


#import decoupler as d
#model = d.get_dorothea(levels = ['A', 'B', 'C'])
m = model.loc[model['source'] == 'GLI2']
print(m)

data = analysis.datasets[0].data

print(data.var_names)

print("BCL2" in data.var_names)
print("CCND1" in data.var_names)
print("COL5A2" in data.var_names)
print("EFEMP1" in data.var_names)
print("FAS" in data.var_names)
print("FGF13" in data.var_names)
print("FOXA2" in data.var_names)
print("FOXE1" in data.var_names)
print("IFNGR1" in data.var_names)
print("LUM" in data.var_names)



# In[51]:


print(data.raw.var_names)

print("BCL2" in data.raw.var_names)
print("CCND1" in data.raw.var_names)
print("COL5A2" in data.raw.var_names)
print("EFEMP1" in data.raw.var_names)
print("FAS" in data.raw.var_names)
print("FGF13" in data.raw.var_names)
print("FOXA2" in data.raw.var_names)
print("FOXE1" in data.raw.var_names)
print("IFNGR1" in data.raw.var_names)
print("LUM" in data.raw.var_names)


# ## Decoupler  
# ### Activity estimates  
# For each dataset the activities are estimated according to the given prior knowledge and decoupler parameters. 

# In[29]:


#%%asmarkdown
scl.get_acts()



#import decoupler as d
#d.run_consensus(analysis.datasets[1].data)
#data = analysis.datasets[0]
#a = data.acts[2]
#c = d.decouple(analysis.datasets[0].data, d.get_dorothea())


# In[30]:


scl.plot_umap()


# ### Mean Activities
# For each calculated activity the mean activity values are calculated. 

# In[31]:


#%%asmarkdown
scl.get_mean_acts()


# In[32]:


#%%asmarkdown
scl.plot_mean_acts()


# In[15]:


import os
import shutil

dir_name = "/Users/hanna/Documents/projects/MBEN/v01/sent/v01_sent220901/"

def delete_files(dir_name):
    all_subdir_names = ''
    if os.path.isdir(dir_name):
        all_subdir_names = os.listdir(dir_name)
        print(all_subdir_names)
        if len(all_subdir_names) >= 1:
            for elem in all_subdir_names:
                match = re.match("^.*(h5ad|DS_Store|pickle|priorKnowledge|data|analysis_params.yaml)", elem)
                if match != None:
                    if os.path.isdir(os.path.join(dir_name, elem)) : 
                        shutil.rmtree(os.path.join(dir_name, elem))  
                        print('this gets deleted: ', elem)
                    else: 
                        os.remove(os.path.join(dir_name, elem))
                         
                        print('this gets deleted: ', elem)
                else :
                    print('new iteration with: ', os.path.join(dir_name, elem))
                    print(delete_files(os.path.join(dir_name, elem)))

delete_files(dir_name)


# In[33]:


dir_name = "/Users/hanna/Documents/projects/MBEN/v01_copy/human/sn.h5ad/.DS_Store"
print(re.match("^.*[.h5ad|.DS_Store]", dir_name)[0])


# In[ ]:




