import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import numpy as np
from textwrap import dedent
import codecs, json 
import pandas as pd
import math
import matplotlib.pyplot as plt
from dash.exceptions import PreventUpdate
import urllib
import ttim


external_stylesheets = ['/assets/main.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server


colors = {
    'background': '#BF5700',
    'text': '#333F48',
    'darker':'#cc0000',
    'out':'#FFFF00'
}

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

app.title = 'TTim on the Web'



#app.layout - porvides the main app layout
app.layout =html.Div(children=[
        # .container class is fixed, .container.scalable is scalable
        html.Div(style={'backgroundColor': colors['background'], 'border-top-left-radius':'10px', 'border-top-right-radius':'10px'}, children=[
        # Change App Name here
       
            html.H1(
                'TTim Multi-Layer, Transient, Analytic Element Model',
                style={
                'textAlign': 'center',
                'color': colors['text'],
                'fontSize': '70px'
                }
            ),
            html.Img(
                src='/assets/intera-logo-sm.png',
                style={
                    'height' : '10%',
                    'width' : '10%',
                    'float' : 'right',
                    'position' : 'relative',
                    'padding-top' : 0,
                    'padding-left' : 0
                    })
        ]),
 

        #app info
        html.Div(children=[
            html.Div(children=[
                html.H2('Simple TTim Applet'),
                ],
                ),
            html.Div([
                dcc.Tabs(
                    id="tabs",
                    value='tab-1',
                    parent_className='custom-tabs',
                    className='custom-tabs-container',
                    children=[

                    dcc.Tab(
                        label='Main',
                        value='tab-1',
                        className='custom-tab',
                        selected_className='custom-tab--selected'
                    ),
                    dcc.Tab(
                        label='More info',
                        value='tab-2',
                        className='custom-tab',
                        selected_className='custom-tab--selected'
                    ),
                    dcc.Tab(
                        label='How to use',
                        value='tab-3',
                        className='custom-tab',
                        selected_className='custom-tab--selected'
                    ),
                ],
                style={'width': '30%'}
                ),
            ],
            ),
            
            html.Div(id='tabs-content'),
            
            
        ],
        style={'padding': '0px 0px 50px 0px'}
        ),

        html.Hr(),

        html.Div([
            "This applet was built using ",
            html.A('Dash',
                target='_blank', href='https://plotly.com/dash/'),
            ", an open-sourced Python framework",
            html.Br(),
            "This applet was built using ",
            html.A('TTim',
                target='_blank', href='https://github.com/mbakker7/ttim'),
            ", A Multi-Layer, Transient, Analytic Element Model by Mark Bakker",
            html.Br(),
            "The ",
            html.A('INTERA Inc. ',
                target='_blank', href='https://www.intera.com/'),
            "in Austin Texas",
            dcc.Markdown('''
                Developed by Ross Kushnereit
                ''',
                style={'textAlign':'left', 'color':'#6B8E23'}),
        ],
        style={'padding': '0px 0px 0px 0px'}
        ),


               
],
style={'padding': '0px 50px 0px 50px','fontSize': '16px'}
)


#CALLBACK: TABS
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            
            dcc.Markdown(dedent('''
            The **TxASR app** provides a user-friendly interface with interactive features to assess the feasibility
            of water recharge, storage, and recovery.
            
            ''')),

            dcc.Markdown(dedent('''
            See the *'How to use'* tab to get started.
            
            ''')),
            
            html.P(
                [
                    "Download the TCEQ ASR ",
                    html.A('Application Guide',
                        download='Application_Guide.pdf', href='/assets/Application_Guide.pdf'),
                    ""
                ]
            ),
            html.Hr(),
            
            html.Div(
                id='instructions', style={'color': colors['text']}),
         
            #operational parameters
            html.Div(
                children=[
                html.Div(children=[       
                    html.H5('Operational Parameters:'),
                    html.Div(
                        id='nlay',
                        style={'width': '90%','textAlign': 'left'}
                        ),
                    html.Div(
                        id='tmax',
                        style={'width': '90%','textAlign': 'left'}
                        ),
                       
                    html.Div(
                        id='nwells',
                        style={'width': '90%','textAlign': 'left'}
                        ),
                    html.Div(
                        id='pumping-time',
                        style={'width': '90%','textAlign': 'left'}
                        ),
                    html.Div(
                        id='pumping-rate',
                        style={'width': '90%','textAlign': 'left'}
                        ),
                    # html.Div(id='tp-container',
                    #     children=[html.Div(
                    #         [dcc.Slider(
                    #             id='tp-num-points',
                    #             min=5,
                    #             max=25,
                    #             step=1,
                    #             value=10,
                    #             updatemode='drag'
                    #         )
                    #         ],
                    #     style={'width': '20%'}
                    #     ),        
                    #     html.Div(id='tp-points-text'),
                    # ],
                    # ),
                ],style={'width': '50%','display': 'inline-block','textAlign': 'left', 'color': colors['text'],}
                ),
                #physical parameters
                html.Div(children=[
                    html.H5('Physical Parameters:',
                    style={'width': '90%','textAlign': 'left'}
                    ),
                    html.Div(
                        id='hydraulic-conductivity',
                        style={'width': '90%','textAlign': 'left'}
                        ),
                    html.Div(
                        id='specific-storage',
                        style={'width': '90%','textAlign': 'left'}
                        ),
                    html.Div(
                        id='porosity',
                        style={'width': '90%','textAlign': 'left'}
                        ),
                    html.Div(
                        id='aquifer-thickness',
                        style={'width': '90%','textAlign': 'left'}
                        ),  
                ],
                style={'padding': '0 0 0 0','width': '50%','display': 'inline-block','textAlign': 'center','vertical-align':'top', 'color': colors['text']  }
                ),
            ],
            ),
            
            html.Div([
                html.Label('More Options:',
                    style={
                    'fontWeight': 'bold'
                    }
                ),
                dcc.RadioItems(
                    id='time-radio',
                    options=[{'label': k, 'value': k} for k in [' Manual data entry'
                                                                ]
                             ],
                    value=' Manual data entry',
                    style={'color': colors['text'], 'fontStyle': 'italic'}
                ),
                
            ],style={'padding': '30px 0px 0px 0px','width': '50%', 'color': colors['text']},
            ),
                    
                    #submit button
            html.Div(children=[
                dcc.ConfirmDialogProvider(
                    html.Button(
                      'Submit',
                      style={
                        'backgroundColor': colors['background'],
                        'color': colors['text'],
                        'fontWeight': 'bold',
                        'fontSize': '20px'}
                    ),
                    id='submit-button',
                    message='Are you sure you want to continue?'
                    ),
                dcc.Markdown('*click button to generate graphs below*')
            ],
                style={'width': '90%','textAlign': 'right'}
            ),
            # html.Hr(),
            #parameter options, i.e., input or slider
            
            html.Div(
                id='error',
                style={
                    'backgroundColor': '#FFCCCC',
                    'color': 'black',
                    'opacity': '.9',
                    'border-radius': '25px'
                   
                    #'fontWeight': 'bold',
                    #'fontSize': '20px'
                }
            ),
            html.Hr(),

            html.Div(dcc.Markdown('*click data points on "Recovery Efficiency vs Pumping Time" graph to generate corresponding "Front Positions for a Single Well" graph*')),
            # graphs- first row
            html.Div(children=[
                html.Div([
                    dcc.Graph(
                        id='recovery-scatter',
                  
                        
                        config={
                            'toImageButtonOptions':{
                                'format': 'png', #one of png, svg, jpeg, webp
                                'filename': 'graph_recovery',
                                #'height': 1000,
                                #'width': 1400,
                                'scale': 5 #Multiply title/legend/axis/canvas sizes by this facto
                                }
                        },
                        
                    ),
                    html.A(
                        html.Button('Download data'),
                        id='download-link',
                        download="data_recovery.csv",
                        href="",
                        target="_blank"
                    ),
                    dcc.Markdown(dedent('*download data for "Recovery Efficiency vs Pumping Time" graph*'))
                    ],
                    style={'width': '49%', 'display': 'inline-block'},
                    ),
                html.Div([
                    dcc.Graph(
                        id='front-position-graph',
                        
                        config={
                            'toImageButtonOptions':{
                                'format': 'png', #one of png, svg, jpeg, webp
                                'filename': 'graph_fronts',
                                #'height': 1000,
                                #'width': 1400,
                                'scale': 5 #Multiply title/legend/axis/canvas sizes by this facto
                                }
                        },
                    ),
                    html.A(
                        html.Button('Download data'),
                        id='download-link-2',
                        download="data_fronts.csv",
                        href="",
                        target="_blank"
                    ),
                    dcc.Markdown(dedent('*download data for selected "Front Positions for a Single Well" graph*'))
                    ],
                    style={'width': '49%', 'display': 'inline-block'},
                    ),
            ],
    
            style={'padding': '0px 0px 0px 0px'}
            ),
               
            #hidden json data holder
            dcc.Loading(
                id='loading',
                children=[html.Div([html.Div(id='intermediate-value',style={'display': 'none'})])],
                type='cube',
                fullscreen=True,
                color=colors['background']
            ),
                
                
            ],
            style={'padding': '20px 0px 0px 0px'}
            )
    elif tab == 'tab-2':
        return html.Div([
        
            html.Div([
                dcc.Markdown('''
                >
                > **Aquifer Storage and Recovery** \[30 TAC &sect;331.2(8)\]: *"The injection of water into a geologic formation,
                > group of formations, or part of a formation that is capable
                > of underground storage of water for later retrieval and
                > beneficial use."*
                >
                '''),
                ],
                style ={'fontSize': '16px','width': '50%','padding': '0px 0px 0px 0px'}
            ),
            dcc.Markdown(''' The movement of injected waters into a confined aquifer
                is controlled both by the natural flow patterns
                in an aquifer and by the flow patterns generated
                during injection and pumping of water from wells. Understanding the 
        movement of injected waters
                is essential for predicting the efficiency of later
                retrieval (i.e., recovery efficiency).''',
                style={'padding': '0px 30px 0px 30px', 'textAlign': 'justify','width': '60%'}
            ),
            dcc.Markdown('''
                The TxASR App determines recoverability for a single ASR well under steady flow conditions.
                TxASR is based on the analytical solution of the *Complex Potential Function*
                for combined flow in the *(x, y)* plane derived by **Bear and Jacobs (1965)**.
                ''',
                style={'padding': '0px 30px 0px 30px', 'textAlign': 'justify','width': '60%'}
            ),
            html.Div(
                html.Img(
                    src='/assets/equation1.svg',
                    style={
                        #'height' : '70%',
                        #'width' : '70%',
                        'padding-top' : 0,
                        'padding-left' : 60,},
                ),
            ),
            dcc.Markdown('''
            **Figure 1** provides a conceptual diagram of an ASR system. The diagram depicts the injection stage of
            an ASR well with the conditions and variables required for the analytical solution.
            The solution assumes the following conditions:
            ''',
            style={'padding': '10px 30px 0px 30px','width': '60%'},
            ),
            dcc.Markdown('''
            * Homogeneous and isotropic aquifer properties
            * Confined aquifer with an infinite areal extent
            * Uniform aquifer thickness
            * Uniform transmissivity
            * Constant injection and pumping rates
            * Negligible elastic storativity
            * Negligible mixing and dispersion
            
            ''',
            style={'padding': '0px 30px 0px 60px','width': '60%'},
            ),
        
            dcc.Markdown('''
            Recoverability is determined by solving a *dimensionless* form of the *Complex
            Potential Function* during the injection and storage stage (i.e., recharge) and the pumping stage
            (i.e., recovery).
            ''',
                style={'padding': '0px 30px 0px 30px', 'textAlign': 'justify','width': '60%'}
            ),
            html.Div(
                html.Img(
                    src='/assets/equation4.svg',
                    style={
                        #'height' : '70%',
                        #'width' : '70%',
                        'padding-top' : 0,
                        'padding-left' : 80,},
                ),
            ),
            dcc.Markdown('''
            **Figure 2** provides a schematic for recoverability. The *Recovery Efficiency*
            and *Native Groundwater Recovery* is determined by superimposing the injection and pumping fronts.
            ''',
                style={'padding': '0px 30px 0px 30px', 'textAlign': 'justify','width': '60%'}
            ),
            
            html.Div(
                html.Img(
                    src='/assets/equation2.svg',
                    style={
                        #'height' : '70%',
                        #'width' : '70%',
                        'padding-top' : 0,
                        'padding-left' : 60,},
                ),
            ),
            
            html.Div(
                html.Img(
                    src='/assets/equation3.svg',
                    style={
                        #'height' : '70%',
                        #'width' : '70%',
                        'padding-top' : 0,
                        'padding-left' : 60,},
                ),
            ),
            dcc.Markdown('''
            The ASR app is an initial assessment, complex aquifer
            systems may require additional numerical modeling
            to justify recoverability.
            ''',
                style={'padding': '0px 30px 0px 30px', 'textAlign': 'justify','width': '60%'}
            ),

            html.Hr(),
            html.Div(
                html.Img(
                    src='/assets/variables.svg',
                    style={
                        #'height' : '70%',
                        #'width' : '70%',
                        'padding-top' : 0,
                        'padding-left' : 80,},
                ),
            ),
           
            html.Hr(),
            html.Img(
                src='/assets/ideal.png',
                style={
                    #'height' : '80%',
                    'width' : '50%',
                    #'position' : 'relative',
                    #'display': 'inline-block'
                    'padding-bottom' : 0,
                    'padding-left' : 30
                },
            ),
            dcc.Markdown('**Figure 1:** Conceptual Diagram of an ASR System with Homogeneous and Isotropic Properties',
                   style={'padding': '0px 0px 30px 30px'}),
            
            
            html.Img(
                src='/assets/bubbles.png',
                style={
                    #'height' : '90%',
                    'width' : '60%',
                    #'position' : 'relative',
                    'padding-top' : 30,
                    'padding-left' : 30
                },
            ),
            dcc.Markdown('**Figure 2:** Schematic for Recoverability',
                   style={'padding': '0px 0px 0px 30px'}),
            html.Hr(),
            dcc.Markdown('''
            ###### Reference:
            Bear, J.; Jacobs, M. On the Movement of Water Bodies Injected
            into Aquifers. *Journal of Hydrology* **1965**, 3 (1), 37–57.
            [https://doi.org/10.1016/0022-1694(65)90065-X] 
            (https://doi.org/10.1016/0022-1694(65)90065-X).
            ''',
            style={'padding': '0px 0px 0px 30px','width': '60%'}
            ),    
        ],
        style={'fontSize': '16px'},
        )
    elif tab == 'tab-3':
        return html.Div([
            dcc.Markdown(
            '''### Getting started is easy
            ''',
            style={'padding': '0px 0px 0px 30px','width': '60%'}),

            dcc.Markdown(
            '''
            * **Step 1:** Input operational and physical parameters
                * Click and drag slider handles to select desired parameter values
                * Toggle keyboard arrows for fine adjustment
                    * ![](/assets/step1.gif)               
            * **Step 1 (more options):** Select a different form of data entry using the 'More Options' radio inputs
                * Click *'Single time point entries'* to select a single injection, delay, and pumping time (default option)
                    * ![](/assets/step1a.gif)
                * Click *'Ranged pumping time entry'* to select a range of pumping times 
                    * An array of evenly spaced pumping time points (rounded to the nearest integer)
                    within the selected range is generated
                    * Note that a *'Number of points'*  slider appears under pumping. It allows you to select the number of pumping time points  
                        * It is suggested to begin trial runs with 10 time points (default value)
                        * The more time points you select the greater the computational time
                    * ![](/assets/step1b.gif)
                * Click *'Ranged injection & pumping time entries'* to select a range
                    for injection and pumping times.
                    * An array of 3 evenly spaced injection time
                    points (rounded to the nearest integer) within the selected range
                    is generated
                    * An array of evenly spaced pumping time points (rounded to the nearest integer)
                    within the selected range is generated
                    * ![](/assets/step1c.gif)
                * Click *'Ranged delay & pumping time entries'* to select a range for delay and pumping times.
                    * An array of 3 evenly spaced delay time points
                    (rounded to the nearest integer) within the selected range
                    is generated
                    * An array of evenly spaced pumping time points (rounded to the nearest integer)
                    within the selected range is generated
                    * ![](/assets/step1d.gif)
                * Click *'Manual data entry'* to enter all parameter values manually
                    * Injection, delay, and pumping times may be entered as single or multiple time points
                    * Multiple time points must be separated by commas 
                    * There must be an equal number of injection and delay time points 
                    * The default time point entries provided are an example of multiple entries
                    * ![](/assets/step1e.gif)                             
            * **Step 2:** Submit data 
                * Click the *'Submit'* button to run calculations and generate results
                    * ![](/assets/step3.gif)
            * **Step 3:** View generated graphs
                * Click on data points in the graph titled *'Recovery Efficiency vs Pumping Time'* to generate the corresponding *'Front Positions for a Single Well'* graph
                * Note that the pumping time point where the volume injected equals the volume pumped *(Vi=Vp)* is generated by default in *'Recovery Efficiency vs Pumping Time'* graph (i.e., tp= ti\*Qi/Qp)
                    * ![](/assets/step4.gif)              
            * **Step 4:** Use the [Modebar] (https://help.plot.ly/getting-to-know-the-plotly-modebar/#an-introduction-to-chart-studio-modebar)
                * The modebar is the strip of icons at the top of the plot
                * Icons include *download plot, zoom, pan, zoom in/out,
                autoscale and reset axes, toggle spike lines, show closest data on hover,
                compare data on hover* 
                * Click on desired icons to enhance your data visualization               
                    * ![](/assets/step5.gif)
            * **Step 5:** Download graphs
                * Click the modebar *'download plot'* icon to download graphs a PNG file
                * Download PNG for the *'Recovery Efficiency vs Pumping Time'* graph or a selected *'Front Positions for a Single Well'* graph
                    * ![](/assets/step6.gif)
            * **Step 6:** Download raw data
                * Click the *'DOWNLOAD DATA'* buttons to download tabular raw data as a CSV file
                * Download CSV for the *'Recovery Efficiency vs Pumping Time'* graph or a selected *'Front Positions for a Single Well'* graph
                * CSV files may be opened with software such as Microsoft Excel
                    * ![](/assets/step7.gif)
            
            * **Step 7:** Rinse and repeat! Simply change parameters and resubmit, or refresh the page and resubmit
            ''',
            style={'padding': '0px 0px 0px 60px','width': '60%','fontSize': '18px'}),

            
        ])

app.config.suppress_callback_exceptions = True 
#CALLBACK: output time-radio for injection
@app.callback([
    dash.dependencies.Output('nwells', 'children'),
    dash.dependencies.Output('pumping-time', 'children'),
    dash.dependencies.Output('pumping-rate', 'children'),
    dash.dependencies.Output('nlay', 'children'),
    dash.dependencies.Output('tmax', 'children'),
    dash.dependencies.Output('hydraulic-conductivity', 'children'),
    dash.dependencies.Output('specific-storage', 'children'),
    dash.dependencies.Output('porosity', 'children'),
    dash.dependencies.Output('aquifer-thickness', 'children'),
    dash.dependencies.Output('instructions','children')],
    [dash.dependencies.Input('time-radio', 'value')])
def model_option(option):
    if option == ' Manual data entry':
        return [html.Div(children=[
            html.Label(
                dcc.Markdown(
                    dangerously_allow_html=True,
                    children=dedent(
                        'Number of Pumping Wells'),
                ),  
                style={'fontWeight': 'bold'}
            ),
            dcc.Input(
                id='nwells',
                # value='30, 60, 90',
                # type='text'
                value=1,
                type='number',
                min=0
            ),
            html.Div(id='nwells-output-text'),
        ]
        ),
        html.Div(children=[
            html.Label(
                dcc.Markdown(
                    dangerously_allow_html=True,
                    children=dedent(
                        'Pump Time (t<sub>p</sub>), days'),
                ),
                style={'fontWeight': 'bold'}
            ),
            dcc.Input(
                id='pumping-time',
                value='30, 60, 90',
                type='text'
            ),
            html.Div(id='tp-output-text')
        ]
        ),
        html.Div(children=[
            html.Label(
                dcc.Markdown(
                    dangerously_allow_html=True,
                    children=dedent(
                        'Pumping Rate (Q<sub>p</sub>), gpm'),
                ),
                style={'fontWeight': 'bold'}),
            dcc.Input(
                id='pumping-rate',
                value='0, 1000, 3000',
                type='text'
            ),
            html.Div(id='qp-output-text')
        ],    
        ),
        #injection rate
        html.Div(children=[
            html.Label(
                dcc.Markdown(
                    dangerously_allow_html=True,
                    children=dedent(
                        'Number of layers'),
                ),
                style={'fontWeight': 'bold'},
            ),
            dcc.Input(
                id='nlay',
                value=1,
                type='number',
                min=0
            ),
            html.Div(id='nlay-output-text')
        ],
        ),
        #pumping rate
        html.Div(children=[
            html.Label(
                dcc.Markdown(
                    dangerously_allow_html=True,
                    children=dedent(
                        'Model Run Time (tmax) days'),
                ),
                style={'fontWeight': 'bold'},
            ),
            dcc.Input(
                id='tmax',
                value=365.25,
                type='number',
                min=0
            ),
            html.Div(id='tmax-output-text')
        ],
        ),
        #hydraulic conductivity
        html.Div(children=[
            html.Label(
                dcc.Markdown(
                    dangerously_allow_html=True,
                    children=dedent('Hydraulic Conductivity (K<sub>d</sub>), ft/day')),    
                style={'fontWeight': 'bold'}
            ),
            dcc.Input(
                id='hydraulic-conductivity',                        
                value=20,
                type='number',
                min=0
            ),
            html.Div(id='kd-output-text')
        ],
        ),
        #hydraulic gradient
        html.Div(children=[
            html.Label(dcc.Markdown('Specific-Storage, 1/ft'),    
                style={'fontWeight': 'bold'}),
            dcc.Input(
                id='specific-storage',
                value=0.0001,
                type='number',
                min=0
            ),
            html.Div(id='specific-storage-output-text')
        ],
        ),
        #porosity
        html.Div(children=[
            html.Label(dcc.Markdown('Porosity (n)'),    
                style={'fontWeight': 'bold'}),
            dcc.Input(
                id='porosity-intermediate',
                value=0.3,
                type='number',
                min=0,
                max=1,
                step= 0.1
                ),
            html.Div(id='n-output-text')
        ],
        ),
        #aquifer thickness
        html.Div(children=[
            html.Label(dcc.Markdown('Aquifer Thickness (B), ft'),    
                style={'fontWeight': 'bold'}),
            dcc.Input(
                id='aquifer-thickness',
                value=100,
                type='number',
                min=0
                ),
            html.Div(id='B-output-text')
        ],
        ),
        html.Div(children=[dcc.Markdown('''
            *This option allows you to enter parameter values manually.*
            
            *Injection, delay, and pumping times may be entered as single or multiple time points. 
            If entering multiple points, separate each value by a comma.
            There must be an equal number of injection and delay time points. 
            The default time point entries provided are an example of multiple entries.*''',
            style={'background-color': colors['out']}),
        ],
        ),
        ] 
    
    else:
        
        raise PreventUpdate
 
#CALLBACK: ALL input texts
@app.callback([
    dash.dependencies.Output('nlay-output-text', 'children'),
    dash.dependencies.Output('kd-output-text', 'children'),
    dash.dependencies.Output('specific-storage-output-text', 'children'),
    dash.dependencies.Output('B-output-text', 'children'),
    dash.dependencies.Output('qp-output-text', 'children'),
    dash.dependencies.Output('n-output-text', 'children'),
    dash.dependencies.Output('nwells-output-text', 'children'),
    dash.dependencies.Output('tmax-output-text', 'children'),
    dash.dependencies.Output('tp-output-text', 'children')],
              
    [dash.dependencies.Input('nlay', 'value'),
    dash.dependencies.Input('hydraulic-conductivity', 'value'),
    dash.dependencies.Input('specific-storage', 'value'),
    dash.dependencies.Input('aquifer-thickness', 'value'),
    dash.dependencies.Input('tmax', 'value'),
    dash.dependencies.Input('porosity', 'value'),
    dash.dependencies.Input('time-radio', 'value'),
    dash.dependencies.Input('nwells', 'value'),
    dash.dependencies.Input('pumping-time', 'value'),
    dash.dependencies.Input('pumping-rate', 'value')])

def callback_a(nlay,hk,Saq,thk,tmax,variable_option,v7,nwells,pt,Qs):
    # this will be the function that converts the web inputs into inputs for the ttim model
    # if variable_option ==' Manual data entry':
    if nwells == 1:
        ptimes = [float(v) for v in pt.split(',')]
        Qgpm = [float(v) for v in Qs.split(',')]

        tsandQ_dict = {}
        tsandQ = []
        for pi, ptime in enumerate(ptimes):
            tsandQ.append((ptime,Qgpm[pi])) # todo convert to cfd
        tsandQ_dict[0] = tsandQ

    if nlay == 1:
        # nwells = int(nwells) + 'hi'

        # float(Qs)
        tmax = float(tmax)
        hk = float(hk)
        z = [float(thk),0]
        ml = ttim.ModelMaq(kaq=hk, z=z, Saq=Saq, tmin=1e-5, tmax=tmax)

        for w in range(nwells):
            tsandQ = tsandQ_dict[0]
            w = ttim.Well(ml, xw=0, yw=0, rw=0.1, tsandQ=tsandQ, layers=0)

        ml.solve()
        h = ml.head(0,0,np.arange(1e-5,tmax,30))
        print(h)

    Qi, Qp, kd, dhdx, n, B, ti, td, tp = [n for n in range(9)]
    return nlay, Qp, kd, dhdx, n, B, ti, td, tp



if __name__ == '__main__':
    app.run_server(debug=True)