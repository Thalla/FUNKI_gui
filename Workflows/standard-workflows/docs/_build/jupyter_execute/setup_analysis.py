#!/usr/bin/env python
# coding: utf-8

# # Fileinput Exploration with Pandas and Plotly
# 
# In Panel the FileDownload widget allows downloading a file generated on the server the app is running on while the `FileInput` widget allows uploading a file. In this example we demonstrate a pipeline of two little apps one which allows generating a sample data CSV file and one which allows uploading this file and displays it as a Plotly plot. 
# 
# For more details on how to use these components see  [`FileInput`](../../reference/widgets/FileInput.ipynb) and [`FileDownload`](../../reference/widgets/FileDownload.ipynb) reference guides.

# In[1]:


import io
import param
import panel as pn
import pandas as pd
import random
import json
from standard_workflows import analysis_params as ap

from datetime import datetime, timedelta

import plotly.express as px

pn.extension('plotly', 'tabulator', sizing_mode="stretch_width")
pn.extension('ace', 'jsoneditor')


# Lets start out by creating some sample data by defining some parameters which declare bounds on the values to generate along with a [`FileDownload`](../../reference/widgets/FileDownload.ipynb) widget which will allow the user to download the data onto their machine.

# In[2]:


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    

print(f"{colors.WARNING}Warning: No active frommets remain. Continue?{colors.ENDC}")

# not working
from termcolor import colored
print(colored('hello', 'red'))


# In[ ]:





# class AnalysisInit(param.Parameterized):
#     # Basic paramters to set
#     projName  = pn.widgets.TextInput(name = 'Full Project Name', placeholder = 'aNameWithoutSpaces')
#     projID    = pn.widgets.TextInput(name = 'Project ID ', placeholder = 'two to six capital letters')
#     version   = pn.widgets.TextInput(name = 'Analysis Version', placeholder = 'v01')
#     host      = pn.widgets.Select(name = 'Host', default="human", options=['human', 'mouse'])
#     datasetname = pn.widgets.TextInput(name = "Dataset Name", placeholder = 'all_tumor_liver_pid12pid14')
#     seqType   = pn.widgets.Select(name = 'Sequencing Type', default = 'sc', options=['sc', 'sn', 'atac', 'bulk'])
#     local_folder_path = pn.widgets.TextInput(name = 'Results Folder Path', placeholder = 'path to where to save the results folder')
#     # Put elements into grid
#     proj_parameters  = pn.GridBox(projName, projID, version, host, datasetname, seqType, local_folder_path, ncols = 2)
#     # Param Editor
#     param_editor = pn.widgets.JSONEditor(value= ap.analysis_params, width=400, height=800)
#     # File Handling
#     add_data = pn.widgets.FileInput()
#     upload_params = pn.widgets.FileInput()
#     
#     data = ''
# 
#    #setup_analysis = param.Action(lambda self: save_params(), label="Run Analysis Setup", doc="""
#    #  An action callback which will initialize the analysis obj.""")
#     def do_save_params(self):
#       """
#       A FileDownload callback will return a file-like object which can be serialized
#       and sent to the client.
#       """
#       import yaml
#       ff = open(os.path.join(local_folder_path.value, projID.value, version.value, host,value, seqType.value, datasetname.value, 'data', 'data.h5ad'), 'w+')
#       yaml.dump(json_editor.value, ff)
#       #self.download.filename = file_name
#       #sio = io.StringIO()
#       #sample_df.to_csv(sio, index=False)
#       #sio.seek(0)
#       #return sio
# 
#       save_params = pn.widgets.FileDownload(name = 'Save Parameters', filename = 'analysis_params.yaml', callback = do_save_params, button_type = 'primary')
# 
#     def __init__(self, **params):
#       super().__init__(**params)
#       
#      # table = pn.widgets.Tabulator(
#      #     pd.DataFrame(self.analysis_params), layout='fit_data_stretch', theme='site', height=360
#       #)
# 
#     def _add_data():
#       if add_data.value is not None:
#         import scanpy
#         self.data = scanpy.read_h5ad(add_data.value)
#         ff = open(os.path.join(local_folder_path, projName.value, self.download.file_name), 'w+')
#         yaml.dump(self.data, ff)
#         
# 
#    
#       
# analysis_init = AnalysisInit()
# pn.Column(pn.Row(analysis_init, analysis_init.param_editor), pn.Row(analysis_init.proj_parameters))
# 

# pn.widgets.TextInput(name = 'Full Project Name', placeholder = 'aNameWithoutSpaces')  
# pn.widgets.Select(name = 'Sequencing Type', default = 'sc', options=['sc', 'sn', 'atac', 'bulk'])  
# pn.GridBox(projName, projID, version, host, datasetname, ncols = 2)  
# pn.widgets.JSONEditor(value= ap.analysis_params, width=400, height=800)  
# pn.widgets.Tabulator(pd.DataFrame(self.analysis_params), layout='fit_data_stretch', theme='site', height=360)  
#   
# add_data = pn.widgets.Button(name='Click me', button_type='primary')  
# add_data.on_click(_add_data) 
#      
# *param Action Button*  
# action = param.Action(lambda x: x.param.trigger('action'), label='Click here!')  
# number = param.Integer(default=0)   
# @param.depends('action')  
# def get_number(self): 
#     self.number += 1  
#     return self.number  
#   
# """  
# A FileDownload callback will return a file-like object which can be serialized
# and sent to the client.  
# """
# self.download.filename = self.file_name  
# sio = io.StringIO()  
# self.sample_df.to_csv(sio, index=False)  
# sio.seek(0)  
# return sio  

# In[61]:


import scanpy
d = scanpy.read_h5ad('Users/hanna/Documents/projects/MBEN/all_cnvsNormal/data/all_cnvsNormal.h5ad')


# In[74]:


class Test(param.Parameterized):
    add_data = param.Action(lambda x: x.param.trigger('add_data'), label='Click here!')  
    number = param.Integer(default=0)   
    data = ''
    @param.depends('add_data')  
    def _add_data(self): 
        self.number += 1  
        self.data = "miau"
        import scanpy
        self.data = scanpy.read_h5ad('/Users/hanna/Documents/projects/MBEN/all_cnvsNormal/data/all_cnvsNormal.h5ad')
        from pathlib import Path
        Path('/Users/hanna/Documents/projects/Workflows/standard-workflows/MBEN_T/v00/human/sc/test/data').mkdir(parents=True, exist_ok=True)
        #ff = open('/Users/hanna/Documents/projects/Workflows/standard-workflows/MBEN_T/v00/human/sc/test/data/all_cnvsNormal.h5ad', 'w+')
        import anndata
        self.data.write_h5ad('/Users/hanna/Documents/projects/Workflows/standard-workflows/MBEN_T/v00/human/sc/test/data/all_cnvsNormal.h5ad')
        return self.number  
test = Test()
pn.Column(
    pn.Row(
        pn.Column(pn.panel(test, show_name=False, margin=0, widgets={"add_data": {"button_type": "primary"}, "number": {"disabled": True}}),
            '**Click the button** to trigger an update in the output.'),
        pn.panel(test._add_data, width=300), max_width=600)
)


# In[467]:


css = '''
.bk.panel-widget-box {
  #background: #fefefe;
  border-radius: 5px;
  border: 1px black solid;
  font-weight: 700;
}
.custom{
    background-color: #ffc107;
    color: aliceblue;
}

h2{
    backgound-color: pink;
}

'''

pn.extension(raw_css=[css])


# In[275]:


txt = pn.widgets.TextInput(name = "huhui",  placeholder = "huhu")
widget1 = pn.widgets.Button(name = "mybutton")
data = 'huhu'

def my_func(e):
   widget1.name = "miau"
   txt.value = "muhhh"
   data="huihuihui"
   print(data)


widget1.on_click(my_func)  
ui = pn.panel(pn.Column(widget1, txt))
ui


# # Comments
# Param:  
# - Param wants to be used in classes?
#   - param.Action button doesn't allow to add parameters like self etc.?
# - Using the things in a class somehow doesn't work. And the error message aren't presented.
# 
# Widgets:  
# - FileInput: Is the filepath saved or only the filename? How do I read a yaml file from io.StringIO??
# - Button: add on_click event, the attached method must have an event parameter
# 

# In[ ]:


import anndata


pn.extension(template='fast')

data = anndata.AnnData()

# Basic paramters to set
projName    = pn.widgets.TextInput(name = 'Full Project Name', placeholder = 'aNameWithoutSpaces')
projID      = pn.widgets.TextInput(name = 'Project ID ', placeholder = 'two to six capital letters')
version     = pn.widgets.TextInput(name = 'Analysis Version', placeholder = 'v01')
host        = pn.widgets.Select(name = 'Host',  options=['human', 'mouse'])
datasetname = pn.widgets.TextInput(name = 'Dataset Name', placeholder = 'all_tumor_liver_pid12pid14')
seqType     = pn.widgets.Select(name = 'Sequencing Type',  options=['sc', 'sn', 'atac', 'bulk'])
param_editor        = pn.widgets.JSONEditor(value= ap.analysis_params, width=400, height=800)
results_folder_path = pn.widgets.TextInput(name = 'Results Folder Path', placeholder = 'path to where to save the results folder')
dataset_source      = pn.widgets.TextInput(name = 'Data Filepath')

def _download_params(e):
  import yaml
  paths = set_paths()
  ff = open(paths['analysis_params'], 'w+')
  yaml.dump(param_editor.value, ff)

# Buttons
upload_params = pn.widgets.Button(name = 'Upload Parameter File')
download_params = pn.widgets.Button(name='Download Data', button_type='primary')
add_data = pn.widgets.Button(name='Upload Data', button_type='primary')
buttons = pn.Column( 'Upload Parameters', upload_params, download_params, width=300)


def _upload_params(e):
  import yaml
  from yaml.loader import BaseLoader
  paths = set_paths()
  with open(paths['analysis_params']) as stream:
#    try:
      param_editor.value = yaml.load(stream, Loader=BaseLoader)
 #   except yaml.YAMLError as exc:
 #     alert_text = ("Please add data first as the project structure with the default analysis_params.yaml file will be generated automatically then.")
 #     pn.Column(pn.pane.Alert(alert_text.format(alert_type='warning'), alert_type='warning'),sizing_mode='stretch_width')

def _add_data(e):
  paths = set_paths()
  import scanpy
  data = scanpy.read_h5ad(paths['dataset_source'])
  from pathlib import Path
  Path(paths['dataset_folder']).mkdir(parents=True, exist_ok=True)
  data.write_h5ad(paths['dataset_file'])


add_data.on_click(_add_data)
download_params.on_click(_download_params)
upload_params.on_click(_upload_params)

ui = pn.Row(pn.Column('## Basic Project Definition', projName, projID, version, host, datasetname, seqType, pn.layout.Divider(), 
                      '## Upload Dataset', dataset_source, results_folder_path, add_data, pn.layout.Divider(), 
                      '## Up- & Download Parameters', buttons), pn.Spacer(width=100), pn.Column(
                      '## Adjust Parameters', "If no paramter file is uploaded, default paramters are shown. If you are finished with adjusting them, don't forget to push the download button.", 
                      param_editor, max_width = 400), css_classes=['panel-widget-box']).servable(area='main')

def set_paths() -> dict:
  """ Defines basic file & folder paths for receiving and storing data. These paths are needed to initialize the analysis. """
  paths = {
    'dataset_source' : dataset_source.value,
    'dataset_folder' : os.path.join(results_folder_path.value, projID.value, version.value, host.value, seqType.value, datasetname.value, 'data')
  }
  pahts = paths.update({
    'dataset_file': os.path.join(paths['dataset_folder'], 'data.h5ad'),
    'analysis_params': os.path.join(results_folder_path.value, projID.value, 'analysis_params.yaml')
  })
  return paths

  # initialize with default values for testing purposes
projName.value, projID.value, version.value, datasetname.value, dataset_source.value, results_folder_path.value = ['MBEN_Test', 'MBEN_T', 'v00', 'test', '/Users/hanna/Documents/projects/MBEN/all_cnvsNormal/data/all_cnvsNormal.h5ad', '/Users/hanna/Documents/projects/Workflows/standard-workflows/docs/']
  ## Define paths


#pn.serve(pn.Column(pn.pane.Markdown('# Funki').servable(area='sidebar'), ui.servable(area='main')))
template = pn.template.FastListTemplate(
    title="Fast Panel App",
    logo="https://panel.holoviz.org/_static/logo_stacked.png"
)

m = pn.pane.Markdown('# Funki').servable(area='sidebar')
template.servable()
pn.serve(template, m)




# In[468]:


import panel as pn
from panel.template import DarkTheme, DefaultTheme

#css_files = ['./style.css']
#pn.extension(css_files=css_files)
template = pn.template.FastGridTemplate(title='FUNKI', sidebar_footer="hello I'm the footer", theme=DefaultTheme, accent='black')#"#A01346")
template = pn.template.MaterialTemplate(title='FUNKI', sidebar_footer="hello I'm the footer", theme=DefaultTheme, accent='black')#"#A01346")
template = pn.template.BootstrapTemplate(title='FUNKI', sidebar_footer="hello I'm the footer", theme=DefaultTheme, accent='black')#"#A01346")
template = pn.template.VanillaTemplate(title='FUNKI', sidebar_footer="hello I'm the footer", theme=DefaultTheme, accent='black')#"#A01346")
template = pn.template.FastGridTemplate(title='FUNKI', sidebar_footer="hello I'm the footer", theme=DefaultTheme, accent='black')#"#A01346")
template = pn.template.GoldenTemplate(title='FUNKI', sidebar_footer="hello I'm the footer", theme=DefaultTheme, header_background ='black')#"#A01346")






