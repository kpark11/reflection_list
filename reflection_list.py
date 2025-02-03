#!/usr/bin/env python
# coding: utf-8


### This program is to visualize the Reflection list after it is saved with Dashbaord. ###


import dash
from dash import dcc
from dash import State
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import os
import re
import base64
import dash_bootstrap_components as dbc
#from flask import Flask


cwd = os.getcwd()
file_path = os.path.join(cwd,'download')
try:
    os.mkdir(file_path)
except:
    print('already exists')
    
data_path = os.path.join(cwd,'data')

#testing_server = Flask(__name__)

app = dash.Dash(#server = testing_server, 
                external_stylesheets=[dbc.themes.LUX])

server = app.server

app.title = "Reflection List"
app.style = {'textAlign':'center','color':'#503D36','font-size':24}
#---------------------------------------------------------------------------------

app.layout = html.Div([
    
    html.H1("Reflection List", style={'textAlign': 'center', 'color': '#3E57B0','font-size':50}),
    
    html.Br(),
    
    html.H2("Description:", style={'textAlign': 'center', 'color': '#FF8903'}),
    
    html.P("Once you upload the .hkl file from Mag2Pol software, please wait. It is cleaning the text file.", 
           style={'textAlign':'center'}),
    
    dcc.Markdown("Here are MnO and LaMnO<sub>3</sub> .hkl files if you would like to test it.",
                 dangerously_allow_html=True,
                 style={'textAlign':'center'}),
    
    html.Div([
        html.Button("MnO file", id="button-MnO", 
                    style={'display':'inline-block',
                           'margin-left':'10px',
                           'background':'black',
                           'color':'white',
                           'border-radius':'10px'},),
        dcc.Download(id="download-MnO"),
    
        html.Button("LaMnO3 file", id="button-LMO",
                    style={'display':'inline-block',
                           'margin-left':'10px',
                           'background':'black',
                           'color':'white',
                           'border-radius':'10px'},),
        dcc.Download(id="download-LMO"),
        
        ], 
        style={'text-align':'center',
               'justify-content':'center',
               'align-items':'center'},
        ),
    
    html.Br(),
    
    html.P("You can visualize the polarization matrix by typing in the indices you want.",
          style={'textAlign':'center'}),
                       
    html.Div([html.Label("Upload here"),
              dcc.Upload(
                    id="upload",
                    children=html.Div(
                        ["Drag and drop or click to select a file to upload."]
                    ),
                    style={
                        "width": "98%",
                        "height": "60px",
                        "lineHeight": "60px",
                        "borderWidth": "1px",
                        "borderStyle": "dashed",
                        "borderRadius": "5px",
                        "textAlign": "center",
                        "margin": "10px",
                    },
                         )],
            style={'textAlign':'center','color':'#00AF4A'}),
    
    html.Div([html.Div([html.Label("h: ",  style={'text-align':'center'}),
                         dbc.Input(
                         id='h',
                        value=0,
                        placeholder=0,  style={'text-align':'center'})],
                        style={'text-align':'center',
                               'width':'25%',
                               "margin": "0 auto", 
                               'padding-right':'15px',
                               'display':'inline-block'}),
                html.Div([html.Label("k: ",  style={'text-align':'center'}),
                         dbc.Input(
                         id='k',
                        value=0,
                        placeholder=0,  style={'text-align':'center'})],
                        style={'text-align':'center',
                               'width':'25%',
                               "margin": "0 auto", 
                               'padding-right':'15px',
                               'display':'inline-block'}),
                html.Div([html.Label("l: ",  style={'text-align':'center'}),
                         dbc.Input(
                         id='l',
                        value=0,
                        placeholder=0,  style={'text-align':'center',})],
                        style={'text-align':'center',
                               'width':'25%',
                               "margin": "0 auto", 
                               'padding-right':'15px',
                               'display':'inline-block'})],
             style={'text-align':'center',
                    'justify-content':'center',
                    'align-items':'center',
                    'width':'100%'}),
              
    
    
    html.Div([
        #html.Div(id='output-file',className='file',style={'display':'flex'}),
        #html.Div(id='output-hkl',className='HKL',style={'display':'flex'}),
        #html.Div(id='output-container', className='chart-grid', style={'display':'flex'}),
        html.Div('Input File:', style={'font-weight':'bold'}),
        
        dcc.Loading(id="ls-loading",
                    children=[
                        html.Div(id='output-file',className='file',style={'display':'flex'})
                    ],
                    type="circle"),
        
        html.Div('Chosen Indices (hkl):', style={'font-weight':'bold'}),
        
        dcc.Loading(id="ls-loading-1",
                    children=[
                        html.Div(id='output-hkl',className='HKL',style={'display':'flex'})
                    ],
                    type="circle"),
        
        html.H5("Graphs", style={'textAlign': 'center', 'color': '#3E57B0'}),
        
        dcc.Loading(id="ls-loading-2",
                    children=[
                        html.Div(id='output-container', className='chart-grid', style={'display':'flex'})
                    ],
                    type="circle")
    ]),
    
    
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
    Output("download-MnO", "data"),
    Input("button-MnO", "n_clicks"),
    prevent_initial_call=True,
)

def download_MnO(n_clicks):
    data_file = os.path.join(data_path, 'MnO.hkl')
    data = open(data_file, 'r', encoding='utf-8')
    lines = data.readlines()
    data.close()
    print(' '.join(lines))
    return dict(content=''.join(lines), filename="MnO.hkl")

@app.callback(
    Output("download-LMO", "data"),
    Input("button-LMO", "n_clicks"),
    prevent_initial_call=True,
)

def download_LMO(n_clicks):
    data_file = os.path.join(data_path, 'LaMnO3.hkl')
    data = open(data_file, 'r', encoding='utf-8')
    lines = data.readlines()
    data.close()
    print(lines)
    return dict(content=''.join(lines), filename="LaMnO3.hkl")
        
@app.callback(
    Output(component_id='ls-loading',component_property='children'),
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
        return 'You need to input .hkl file'


@app.callback(
    Output(component_id='ls-loading-1',component_property='children'),
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
    Output(component_id='ls-loading-2',component_property='children'),
    [Input(component_id='ls-loading',component_property='children'),
     Input(component_id='ls-loading-1',component_property='children')]
)

def update_output_container(file,indices):
    try:
        if '_cleaned.txt' in file:
            data = pd.read_fwf(file)
            header = ['Pxx','Pxy','Pxz','Pyx','Pyy','Pyz','Pzx','Pzy','Pzz']

            h = int(indices[0])
            k = int(indices[1])
            l = int(indices[2])
            h1 = str(indices[0])
            k1 = str(indices[1])
            l1 = str(indices[2])
            
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
                    title=h1+','+k1+','+l1+' and q = ' +q,
                    labels={'x': '', 'y':''}))

                bar_plot2 = dcc.Graph(figure=px.bar(y1, 
                    x=header,
                    y=y1,
                    title=h1+','+k1+','+l1+' and q = ' +q1,
                    labels={'x': '', 'y':''}))
                
                bar_plot3 = dcc.Graph(figure=px.bar(y2, 
                    x=header,
                    y=y2,
                    title=h1+','+k1+','+l1+' and q = ' +q2,
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
                    title=str(h1+','+k1+','+l1+' and q = '+q),
                    labels={'x': '', 'y':''}))

                bar_plot2 = dcc.Graph(figure=px.bar(y1, 
                    x=header,
                    y=y1,
                    title=str(h1+','+k1+','+l1+' and q = '+q1),
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
                    title=str(h1+','+k1+','+l1+' and q = '+q),
                    labels={'x': '', 'y':''}))

                return html.Div(className='chart-grid',children=html.Div(bar_plot1),style={'display':'flex'})

            else:
                None
        else:
            None

    
    except:
        return html.Div('Error')
    
    
    
if __name__ == '__main__':
    app.run_server(debug=True)





