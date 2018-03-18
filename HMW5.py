import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go
import quandl

from HMW3_graphs import figure
from HMW3_graphs import figure1
from HMW3_graphs import figure4

quandl.ApiConfig.api_key = "WLod4FCtLHjeK8fdx3qR"
app = dash.Dash()
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

googl_df = quandl.get("WIKI/GOOGL")
ibm_df = quandl.get("WIKI/IBM")
aapl_df = quandl.get("WIKI/AAPL")
amzn_df = quandl.get("WIKI/AMZN")
msft_df = quandl.get("WIKI/MSFT")

gdp_df = quandl.get("FRED/GDP")
churnGraph = dcc.Graph(id="churn", figure=figure)
mapGraph = dcc.Graph(id="roadmap", figure=figure4)

app.layout = html.Div([
	html.Div([
            html.H1("Homework 5")],
            style={
            'textAlign': 'center',
            'color': '#C70039',
            'font-family':'courier'
        		}
            ),
	html.Div([
        html.Div([dcc.RadioItems(
            id = 'rbutton',
            options=[
                {'label': 'Employee Churn', 'value': 'churn'},
                {'label': 'Startup RoadMap', 'value': 'map'}
                ],
            ),
        ], className='three columns'),
       
        html.Div([], id = 'graph_div1',className='nine columns')
    ],
    className='row'),

    html.Div([
        html.Div([
           dcc.Dropdown(
            id = 'dd_in',
            options=[   
                {'label': 'Google', 'value': 'google_price'},
                {'label': 'IBM', 'value': 'ibm_price'},
                {'label': 'Apple', 'value': 'apple_price'},
                {'label': 'Amazon', 'value': 'amzn_price'},
                {'label': 'Microsoft', 'value': 'msft_price'}
            ],
            multi=True,
            placeholder="Please, select a stock")] , className = 'two columns'),
        html.Div([], id = "graph_div2", className = 'ten columns')
        ],
        className='row'),
    html.Div([
    	dcc.Graph(id='graph'),
    	dcc.RangeSlider(
    		id = 'rslider',
    		min=0,
    		max=len(gdp_df.index),
    		step = 5,
    		value=[0, len(gdp_df.index)]
			),
		html.Div(id='graph_div3')
    	],
    	className='row')
	])
@app.callback(
    Output('graph_div1', 'children'),
    [Input('rbutton', 'value')],
    )
def update_graph(input):
    if input=='churn':
        return churnGraph
    elif input=='map':
        return mapGraph

@app.callback(
    Output('graph_div2', 'children'),
    [Input('dd_in', 'value')]
)
def update_graph(stocks):
	headerArray = []
	cellsArray = []
	boxData = []
	if len(stocks) > 1 and len(stocks)< 3:
		for value in stocks:
			if(value=='google_price'):
				headerArray.append('Google')
				cellsArray.append(round(googl_df.Open.pct_change()[1:5,],3))
				boxData.append(go.Box(x=googl_df.Open.pct_change(), name = 'Google'))
			elif(value=='ibm_price'):
				headerArray.append('IBM')
				cellsArray.append(round(ibm_df.Open.pct_change()[1:5,],3))
				boxData.append(go.Box(x=ibm_df.Open.pct_change(), name = 'IBM'))
			elif(value=='apple_price'):
				headerArray.append('Apple')
				cellsArray.append(round(aapl_df.Open.pct_change()[1:5,],3))
				boxData.append(go.Box(x=aapl_df.Open.pct_change(), name = 'Apple'))
			elif(value=='amzn_price'):
				headerArray.append('Amazon')
				cellsArray.append(round(amzn_df.Open.pct_change()[1:5,],3))
				boxData.append(go.Box(x=amzn_df.Open.pct_change(), name = 'Amazon'))
			elif(value=='msft_price'):
				headerArray.append('Microsoft')
				cellsArray.append(round(msft_df.Open.pct_change()[1:5,],3))
				boxData.append(go.Box(x=msft_df.Open.pct_change(), name = 'Microsoft'))
		
		parentDiv = html.Div([
            html.Div([
                getBox(boxData)
                ], className = 'six columns'),
            html.Div([
                getTable(headerArray, cellsArray)
                ], className = 'four columns')
            ],
            className='row')
		return parentDiv
	else: return  'Choose only 2 stocks.'

def getBox(boxData):
    boxLayout = dict(title = 'Distribution of Stock Prices')
    boxFigure = dict(data=boxData, layout=boxLayout)
    box = dcc.Graph(id="box", figure=boxFigure)
    return box

def getTable(headerArray, cellsArray):
	header = dict(values = headerArray,
			fill = dict(color='#119DFF')
            )
	cells = dict(values = cellsArray,
			fill = dict(color = ["yellow","white"])
            )
	traceTable = go.Table(header = header, cells=cells)
	dataTable = [traceTable]
	layoutTable = dict(width=500, height=300)
	figureTable = dict(data=dataTable, layout=layoutTable)
	table = dcc.Graph(id="stock_prices", figure=figureTable)
	return table

@app.callback(
    Output('graph', 'figure'),
    [Input('rslider', 'value')]
)
def update_graph(input_value):
	transformed_index = gdp_df.index[input_value[0]:input_value[1]]
	transformed_values = gdp_df.Value[input_value[0]:input_value[1]]

	sliderData = [go.Scatter(x=transformed_index,y=transformed_values,fill="tozeroy")]
	sliderLayout = dict(title = 'US GDP over time')
	sliderFigure = dict(data=sliderData, layout = sliderLayout)
	return sliderFigure

if __name__ == '__main__':
    app.run_server()