#template = pn.Template(tmpl)

pn.config.sizing_mode = 'stretch_width'



#dashboard side
template.sidebar.append(pn.pane.Markdown("## Settings"))
template.sidebar.append(m)
template.sidebar.append(m)
#dashboard focal
#template.main[:3, :6] = ui
template.main.append(pn.Row(
        pn.Card(ui)))
template.main.append(pn.Row(
        pn.Card(ui)))
tabs = pn.Tabs(('Scatter', m), ui)

template.main.append(pn.Row(
        pn.Card(tabs)))

template.show();


# In[457]:


pn.extension(..., template="fast")
pn.state.template.param.update(site="Panel", title="FastListTemplate")
m = pn.pane.Markdown("## Settings").servable(target="sidebar")
pn.serve(m)


# In[373]:


import yaml
from yaml.loader import BaseLoader
with open('/Users/hanna/Documents/projects/Workflows/standard-workflows/docs/MBEN_T/analysis_params.yaml') as stream:
    d = yaml.load(stream, Loader=BaseLoader)
print(d)


# In[404]:


import panel as pn



# In[168]:


analysis_init.proj_data_folder_path


# In[350]:


import yaml
m=list(yaml.load(stream.read)
print(m)


# In[ ]:


@pn.depends('file_name', watch=True)
def _update_filename(self):
    self.download.filename = self.file_name


    
def update_sample_df(self, event=None):
    self.analysis_params = ap.analysis_params

@pn.depends("sample_df", watch=True)
def _update_table(self):
    if hasattr(self, "table"):
        self.table.value = self.sample_df.head(10)

def save_sample_data(self, event=None):
    if not self.sample_df is None:
        self.sample_df
        
def view(self):
    return pn.Column(
        "## Generate and Download Data",
        pn.Row(
            pn.Param(self, parameters=['generate_sample_df'], show_name=False, widgets={"generate_sample_df": {"button_type": "primary"}}),
            pn.Column(self.param.file_name, self.download, align='end', margin=(10,5,5,5)),
        ),
        "**Sample data (10 Rows)**",
        self.table,
    )

sample_data_app = SampleDataApp()
sample_data_app_view = sample_data_app.view()
sample_data_app_view


# **Click the `Save sample df` button**
# 
# This should save the dataframe to your default download folder. Now let us define the `VoltageApp` which will display the data we just generated.

# In[19]:


class VoltageApp(param.Parameterized):
    data = param.DataFrame()
    
    file_input = param.Parameter()
    
    def __init__(self, **params):
        super().__init__(file_input=pn.widgets.FileInput(), **params)
        self.plotly_pane = pn.pane.Plotly(height=400, sizing_mode="stretch_width")

    @pn.depends("file_input.value", watch=True)
    def _parse_file_input(self):
        value = self.file_input.value
        if value:
            string_io = io.StringIO(value.decode("utf8"))
            self.data = pd.read_csv(string_io, parse_dates=["Time"])
        else:
            print("error")

    @pn.depends('data', watch=True)
    def get_plot(self):
        df = self.data
        if df is None:
            return
        assert ("Voltage" in df.columns) and ("Time" in df.columns), "no columns voltage and time"
        df = (df.loc[df['Voltage'] != 'Invalid/Calib']).copy(deep=True)
        df['Voltage'] = df['Voltage'].astype(float)
        if "FubId" in df.columns:
            p = px.scatter(df, x="Time", y="Voltage", color="FubId")
        else:
            p = px.scatter(df, x="Time", y="Voltage")
        self.plotly_pane.object = p
        
    def view(self):
        return pn.Column(
            "## Upload and Plot Data",
            self.file_input,
            self.plotly_pane,
        )
    
voltage_app = VoltageApp()

voltage_app_view = voltage_app.view()
voltage_app_view


# Now let us put these two components together into a servable app:

# In[21]:


description = """
This application demonstrates the ability to **download** a file using the `FileDownload` widget 
and **upload** a file using the `FileInput` widget.
</br></br>
Try filtering the data, download the file by clicking on the Download button
and then plot it on the right by uploading that same file.
"""

component = pn.Column(
    description,
    #sample_data_app_view,
    voltage_app_view,
    sizing_mode='stretch_both'
)
component


# ## App
# 
# Lets wrap it into nice template that can be served via `panel serve download_upload_csv.ipynb`

# In[24]:


pn.template.FastListTemplate(site="Panel", title="Download and Upload CSV File", main=[ description, 
#sample_data_app_view, 
voltage_app_view,]).servable();


# In[25]:


pn.serve(component)


# In[ ]:




