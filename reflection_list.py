#!/usr/bin/env python
# coding: utf-8

# In[39]:


### This program is to visualize the Reflection list after it is saved with Dashbaord. ###


import dash
from dash import dcc
from dash import State
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import os
import re
import sys
import fnmatch
import matplotlib.pyplot as plt
import base64

cwd = os.getcwd()
print(cwd)
file_path = cwd+'\download'
try:
    os.mkdir(file_path)
except:
    print('already exists')


app = dash.Dash(__name__)

server = app.server

app.title = "Reflection List"
app.style = {'textAlign':'center','color':'#503D36','font-size':24}
#---------------------------------------------------------------------------------

app.layout = html.Div([
    html.H1("Reflection List"),
    
    html.H2("Description:"),
    html.P("Once you upload the .hkl file from Mag2Pol software, please wait. It is little slow :)."),
    html.P("You can visualize the polarization matrix by typing in the indices you want."),
                       
    html.Div([html.Label("Upload here"),
              dcc.Upload(
                    id="upload",
                    children=html.Div(
                        ["Drag and drop or click to select a file to upload."]
                    ),
                    style={
                        "width": "90%",
                        "height": "60px",
                        "lineHeight": "60px",
                        "borderWidth": "1px",
                        "borderStyle": "dashed",
                        "borderRadius": "5px",
                        "textAlign": "center",
                        "margin": "10px",
                    },
                         )]),
    
    html.Div([html.Label("h: "),
             dcc.Input(
             id='h',
            value=0,
            placeholder=0)]),
    html.Div([html.Label("k: "),
             dcc.Input(
             id='k',
            value=0,
            placeholder=0)]),
    html.Div([html.Label("l:  "),
             dcc.Input(
             id='l',
            value=0,
            placeholder=0)]),
              
    
    
    html.Div([
        html.Div(id='output-file',className='file',style={'display':'flex'}),
        html.Div(id='output-hkl',className='HKL',style={'display':'flex'}),
        html.Div(id='output-container', className='chart-grid', style={'display':'flex'})]),
    
    
])


def save_file(contents,name):
    new_path = os.path.join(file_path, name)
    try:
        data = contents.encode("utf8").split(b";base64,")[1]
        with open(new_path, "wb") as fp:
            fp.write(base64.decodebytes(data))
        return str(new_path)
    except:
        return str(new_path)


        
@app.callback(
    Output(component_id='output-file',component_property='children'),
    [Input('upload','contents'),
     State('upload','filename')]
    )

def update_upload_container(contents,name):    
    try:
        if '.hkl' in name:
            new_path = save_file(contents,name)
            writing = open(new_path,'r')
            lines = writing.readlines()
            writing.close()
            del lines[:9]

            new_file = re.sub('\.hkl','_cleaned.txt',name)
            new_file_path = os.path.join(file_path, new_file)
            new_writing = open(new_file_path,'w+')
            for line in lines:
                line1 = re.sub('\(snan\)',' 0.000 ',line)
                line2 = re.sub('nan',' ',line1)
                line3 = re.sub('\!','',line2)
                line = line3
                new_writing.write(line)
            new_writing.close()

            return new_file_path
    except:
        return None


@app.callback(
    Output(component_id='output-hkl', component_property='children'),
    [Input(component_id='h',component_property='value'),
     Input(component_id='k',component_property='value'),
     Input(component_id='l',component_property='value')]
     )

def update_hkl_container(h,k,l):
    if h == '' or k == '' or l == '' or h == '-' or k == '-' or l == '-':
        return [0,0,0]
    else:
        indices = [int(h),int(k),int(l)]
        return indices

@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='output-file',component_property='children'),
     Input(component_id='output-hkl',component_property='children')]
     )

def update_output_container(file,indices):
    try:
        if '_cleaned.txt' in file:
            data = pd.read_fwf(file)
            header = ['Pxx','Pxy','Pxz','Pyx','Pyy','Pyz','Pzx','Pzy','Pzz']
            h = indices[0]
            k = indices[1]
            l = indices[2]
            h1 = str(h)
            k1 = str(k)
            l1 = str(l)
            
            hkl = data.loc[(data['h']==h) & (data['k']==k) & (data['l']==l)].index
            
            if len(hkl)==3:
                hkl0 = hkl[0]
                hkl1 = hkl[1]
                hkl2 = hkl[2]

                mas = data[header].loc[hkl0].reset_index()
                q = data['q'].loc[hkl0]
                q = str(q)
                mas1 = data[header].loc[hkl1].reset_index()
                q1 = data['q'].loc[hkl1]
                q1 = str(q1)
                mas2 = data[header].loc[hkl2].reset_index()
                q2 = data['q'].loc[hkl2]
                q2 = str(q2)

                y = mas.values
                y = list(y[:,1])
                y1 = mas1.values
                y1 = list(y1[:,1])
                y2 = mas2.values
                y2 = list(y2[:,1])

                bar_plot1 = dcc.Graph(figure=px.bar(y, 
                    x=header,
                    y=y,
                    title=str(h1+','+k1+','+l1+' and q = ' +q),
                    labels={'x': '', 'y':''}))

                bar_plot2 = dcc.Graph(figure=px.bar(y1, 
                    x=header,
                    y=y1,
                    title=str(h1+','+k1+','+l1+' and q = ' +q1),
                    labels={'x': '', 'y':''}))
                
                bar_plot3 = dcc.Graph(figure=px.bar(y2, 
                    x=header,
                    y=y1,
                    title=str(h1+','+k1+','+l1+' and q = ' +q2),
                    labels={'x': '', 'y':''}))

                return html.Div(className='chart-grid',children=[html.Div(bar_plot1),html.Div(bar_plot2),html.Div(bar_plot3)],style={'display':'flex'})


            elif len(hkl)==2:
                hkl0 = int(hkl[0])
                hkl1 = int(hkl[1])

                mas = data[header].loc[hkl0].reset_index()

                q = data['q'].loc[hkl0]
                q = str(q)
                mas1 = data[header].loc[hkl1].reset_index()
                q1 = data['q'].loc[hkl1]
                q1 = str(q1)

                y = mas.values
                y = list(y[:,1])
                y1 = mas1.values
                y1 = list(y1[:,1])

                bar_plot1 = dcc.Graph(figure=px.bar(y, 
                    x=header,
                    y=y,
                    title=str([h1+','+k1+','+l1+' and q = '+q]),
                    labels={'x': '', 'y':''}))

                bar_plot2 = dcc.Graph(figure=px.bar(y1, 
                    x=header,
                    y=y1,
                    title=str([h1+','+k1+','+l1+' and q = '+q1]),
                    labels={'x': '', 'y':''}))

                return html.Div(className='chart-grid',children=[html.Div(bar_plot1),html.Div(bar_plot2)],style={'display':'flex'})

            elif len(hkl)==1:

                mas = data[header].loc[hkl].reset_index()     

                q = data['q'].loc[hkl]
                q = q.values
                q = str(q)

                y = mas.to_numpy()
                y = list(y[0,1:])

                bar_plot1 = dcc.Graph(figure=px.bar(y, 
                    x=header,
                    y=y,
                    title=str([h1+','+k1+','+l1+' and q = '+q]),
                    labels={'x': '', 'y':''}))

                return html.Div(className='chart-grid',children=html.Div(bar_plot1),style={'display':'flex'})

            else:
                None


    
    except:
        None
    
    
    
if __name__ == '__main__':
    app.run_server(debug=True)




# In[ ]:




