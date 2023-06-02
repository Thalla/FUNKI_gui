# Current Version of Python Analysis Class

Concept: A project with a *main* file (see for example [MBEN/v00/.../src/MBEN_Python/](https://github.com/saezlab/MBEN/tree/main/v00/src/MBEN_Python)) that uses the functions and classes from this folder to initialise an analysis object that holds information about datasets, analysis parameters, methods and paths with supporting functions.   

*sc_analysis_baseclass.py:* Holds the analysis class and the basic dataset class.  
*sc_analysis_loops.py:* Wraps the functions into loops that go over all parameter combinations.  
*sc_decoupler_utility.py:* Decoupler class that a dataset can inherit from to receive additional methods, paths and properties for a smooth analysis with decoupler.  
*scfunctions.py:* Any useful function that doesn't make sense in a class context.  
*decoupler_v2_outsourcedStuff.ipynb:* Other code...should be cleaned and added somewhere more specific. 

## How To Get Started

- Create the following: *projects/<projectShortcut>/v00/analysis_params.py*
- Fill in *analysis_params.py*

## Open ToDos: 
- Generate subsets not in local proj folder but in mounted folder next to the rest. ID of a dataset is actually seqType + host + datasetname. 
- Clean pseudobulk analysis
- Data folders that can describe Seurat and AnnData objects in more detail (counts_data_scale.data; scale.data_log (for X and raw)). Is scale.data always only highly variable genes? Normalize names to counts, log, hvgs ? What other assay types are there? What are the intra assay differences? What's the best way of storing and reading the data to be able to use any combination of two assays in the Anndata object? Or could just everyting be a layer and the methods only work with the layers? Similar to the Pseudobulk analysis. Can decoupler use a layer instead of raw or not raw? Otherwise just set raw to a specific layer. 
- decoupler results are under 'scaled' but should be under 'log'. (better 'logcounts' to not get confused with logging)
- Must decoupler use log transformed data or can it be scale.data that has only hvgs?
- Method for generating collaborator friendly copy of data (no h5ad files, analysis_params files, ...) taht is automatically saved in 'sent' folder with the date and a description
- Clean up paths and smoothen interaction with R (create analysis object for R as well?)


## Analysis Params  
  
Analysis params are set in the file analysis_params.py in the format of a python dictionary.
Every dataset must have an entry in 'other'. This way, R knows the dataset names. (The names can't be read from the folder as priorKnowledge is placed at the same layer as the datasets. TODO: In the analysis init step, add a key + list with all dataset names to the dict. Or add an empty key for every dataset that isn't already in the dict under 'other')
When the analysis obj gets initialized:   
  
- The analysis_params from the file are set as property of the analysis.   
- Paths are generated from the basepaths information in analysis_params and then set as 'paths' property of the analysis.   
- Paths and analysis_params are forwarded to the constructor of the datasets. Each dataset holds an extended copy of these properties.   
- A combination of analysis_params and paths is saved as yaml file for each dataset. Therefore, 'paths' gets added as key to the dictionary.  
 
  
Description of the dictionary:   

- Subsets:   
  - key: 'subs'   
    - key: name of obs/metadata column  
      - value: ['prefixOfSubsetName', (val1, val2), (val3,)] -> a subset is created for each tuple by selecting only matching data. It is named by prefixOfSubsetName + the concatenated list of column values used for creating it. 
  - A subset is set as the 'subs' property of a dataset. A subset is a dataset itself and can have subsets.   

## Glossary:   
  
- analysis: an object with paths & parameter information holding one or multiple datasets
- dataset: an object with paths & parameter information holding zero, one or multiple related datasets (subsets or method results)  
- hvg: highly variable genes

## Shortcuts:   

Most of the time, Plural = Shortcut + 's'  
  
- col: column  
- val, v: value  
- k: key  
- ind, i: index (used in loops)
- elem, e: element (used in loops)
- meta: metadata (obs)  
- ds: dataset ('Dataset' object)
- param: parameter  
- subs (Pl. subsets): subset  
- cond: condition (for comparisons)  
- relAb: relative abundance


## Usage Example


```dc_dataset = sc_classes.Analysis.new_dataset(sc_classes.Baseanalysis, dcu.Decoupler)  
analysis = sc_classes.Analysis(proj='MBEN', datasets=[  
                                ('all_t', 'sn', 'human', dc_dataset),  
                                ('all', 'sn', 'human', dc_dataset)], version = '00')  
scl.analysis = analysis  
scl.get_acts()  
scl.plot_umap() # these are umaps for acts  
scl.get_mean_acts()  
scl.plot_mean_acts() 
``` 
### Adding subsets

To add subsets you need to load all datasets that shall get subsets. In this example we want to generate the subsets for all_t and all_t_clust43. 

```
analysis = sc_classes.Analysis(proj='MBEN', datasets=[
            ('all_t', 'sn', 'human', dc_dataset), 
            ('all_t_clust43', 'sn', 'human', dc_dataset), 
          ], version = 'v01')
```

The analysis params entry for all_t_clust43 looks for example like this: 

```
        'all_t_clust43': {
            'subs':{
                'PID':['subj', ('AK1',), ('AK2',), ('AK3',), ('MB263',), ('MB266',), ('MB287',), ('MB295',), ('MB299',), ('MB88',)]
             }
        }
``` 

After generating the `analysis` object you can run the subset command: 

```
scl.get_subsets(dc_dataset)
```

The subsets are added in the proj folder. To use them you have to move them to the mounted folder next to the datasets that they come from. 
To initialize the new subsets with params and paths, you have to add them to the analysis object: 

```
analysis = sc_classes.Analysis(proj='MBEN', datasets=[
            ('all_t', 'sn', 'human', dc_dataset), 
            ('all_t_clust43', 'sn', 'human', dc_dataset), 
            ('all_t_subjAK1', 'sn', 'human', dc_dataset),
            ...
          ], version = 'v01'),        
```

Then save their params and paths: 

```
save_paths(analysis)
``` 

For using the subsets in R use the get_subsets function. The base datasets are subsetted according to the analysis_params and saved in the data correct data folder. Afterwards you can read them in as usual.


### Loops

When running get_mean_acts() the following function from sc_analysis_loops is executed.  
sc_analysis_loops is kind of an interface between main program and class methods that is used to run the methods over all parameter combinations as they are defined in analysis_params.py .

```@loop('analysis.datasets')
def get_mean_acts(dataset):
    @loop([dataset.analysis_params['decoupler']['meanacts']['minstd']])
    @loop(dataset.acts)
    def get_peract_perminstd(acts, minstd):
        @loop(acts.data.obs)
        def get_pergroupby(groupby):
            acts.get_mean_acts(minstd, groupby)
        get_pergroupby()
    get_peract_perminstd()```


## Snakemake

The workflow is as follows:   
- Create all paths, data to read in and a config file for the analysis. The config file is tool specific. It holds the parameters and paths for input and output files. Each parameter combination is a row in a table. The table is used as input for snakemake in a way that the rows are processed in parallel. 
- Create the fitting snakemake folder structure and Snakefile.
- Make sure that the script or notebook that is run by a rule can take the config table as input. 


## R
Naming convention: snake_case, because this is a standard for python

Everything is based on the analysis_params.yaml file of the project. 

## Useful 

Conversion: 
- SeuratDisk: Seurat to AnnData
  - if scale.data exists: data to raw & scale.data to X 
  - else: counts to raw & data to X
  
scale.data holds only highly variable genes?









