#----------------------------# Load Your Dependencies#--------------------------#
import dash
from dash import  dcc    # Dash core Components
from dash import html   # HTML for Layout and Fonts
import plotly.express as px           # Plotly Graphs uses graph objects internally
from plotly.subplots import make_subplots
import plotly.graph_objects as go     # Plotly Graph  more customized 
import pandas as pd                   # Pandas For Data Wrangling
import numpy as np
from dash import Input, Output, dash_table  # Input, Output for  Call back functions
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#--------------------------#Instanitiate Your App#--------------------------#

app = dash.Dash(__name__)  
server = app.server

#--------------------------# Pandas Section #------------------------------#

df =pd.read_csv('marketing_data.csv')
df['Income'] = df[" Income "].astype('str').str.extractall('(\d+)').unstack().fillna('').sum(axis=1).astype(int)
df['Income'].fillna(df['Income'].mode()[0], inplace=True)
df['Age'] = 2021 - df['Year_Birth']
df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'], format="mixed")
df['Enrol_years'] = 2021 - df['Dt_Customer'].dt.year
df["Total_amount_spent"] = df["MntFruits"] + df["MntMeatProducts"] + df["MntFishProducts"] + df["MntSweetProducts"] + df["MntGoldProds"]
df['Total_campaign'] = df['AcceptedCmp1'] + df['AcceptedCmp2'] + df['AcceptedCmp3'] + df['AcceptedCmp4'] + df['AcceptedCmp5'] + df['Response']
df["Total_Purchases"] = df["NumDealsPurchases"] + df["NumWebPurchases"] + df["NumCatalogPurchases"] + df["NumStorePurchases"]
df['Income_cat'] = pd.cut(df['Income'], 3, labels=['Low', 'Middle', 'High'])
demog = ['Education', 'Marital_Status', 'Income_cat', 'Kidhome', 'Teenhome', 'Country']
demogs = ['Education', 'Marital_Status', 'Income', 'Kidhome', 'Teenhome', 'Country', 'Age']
activ = ['Dt_Customer', 'Enrol_years', 'Recency']
spent = ['MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds', 'Total_amount_spent']
purch = ['NumDealsPurchases', 'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases', 'Total_Purchases']
visit = ['NumWebVisitsMonth']
compan = ['AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5', 'AcceptedCmp1', 'AcceptedCmp2', 'Response', 'Total_campaign']
compln = ['Complain']
val_typ = {'Product amount':['MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds'], 'Purchased amount':['NumDealsPurchases', 'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases'], 'Accepted campaign': ['AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5', 'AcceptedCmp1', 'AcceptedCmp2', 'Response']}
names = list(val_typ.keys())
cust_df = ['Kidhome', 'Teenhome', 'Recency', 'Response', 'Complain', 'Income', 'Age', 'Enrol_years', 'Total_amount_spent', 'Total_campaign', 'Total_Purchases']
all_df = ['Kidhome', 'Teenhome', 'Recency', 'MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds', 'NumDealsPurchases', 'NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases', 'NumWebVisitsMonth', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5', 'AcceptedCmp1', 'AcceptedCmp2', 'Response', 'Complain', 'Income', 'Age', 'Enrol_years']
#--------------------------------------------------------------------------#
    
app.layout = html.Div([html.Div([html.A([html.H2('Marketing Data Analysis Dashboard'),html.Img(src='/assets/logo3.png')],
                                        href='http://projectnitrous.com/')],className="banner"),
                       dcc.Tabs(
                           id='tabs-parent',
                           value='tab-1',
                           parent_className='custom-tabs',
                           className='custom-tabs-container',
                           children=[
                               dcc.Tab(
                                   label='Tab 1',
                                   value='tab-1',
                                   className='custom-tab',
                                   selected_className='custom-tab--selected',
                                   children=[
                                       html.Div([
                                            html.Div([html.Br(),],className="eleven columns", style={'padding':5}),
                                            
                                            # First Row
                                            html.Div([
                                                html.Div([
                                                    html.H6('The average customer for this company looks like (depending on)  '),
                                                ], className='five columns'),
                                                html.Div([
                                                    dcc.Dropdown(
                                                            id='dropdown_dem',
                                                            options=[{'label':demogs[i], 'value':demogs[i]} for i in range(len(demogs))],
                                                            value=demogs[0],
                                                            multi=False,
                                                            searchable=True,
                                                            clearable=False,
                                                       ),
                                                ], className='two-half columns', style={'margin-left':30}),
                                                html.Div([
                                                    html.Div(html.Button('Send Email', id='submit-val', n_clicks=0), className='five columns'),
                                                    html.Div(id='div_email', className='five columns', style={'margin-left':20}),
                                                ], className='two-half columns', style={'margin-left':80}),
                                            ], className='eleven columns', style={'backgroundColor': '#01429e', 'padding':10, 'border-radius': 10, 'margin-left':20}),
                                            html.Div([html.Br(),],className="eleven columns", style={'padding':5}),
 
                                            # Second Row
                                            html.Div([
                                                html.H6('Unique values'),
                                                html.Div(id='div_uni', style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
                                            ], className='two-half columns', style={'backgroundColor': '#01429e', 'padding':15, 'border-radius': 10, 'margin-left':20}),
                                            html.Div([
                                                html.H6('Most frequent'),
                                                html.Div(id='div_mst', style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
                                            ], className='two-half columns', style={'backgroundColor': '#01429e', 'padding':15, 'border-radius': 10, 'margin-left':20}),
                                            html.Div([
                                                html.H6('Frequency'),
                                                html.Div(id='div_frq', style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
                                            ], className='two-half columns', style={'backgroundColor': '#01429e', 'padding':15, 'border-radius': 10, 'margin-left':20}),
                                            html.Div([
                                                html.H6('Total count'),
                                                html.Div(id='div_tot', style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
                                            ], className='two-half columns', style={'backgroundColor': '#01429e', 'padding':15, 'border-radius': 10, 'margin-left':20}),
                                            html.Div([html.Br(),],className="eleven columns"),
                                           
                                           # Third Row
                                           html.Div([
                                                html.Div([
                                                    html.H6('Select one of the elements  '),
                                                ], className='five columns'),
                                                html.Div([
                                                    dcc.Dropdown(
                                                            id='dropdown_elm',
                                                            options=[{'label':name, 'value':name} for name in val_typ],
                                                            value = list(val_typ.keys())[0],
                                                            multi=False,
                                                            searchable=True,
                                                            clearable=False,
                                                       ),
                                                ], className='five columns'),
                                               html.Div(id='div_tbl', className='twelve columns'),
                                           ], className='eleven columns', style={'backgroundColor': '#01429e', 'padding':10, 'border-radius': 10, 'margin-left':20}),
                                           html.Div([html.Br(),],className="eleven columns", style={'padding':5}),
                                           
                                           # Fourth Row
                                           html.Div([
                                                html.Div([
                                                    html.H6('Select one of the elements   '),
                                                ], className='seven columns'),
                                                html.Div([
                                                    dcc.Dropdown(
                                                            id='dropdown_cat',
                                                            options=[{'label':name, 'value':name} for name in val_typ],
                                                            value = list(val_typ.keys())[0],
                                                            multi=False,
                                                            searchable=True,
                                                            clearable=False,
                                                       ),
                                                ], className='four columns'),
                                               html.Div([html.H6('Counting the categorized element depending on the average value of each category, divied by above average and below average')], className='eleven columns'),
                                               html.Div([html.Br(),],className="eleven columns", style={'padding':5}),
                                               html.Div(id='div_tbl_cat', className='twelve columns'),
                                           ], className='five columns', style={'backgroundColor': '#01429e', 'padding':10, 'border-radius': 10, 'margin-left':20, 'height':560}),
                                           html.Div([
                                                html.Div([
                                                    html.H6('Customized correlation betweeen elements '),
                                                ], className='seven columns'),
                                                html.Div([
                                                    dcc.RadioItems(
                                                        id='radio_cor',
                                                        options=[
                                                            {'label': 'customized', 'value': 0},
                                                            {'label': 'all elements', 'value': 1},
                                                        ],
                                                        value=0,
                                                        labelStyle={'display': 'inline-block', 'color':'#ffffff'}
                                                    ),
                                                ], className='four columns'),
                                               html.Div([
                                                   dcc.Graph(id='heat_cor'), #, style={'height':150}
                                                ], className='twelve columns'),
                                           ], className='five columns', style={'backgroundColor': '#01429e', 'padding':10, 'border-radius': 10, 'margin-left':20, 'height':560}),
                                           html.Div([html.Br(),],className="eleven columns", style={'padding':5}),
                                        ], className="twelve columns", style={'backgroundColor': '#00307c', 'width':'calc(100% + 20px)', 'height':'100%', 'margin-left':-10, 'margin-right':0})
                                   ],
                               ),
                               dcc.Tab(
                                   label='Tab 2',
                                   value='tab-2',
                                   className='custom-tab',
                                   selected_className='custom-tab--selected',
                                   children=[
                                       html.Div([
                                            html.Div([html.Br(),],className="eleven columns", style={'padding':5}),
                                            # First Row
                                            html.Div([
                                                html.Div([
                                                    html.H6('Best type'),
                                                    html.Div([
                                                    dcc.Dropdown(
                                                                id='dropdown_typ',
                                                                options=[{'label':name, 'value':name} for name in val_typ],
                                                                value = list(val_typ.keys())[0],
                                                                multi=False,
                                                                searchable=True,
                                                                clearable=False,
                                                           ),
                                                        ], className='custom-dropdown-div',),
                                                    html.P('           ', style={'font-size': '1.1rem', 'color':'#ffffff'}),
                                                    html.P('Comparison between the different applied types', style={'font-size': '1.1rem', 'color':'#ffffff'}),
                                                ], className='four columns', style={'backgroundColor': '#004aad', 'padding':5, 'border-radius': 10, 'height':"100%"}),
                                                html.Div(['   '], style={'padding':5}),
                                                html.Div([
                                                    dcc.Graph(id='pie_typ', style={'height':150}),
                                                ], className='eight columns', style={'backgroundColor': '#01429e', 'padding':0, 'border-radius': 10, 'margin-left':2}),
                                            ], className='two columns', style={'backgroundColor': '#01429e', 'padding':0, 'border-radius': 10, 'margin-left':20}),
                                            html.Div([
                                                html.Div([
                                                    html.H6('Products'),
                                                    html.Div([
                                                    dcc.Dropdown(
                                                                id='dropdown_spt',
                                                                options=[{'label':spent[i], 'value':spent[i]} for i in range(len(spent))],
                                                                value=spent[0],
                                                                multi=False,
                                                                searchable=True,
                                                                clearable=False,
                                                           ),
                                                        ], className='custom-dropdown-div',),
                                                    html.P('           ', style={'font-size': '1.1rem', 'color':'#ffffff'}),
                                                    html.P('Products spent amount at the last two years', style={'font-size': '1.1rem', 'color':'#ffffff'}),
                                                ], className='four columns', style={'backgroundColor': '#004aad', 'padding':5, 'border-radius': 10, 'height':"100%"}),
                                                html.Div(['   '], style={'padding':5}),
                                                html.Div([
                                                    dcc.Graph(id='pie_spt', style={'height':150}),
                                                ], className='eight columns', style={'backgroundColor': '#01429e', 'padding':0, 'border-radius': 10, 'margin-left':2}),
                                            ], className='two columns', style={'backgroundColor': '#01429e', 'padding':0, 'border-radius': 10, 'margin-left':20}),
                                            html.Div([
                                                html.Div([
                                                    html.H6('Purchased'),
                                                    html.Div([
                                                    dcc.Dropdown(
                                                                id='dropdown_prc',
                                                                options=[{'label':purch[i], 'value':purch[i]} for i in range(len(purch))],
                                                                value=purch[0],
                                                                multi=False,
                                                                searchable=True,
                                                                clearable=False,
                                                           ),
                                                        ], className='custom-dropdown-div',),
                                                    html.P('           ', style={'font-size': '1.1rem', 'color':'#ffffff'}),
                                                    html.P('Purchased used method at the last two years ', style={'font-size': '1.1rem', 'color':'#ffffff'}),
                                                ], className='four columns', style={'backgroundColor': '#004aad', 'padding':5, 'border-radius': 10, 'height':"100%"}),
                                                html.Div(['   '], style={'padding':5}),
                                                html.Div([
                                                    dcc.Graph(id='pie_prc', style={'height':150}),
                                                ], className='eight columns', style={'backgroundColor': '#01429e', 'padding':0, 'border-radius': 10, 'margin-left':2}),
                                            ], className='two columns', style={'backgroundColor': '#01429e', 'padding':0, 'border-radius': 10, 'margin-left':20}),
                                            html.Div([
                                                html.Div([
                                                    html.H6('Campaigns'),
                                                    html.Div([
                                                    dcc.Dropdown(
                                                                id='dropdown_cmp',
                                                                options=[{'label':compan[i], 'value':compan[i]} for i in range(len(compan))],
                                                                value=compan[0],
                                                                multi=False,
                                                                searchable=True,
                                                                clearable=False,
                                                           ),
                                                        ], className='custom-dropdown-div',),
                                                    html.P('           ', style={'font-size': '1.1rem', 'color':'#ffffff'}),
                                                    html.P('Accepted campaigns at the last two years ', style={'font-size': '1.1rem', 'color':'#ffffff'}),
                                                ], className='four columns', style={'backgroundColor': '#004aad', 'padding':5, 'border-radius': 10, 'height':"100%"}),
                                                html.Div(['   '], style={'padding':5}),
                                                html.Div([
                                                    dcc.Graph(id='pie_cmp', style={'height':150}),
                                                ], className='eight columns', style={'backgroundColor': '#01429e', 'padding':0, 'border-radius': 10, 'margin-left':2}),
                                            ], className='two columns', style={'backgroundColor': '#01429e', 'padding':0, 'border-radius': 10, 'margin-left':20}),
                                            html.Div([
                                                html.Div([
                                                    html.H6('Annual distriution', style={'margin-top': '0.5rem'}),
                                                    html.Div([
                                                       dcc.Dropdown(
                                                                    id='dropdown_yr',
                                                                    options=[{'label':name, 'value':name} for name in val_typ],
                                                                    value = list(val_typ.keys())[0],
                                                                    multi=False,
                                                                    searchable=True,
                                                                    clearable=False,
                                                               ),
                                                        ], className='custom-dropdown-div',),
                                                    html.Div([
                                                       dcc.Dropdown(
                                                                    id='dropdown_yr_sub',
                                                                    multi=False,
                                                                    searchable=True,
                                                                    clearable=False,
                                                               ),
                                                        ], className='custom-dropdown-div',),
                                                    html.P('           ', style={'font-size': '1.1rem', 'color':'#ffffff'}),
                                                    html.P('For 3 years', style={'font-size': '1.1rem', 'color':'#ffffff'}),
                                                ], className='four columns', style={'backgroundColor': '#004aad', 'padding':5, 'border-radius': 10, 'height':"100%"}),
                                                html.Div(['   '], style={'padding':5}),
                                                html.Div([
                                                    dcc.Graph(id='pie_yr', style={'height':150}),
                                                ], className='eight columns', style={'backgroundColor': '#01429e', 'padding':0, 'border-radius': 10, 'margin-left':2}),
                                            ], className='two columns', style={'backgroundColor': '#01429e', 'padding':0, 'border-radius': 10, 'margin-left':20}),
                                            html.Div([html.Br(),],className="eleven columns"),
                                           
                                           # Second Row
                                           html.Div([
                                               html.Div([
                                                   # Groupby Age
                                                   html.Div([html.H6('Age classifying ')], className='three columns'),
                                                   html.Div([
                                                       dcc.Dropdown(
                                                                    id='dropdown_age',
                                                                    options=[{'label':name, 'value':name} for name in val_typ],
                                                                    value = list(val_typ.keys())[0],
                                                                    multi=False,
                                                                    searchable=True,
                                                                    clearable=False,
                                                               )
                                                       ], className='three columns'),
                                                   html.Div([
                                                       dcc.Dropdown(
                                                                    id='dropdown_age_sub',
                                                                    multi=False,
                                                                    searchable=True,
                                                                    clearable=False,
                                                               )
                                                       ], className='three columns'),
                                                   html.Div([
                                                        dcc.Graph(id='line_age'),
                                                   ], className='twelve columns'),
                                               ], className='seven columns', style={'backgroundColor': '#01429e', 'padding':5, 'border-radius': 10, 'margin-left':20}),
                                               html.Div([
                                                   # Text Information
                                                   html.Div([html.Br(),],className="eleven columns", style={'padding':5}),
                                                   html.Div([html.Br(),],className="eleven columns", style={'padding':5}),
                                                   html.Div([
                                                       html.H5('Max. value'),
                                                       html.Div(id='max_age'),
                                                       html.Div(id='max_val'),
                                                   ], className='six columns', style={'backgroundColor': '#309ef5', 'padding':5, 'border-radius': 5, 'margin-left':0}),
                                                   html.Div([
                                                       html.H5('Min. value'),
                                                       html.Div(id='min_age'),
                                                       html.Div(id='min_val'),
                                                   ], className='six columns', style={'backgroundColor': '#f36279', 'padding':5, 'border-radius': 5, 'margin-left':5}),
                                                   html.Div([html.Br(),],className="eleven columns", style={'padding':5}),
                                                   html.Div([
                                                       html.H5('Repeated value'),
                                                       html.Div(id='mode_age'),
                                                       html.Div(id='mode_val'),
                                                   ], className='six columns', style={'backgroundColor': '#fe9077', 'padding':5, 'border-radius': 5, 'margin-left':0}),
                                                   html.Div([
                                                       html.H5('Standard deviation'),
                                                       html.Div(id='std_age'),
                                                       html.Div(id='std_val'),
                                                   ], className='six columns', style={'backgroundColor': '#ba6ff0', 'padding':5, 'border-radius': 5, 'margin-left':5}),
                                               ], className='four columns', style={'backgroundColor': '#01429e', 'padding':5, 'border-radius': 10, 'margin-left':20}),
                                           ], className='seven columns', style={'backgroundColor': '#01429e', 'padding':0, 'border-radius': 10, 'margin-left':20}),
                                           # Multivariate Analysis
                                           html.Div([
                                               html.Div([
                                                   html.H6('Multvariate Analysis'),
                                                   dcc.Dropdown(
                                                        id='dropdown_var1',
                                                        options=[{'label':demog[i], 'value':demog[i]} for i in range(len(demog))],
                                                        value=[demog[0]],
                                                        multi=True,
                                                        searchable=True,
                                                        clearable=False
                                                   ),
                                                   dcc.Dropdown(
                                                        id='dropdown_var2',
                                                        options=[{'label':i, 'value':i} for i in df.iloc[:,9:-2]],
                                                        value='MntWines',
                                                        multi=False,
                                                        searchable=True,
                                                        clearable=False
                                                   ),
                                               ], className='three columns',style={'backgroundColor': '#004aad', 'padding':5, 'border-radius': 10, 'margin-left':0, 'margin-top':0}),
                                               html.Div(['   '], style={'padding':50.5}),
                                               html.Div(
                                                   dcc.Graph(id='sun_multi', style={'height':400})
                                               ),
                                           ], className='four columns', style={'backgroundColor': '#01429e', 'padding':0, 'border-radius': 10, 'margin-left':20}),
                                           html.Div([html.Br(),],className="eleven columns", style={'padding':5}),
                                           
                                           # Third Row
                                           html.Div([
                                               html.Div([
                                                   html.H6('Multvariate Analysis'),
                                                   dcc.Dropdown(
                                                        id='dropdown_var11',
                                                        options=[{'label':demog[i], 'value':demog[i]} for i in range(len(demog))],
                                                        value=demog[0],
                                                        multi=False,
                                                        searchable=True,
                                                        clearable=False
                                                   ),
                                                   dcc.Dropdown(
                                                        id='dropdown_var12',
                                                        options=[
                                                            {'label':'Total spent', 'value':'Total_amount_spent'},
                                                            {'label':'Tptal campaign', 'value':'Total_campaign'},
                                                            {'label':'Total purchases', 'value':'Total_Purchases'},
                                                            {'label':'Complain', 'value':'Complain'},
                                                        ],
                                                        value='Total_amount_spent',
                                                        multi=False,
                                                        searchable=True,
                                                        clearable=False
                                                   ),
                                                    html.P('           ', style={'font-size': '1.6rem', 'color':'#ffffff'}),
                                                    html.P('The relation between the different demographic characters with the total number of products spent amounts, accepted campaigns, deals purchased and complains', style={'font-size': '1.6rem', 'color':'#ffffff'}),
                                               ], className='three columns',style={'backgroundColor': '#004aad', 'padding':5, 'border-radius': 10, 'margin-left':0, 'margin-top':0}),
                                              html.Div([
                                                  dcc.Graph(id='hist_tot', style={'height':320}),
                                              ], className='eight columns', style={'backgroundColor': '#01429e', 'padding':0, 'border-radius': 10, 'margin-left':10}), 
                                           ], className='five columns', style={'backgroundColor': '#01429e', 'padding':0, 'border-radius': 10, 'margin-left':20}),
                                           html.Div([
                                               html.Div([
                                                   html.H6('Multvariate Analysis'),
                                                   dcc.Dropdown(
                                                        id='dropdown_var21',
                                                        options=[{'label':demog[i], 'value':demog[i]} for i in range(len(demog))],
                                                        value=demog[0],
                                                        multi=False,
                                                        searchable=True,
                                                        clearable=False
                                                   ),
                                                   dcc.Dropdown(
                                                        id='dropdown_var22',
                                                        options=[
                                                            {'label':'Total spent', 'value':'Total_amount_spent'},
                                                            {'label':'Tptal campaign', 'value':'Total_campaign'},
                                                            {'label':'Total purchases', 'value':'Total_Purchases'},
                                                            {'label':'Complain', 'value':'Complain'},
                                                        ],
                                                        value='Total_amount_spent',
                                                        multi=False,
                                                        searchable=True,
                                                        clearable=False
                                                   ),
                                                    html.P('           ', style={'font-size': '1.6rem', 'color':'#ffffff'}),
                                                    html.P('The relation between the demographic characters with the total number of products spent amounts, accepted campaigns, deals purchased and complains ', style={'font-size': '1.6rem', 'color':'#ffffff'}),
                                               ], className='three columns',style={'backgroundColor': '#004aad', 'padding':5, 'border-radius': 10, 'margin-left':0, 'margin-top':0}),
                                              html.Div([
                                                  dcc.Graph(id='line_tot', style={'height':320}),
                                              ], className='eight columns', style={'backgroundColor': '#01429e', 'padding':0, 'border-radius': 10, 'margin-left':10}), 

                                           ], className='five columns', style={'backgroundColor': '#01429e', 'padding':0, 'border-radius': 10, 'margin-left':20}),
                                           html.Div([html.Br(),],className="eleven columns", style={'padding':5}),
                                        ], className="twelve columns", style={'backgroundColor': '#00307c', 'width':'calc(100% + 20px)', 'height':'100%', 'margin-left':-10, 'margin-right':0})
                                   ],
                               ),
                           ],
                       ),
               ])

@app.callback(
    Output('pie_typ', 'figure'),
    Input('dropdown_typ', 'value'),
    )
def type_pie(value):
    df_chn = pd.DataFrame(df[val_typ[value]].sum(axis=0))
    df_chn.reset_index(inplace=True)
    df_chn = df_chn.rename(columns = {'index':'Channels', 0:'Amount'})
    fig = px.pie(df_chn,names='Channels', values='Amount', hole=.5)
    fig.update_layout({'font_color':"white", 'paper_bgcolor': 'rgba(0, 0, 0, 0)'},  margin=dict(l=2, r=2, t=2, b=2))
    fig.update_layout(showlegend=False, font_size=8, height=150)
    return fig

@app.callback(
    Output('pie_spt', 'figure'),
    Input('dropdown_spt', 'value'),
    )
def spt_pie(value1):
    val_avg = df[df['Dt_Customer'].dt.year>df['Dt_Customer'].dt.year.max()-2][value1].mean()
    df['spt_avg'] = np.where(df[value1] > val_avg, 'Above average', 'Below average')
    fig = px.pie(df,names='spt_avg', hole=.5)
    fig.update_layout({'font_color':"white", 'paper_bgcolor': 'rgba(0, 0, 0, 0)'},  margin=dict(l=2, r=2, t=2, b=2))
    fig.update_layout(showlegend=False, font_size=8, height=150)
    return fig

@app.callback(
    Output('pie_prc', 'figure'),
    Input('dropdown_prc', 'value'),
    )
def prc_pie(value1):
    val_avg = df[df['Dt_Customer'].dt.year>df['Dt_Customer'].dt.year.max()-2][value1].mean()
    df['prc_avg'] = np.where(df[value1] > val_avg, 'Above average', 'Below average')
    fig = px.pie(df,names='prc_avg', hole=.5)
    fig.update_layout({'font_color':"white", 'paper_bgcolor': 'rgba(0, 0, 0, 0)'},  margin=dict(l=2, r=2, t=2, b=2))
    fig.update_layout(showlegend=False, font_size=8, height=150)
    return fig

@app.callback(
    Output('pie_cmp', 'figure'),
    Input('dropdown_cmp', 'value'),
    )
def cmp_pie(value1):
    val_avg = df[df['Dt_Customer'].dt.year>df['Dt_Customer'].dt.year.max()-2][value1].mean()
    df['cmp_avg'] = np.where(df[value1] > val_avg, 'Above average', 'Below average')
    fig = px.pie(df,names='cmp_avg', hole=.5)
    fig.update_layout({'font_color':"white", 'paper_bgcolor': 'rgba(0, 0, 0, 0)'},  margin=dict(l=2, r=2, t=2, b=2))
    fig.update_layout(showlegend=False, font_size=8, height=150)
    return fig

@app.callback(
    Output('dropdown_yr_sub', 'options'),
    Input('dropdown_yr', 'value'),
    )
def yr_sub(value):
    return [{'label': i, 'value': i} for i in val_typ[value]]

@app.callback(
    dash.dependencies.Output('dropdown_yr_sub', 'value'),
    [dash.dependencies.Input('dropdown_yr_sub', 'options')])
def set_yr_value(available_options):
    return available_options[0]['value']

@app.callback(
    Output('pie_yr', 'figure'),
    Input('dropdown_yr', 'value'),
    Input('dropdown_yr_sub', 'value'),
    )
def yr_pie(val1, val2):
    val_yr = df['Dt_Customer'].dt.year
    fig = px.pie(df,names= val_yr, values=val2, hole=.5)
    fig.update_layout({'font_color':"white", 'paper_bgcolor': 'rgba(0, 0, 0, 0)'},  margin=dict(l=2, r=2, t=2, b=2))
    fig.update_layout(showlegend=False, font_size=8, height=150)
    return fig

@app.callback(
    Output('dropdown_age_sub', 'options'),
    Input('dropdown_age', 'value'),
    )
def age_sub(value):
    return [{'label': i, 'value': i} for i in val_typ[value]]

@app.callback(
    dash.dependencies.Output('dropdown_age_sub', 'value'),
    [dash.dependencies.Input('dropdown_age_sub', 'options')])
def set_age_value(available_options):
    return available_options[0]['value']

@app.callback(
    Output('line_age', 'figure'),
    Input('dropdown_age', 'value'),
    Input('dropdown_age_sub', 'value'),
    )
def age_line(val1, val2):
    df_prd = df.groupby(['Age'], as_index=False)[val_typ[val1]].agg(sum)
    fig = px.line(df_prd, x="Age", y= val2, markers=True, color_discrete_sequence=['indianred'])
    fig.update_layout({'font_color':"white", 'paper_bgcolor': 'rgba(0, 0, 0, 0)'},  margin=dict(l=2, r=2, t=2, b=2))
    fig.update_layout(legend=dict(yanchor="top", xanchor="right", font_color="black", bgcolor="white"), yaxis_title=None)
    return fig

@app.callback(
    Output('max_age', 'children'),
    Output('max_val', 'children'),
    Output('min_age', 'children'),
    Output('min_val', 'children'),
    Output('mode_age', 'children'),
    Output('mode_val', 'children'),
    Output('std_age', 'children'),
    Output('std_val', 'children'),
    Input('dropdown_age', 'value'),
    Input('dropdown_age_sub', 'value'),
    )
def age_det(val1, val2):
    df_prd = df.groupby(['Age'], as_index=False)[val_typ[val1]].agg(sum)
    var1 = df_prd[val2].max()
    var2 = df_prd[df_prd[val2]==var1].iloc[0]['Age']
    var3 = df_prd[val2].min()
    var4 = df_prd[df_prd[val2]==var3].iloc[0]['Age']
    var5 = df['Age'].mode()[0]
    var6 = df[val2].mode()[0]
    var7 = np.round(df['Age'].std(), 2)
    var8 = np.round(df[val2].std(), 2)
    return html.H6('Age: '+str(var2)), html.H6('Value: '+str(var1)), html.H6('Age: '+str(var4)), html.H6('Value: '+str(var3)), html.H6('Age: '+str(var5)), html.H6('Value: '+str(var6)), html.H6('Age: '+str(var7)), html.H6('Value: '+str(var8))

@app.callback(
    Output('sun_multi', 'figure'),
    Input('dropdown_var1', 'value'),
    Input('dropdown_var2', 'value'),
    )
def multi_sun(value1, value2):
    df_cat = df.groupby(value1, as_index=False)[value2].agg(np.mean)
    fig = px.sunburst(data_frame=df_cat, path=(value1), values=value2)
    fig.update_traces(textinfo='label+percent root')
    fig.update_layout({'paper_bgcolor': 'rgba(0, 0, 0, 0)'},  margin=dict(l=120, r=2, t=2, b=2))
    fig.update_layout(showlegend=False, font_size=12, height=400)
    return fig

@app.callback(
    Output('hist_tot', 'figure'),
    Input('dropdown_var11', 'value'),
    Input('dropdown_var12', 'value'),
    )
def multi_hist(value1, value2):
    df_cam = df.groupby([value1], as_index=False)[value2].agg(np.mean)
    fig = px.bar(df_cam, x=value1, y=value2, color_discrete_sequence=['indianred'])
    fig.update_layout({'paper_bgcolor': 'rgba(0, 0, 0, 0)', 'font_color':'white'},  margin=dict(l=2, r=2, t=2, b=2))
    fig.update_layout(yaxis_title=None, xaxis_title=None, height=320)
    return fig

@app.callback(
    Output('line_tot', 'figure'),
    Input('dropdown_var21', 'value'),
    Input('dropdown_var22', 'value'),
    )
def multi_line(value1, value2):
    df_cam = df.groupby([value1, 'Enrol_years'], as_index=False)[value2].agg(np.mean)
    fig = px.line(df_cam, x=value1, y= value2, color='Enrol_years', markers=True)
    fig.update_layout({'paper_bgcolor': 'rgba(0, 0, 0, 0)', 'font_color':'white'},  margin=dict(l=2, r=2, t=2, b=2))
    fig.update_layout(legend=dict(yanchor="top", xanchor="right", font_color="black", bgcolor="white"))
    fig.update_layout(yaxis_title=None, xaxis_title=None, height=320)
    return fig

@app.callback(
    Output('div_uni', 'children'),
    Output('div_mst', 'children'),
    Output('div_frq', 'children'),
    Output('div_tot', 'children'),
    Input('dropdown_dem', 'value'),
    )
def inf_div(value):
    var1 = df[value].nunique()
    var2 = df[value].mode()[0]
    var3 = df[value].value_counts().max()
    var4 = df[value].count()
    return html.H4(var1, style={'color':'#309ef5'}), html.H4(var2, style={'color':'#f36279'}), html.H4(var3, style={'color':'#fe9077'}), html.H4(var4, style={'color':'#ba6ff0'})

@app.callback(
    Output('div_tbl', 'children'),
    Input('dropdown_dem', 'value'),
    Input('dropdown_elm', 'value'),
    )
def tbl_div(value1, value2):
    df_elm = pd.DataFrame(df.groupby([value1], as_index=False)[val_typ[value2]].agg(np.mean).round(2))
    mycolumns = [{"name": i, "id": i} for i in df_elm.columns]
    return html.Div([
            dash_table.DataTable(
            id='table',
            columns=mycolumns,
            data=df_elm.to_dict("records"),
            editable=True,
            style_cell=({'textAlign': 'left'}),
            style_header=({'backgroundColor': '#3d7dca', 'color': 'white', 'font-size': '1.6rem', 'font-weight': 'Bold'}),
            style_data=({'backgroundColor': '#004aad', 'color': 'white', 'font-size': '1.6rem'}),
         )
        ]),

@app.callback(
    Output('div_tbl_cat', 'children'),
    Input('dropdown_cat', 'value'),
    )
def tbl_cat(value):
    lst_val = []
    x=0
    df_cat = pd.DataFrame(columns=['Name','Above Average','Below Average'])
    for i in val_typ[value]:
        val_avg = df[df['Dt_Customer'].dt.year>df['Dt_Customer'].dt.year.max()-2][i].mean()
        lst_val =np.where(df[i] >= val_avg, 'Above avg', 'Below avg')
        unique, counts = np.unique(lst_val, return_counts=True)
        dct_val = dict(zip(unique, counts))
        df_cat.loc[x,:]=[i,dct_val['Above avg'],dct_val['Below avg']]
        x+=1
    mycolumns = [{"name": i, "id": i} for i in df_cat.columns]
    return html.Div([
            dash_table.DataTable(
            id='table_cat',
            columns=mycolumns,
            data=df_cat.to_dict("records"),
            editable=True,
            style_cell=({'textAlign': 'left'}),
            style_header=({'backgroundColor': '#3d7dca', 'color': 'white', 'font-size': '1.6rem', 'font-weight': 'Bold'}),
            style_data=({'backgroundColor': '#004aad', 'color': 'white', 'font-size': '1.6rem'}),
         )
        ]),

@app.callback(
    Output('heat_cor', 'figure'),
    Input('radio_cor', 'value'),
    )
def cor_heat(value):
    x = cust_df if value == 0 else all_df
    df_new = pd.DataFrame(df[x])
    cor_mat = corr_matrix = df_new.corr()
    mask = np.triu(np.ones_like(cor_mat, dtype=bool))
    rLT = cor_mat.mask(mask)
    heat = go.Heatmap(
        z = rLT,
        x = rLT.columns.values,
        y = rLT.columns.values,
        zmin = - 0.25, # Sets the lower bound of the color domain
        zmax = 1,
        xgap = 1, # Sets the horizontal gap (in pixels) between bricks
        ygap = 1,
        colorscale = 'RdBu'
    )
    layout = go.Layout(
        title_x=0.5, 
        height=500,
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        yaxis_autorange='reversed'
    )
    fig = go.Figure(data=[heat], layout=layout)
    fig.update_layout({'paper_bgcolor': 'rgba(0, 0, 0, 0)', 'font_color':'white'},  margin=dict(l=2, r=2, t=2, b=2))
    return fig

@app.callback(
    Output('div_email', 'children'),
    Input('dropdown_dem', 'value'),
    Input('submit-val', 'n_clicks'),
    )
def inf_div(value1, value2):
    if value2 > 0:
        var1 = df[value1].nunique()
        var2 = df[value1].mode()[0]
        var3 = df[value1].value_counts().max()
        var4 = df[value1].count()
        cont = 'The average ' + str(value1) + ' of customers are ' + str(var2) + ' that repeated with ' + str(var3) + ' times.'
        mail_content = '''Hello,
        This is a simple mail. There is only text, no attachments are there The mail is sent using Python SMTP library.
        '''
        mail_content += cont
        mail_content += '''
        Thank You
        Mona Maze
        '''
        #The mail addresses and password
        sender_address = 'nutskataketo@gmail.com'
        sender_pass = 'tjrjvfilyzaitcew'
        receiver_address = 'nutskataketo@gmail.com'
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Marketing Data Analysis mail sent by Python'   #The subject line
        #The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'plain'))
        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_address, sender_pass) #login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        msg = html.H6('Email sent')
    else:
        msg = html.H6('   ')
    return msg

if __name__ == '__main__':
    app.run_server()
