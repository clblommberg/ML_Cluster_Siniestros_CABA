import dash_ag_grid as dag
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])


equities = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "AMZN": "Amazon",
    "GOOGL": "Alphabet",
    "TSLA": "Tesla",
    "BRK-B": "Berkshire Hathaway",
    "UNH": "United Health Group",
    "JNJ": "Johnson & Johnson",
}


def get_stock_data():
    return yf.download(tickers=list(equities.keys()), period="2y", group_by="ticker")


stock_data = get_stock_data()


def last_close(ticker):
    return stock_data[ticker]["Close"].iloc[-1]

stock_data.to_csv("data.csv") 

data = {
    "ticker": [ticker for ticker in equities],
    "company": [name for name in equities.values()],
    "quantity": [75, 40, 100, 50, 40, 60, 20, 40],
    "price": [last_close(ticker) for ticker in equities],
    "position": ["buy", "sell", "hold", "hold", "hold", "hold", "hold", "hold"],
    "comments": ["Notes" for i in range(8)],
}
df = pd.DataFrame(data)
df.to_csv("data.csv")
columnDefs = [
    {
        "headerName": "Stock Ticker",
        "field": "ticker",
    },
    {
        "headerName": "Company",
        "field": "company",
    },
    {
        "headerName": "Shares",
        "field": "quantity",
        "type": "rightAligned",
        "filter": "agNumberColumnFilter",
        "editable": True,
    },
    {
        "headerName": "Last Close Price",
        "field": "price",
        "type": "rightAligned",
        "filter": "agNumberColumnFilter",
        "valueFormatter": {"function": "d3.format('$,.2f')(params.value)"},
        "cellRenderer": "agAnimateShowChangeCellRenderer",
    },
    {
        "headerName": "Market Value",
        "type": "rightAligned",
        "filter": "agNumberColumnFilter",
        "valueGetter": {"function": "Number(params.data.price) * Number(params.data.quantity)"},
        "valueFormatter": {"function": "d3.format('$,.2f')(params.value)"},
        "cellRenderer": "agAnimateShowChangeCellRenderer",
    },
    {
        "headerName": "Position",
        "field": "position",
        "editable": True,
        "cellEditor": "agSelectCellEditor",
        "cellEditorParams": {
            "values": ["buy", "sell", "hold"],
        },
    },
    {
        "headerName": "Comments",
        "field": "comments",
        "editable": True,
        "cellEditorPopup": True,
        "cellEditor": "agLargeTextCellEditor",
    },
]

cellStyle = {
    "styleConditions": [
        {
            "condition": "params.value == 'buy'",
            "style": {"backgroundColor": "#196A4E", "color": "white"},
        },
        {
            "condition": "params.value == 'sell'",
            "style": {"backgroundColor": "#800000", "color": "white"},
        },
        {
            "condition": "params.colDef.headerName == 'Shares'",
            "style": {"backgroundColor": "#444"},
        },
    ]
}

defaultColDef = {
    "filter": True,
    "resizable": True,
    "sortable": True,
    "editable": False,
    "floatingFilter": True,
    "minWidth": 125,
    "cellStyle": cellStyle,
}


grid = dag.AgGrid(
    id="portfolio-grid",
    className="ag-theme-alpine-dark",
    columnDefs=columnDefs,
    rowData=df.to_dict("records"),
    columnSize="sizeToFit",
    defaultColDef=defaultColDef,
    dashGridOptions={"undoRedoCellEditing": True, "rowSelection": "single"},
)

candlestick = dbc.Card(dcc.Graph(id="candlestick"), body=True)
pie = dbc.Card(dcc.Graph(id="asset-allocation"), body=True)
header = html.Div("My Portfolio", className="h2 p-2 text-white bg-primary text-center")

candlestick = dbc.Card(dcc.Graph(id="candlestick"), body=True)
pie = dbc.Card(dcc.Graph(id="asset-allocation"), body=True)
header = html.Div("My Portfolio", className="h2 p-2 text-white bg-primary text-center")

app.layout = dbc.Container(
    [
        header,
        dbc.Row([dbc.Col(candlestick), dbc.Col(pie)]),
        dbc.Row(dbc.Col(grid, className="py-4")),
    ],
)


@app.callback(
    Output("candlestick", "figure"),
    Input("portfolio-grid", "selectedRows"),
)

def update_candlestick(selected_row):
    if selected_row is None:
        ticker = "AAPL"
        company = "Apple"
    else:
        ticker = selected_row[0]["ticker"]
        company = selected_row[0]["company"]

    dff_ticker_hist = stock_data[ticker].reset_index()
    dff_ticker_hist["Date"] = pd.to_datetime(dff_ticker_hist["Date"])

    fig = go.Figure(
        go.Candlestick(
            x=dff_ticker_hist["Date"],
            open=dff_ticker_hist["Open"],
            high=dff_ticker_hist["High"],
            low=dff_ticker_hist["Low"],
            close=dff_ticker_hist["Close"],
        )
    )
    fig.update_layout(
        title_text=f"{ticker} {company} Daily Price", template="plotly_dark"
    )
    return fig

@app.callback(
    Output("asset-allocation", "figure"),
    Input("portfolio-grid", "cellValueChanged"),
    State("portfolio-grid", "rowData"),
)
def update_portfolio_stats(_, data):
    dff = pd.DataFrame(data)
    dff["total"] = dff["quantity"].astype(float) * dff["price"].astype(float)
    portfolio_total = dff["total"].sum()

    return px.pie(
        dff,
        values="total",
        names="ticker",
        hole=0.3,
        title=f"Portfolio Total ${portfolio_total:,.2f}",
        template="plotly_dark",
    )


if __name__ == "__main__":
    app.run_server(debug=True, port=8060)





#################################################
import dash_ag_grid as dag
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
df = pd.read_csv('../datasets/processed/homicidios_lm.csv', sep=',',index_col='Unnamed: 0', encoding='utf-8')

# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 696 entries, 0 to 695
# Data columns (total 18 columns):
#  #   Column                 Non-Null Count  Dtype         
# ---  ------                 --------------  -----         
#  0   id                     696 non-null    object        
#  1   n_victimas             696 non-null    int64         
#  2   lugar_del_hecho        696 non-null    object        
#  3   tipo_de_calle          696 non-null    object        
#  4   direccion_normalizada  696 non-null    object        
#  5   comuna                 696 non-null    int64         
#  6   pos_x                  684 non-null    float64       
#  7   pos_y                  684 non-null    float64       
#  8   acusado                696 non-null    object        
#  9   anio                   696 non-null    int32         
#  10  mes                    696 non-null    int32         
#  11  dia                    696 non-null    int32         
#  12  fecha_hora             696 non-null    datetime64[ns]
#  13  fecha_formato          696 non-null    object        
#  14  hora_formato           696 non-null    object        
#  15  hora_i                 696 non-null    int32         
#  16  coordenada_x           682 non-null    float64       
#  17  coordenada_y           682 non-null    float64       
# dtypes: datetime64[ns](1), float64(4), int32(4), int64(2), object(7)
# memory usage: 87.1+ KB

# Crear la aplicación Dash

# Definir el diseño de la aplicación
app.layout = html.Div(children=[
    html.H1(children='Gráficos de Caja'),

    dcc.Graph(
        id='boxplot-n-victimas',
        figure={
            'data': [
                go.Box(y=df['n_victimas'], name='Número de Víctimas', marker_color="#FA8072")
            ],
            'layout': go.Layout(
                title='Número de Víctimas',
                yaxis=dict(title='Número de Víctimas')
            )
        }
    ),

    dcc.Graph(
        id='boxplot-anio',
        figure={
            'data': [
                go.Box(y=df['anio'], name='Años', marker_color="#F4A460")
            ],
            'layout': go.Layout(
                title='Años',
                yaxis=dict(title='Años')
            )
        }
    ),

    dcc.Graph(
        id='boxplot-mes',
        figure={
            'data': [
                go.Box(y=df['mes'], name='Meses', marker_color="#FA8072")
            ],
            'layout': go.Layout(
                title='Meses',
                yaxis=dict(title='Meses')
            )
        }
    ),

    dcc.Graph(
        id='boxplot-dia',
        figure={
            'data': [
                go.Box(y=df['dia'], name='Días', marker_color="#6A5ACD")
            ],
            'layout': go.Layout(
                title='Días',
                yaxis=dict(title='Días')
            )
        }
    ),

    dcc.Graph(
        id='boxplot-hora-i',
        figure={
            'data': [
                go.Box(y=df['hora_i'], name='Horas', marker_color="#87CEEB")
            ],
            'layout': go.Layout(
                title='Horas',
                yaxis=dict(title='Horas')
            )
        }
    ),

    dcc.Graph(
        id='boxplot-comuna',
        figure={
            'data': [
                go.Box(y=df['comuna'], name='Comunas', marker_color="#87CEEB")
            ],
            'layout': go.Layout(
                title='Comunas',
                yaxis=dict(title='Comunas')
            )
        }
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8060)



#############################
    import dash_ag_grid as dag
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
df = pd.read_csv('../datasets/processed/homicidios_lm.csv', sep=',',index_col='Unnamed: 0', encoding='utf-8')

# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 696 entries, 0 to 695
# Data columns (total 18 columns):
#  #   Column                 Non-Null Count  Dtype         
# ---  ------                 --------------  -----         
#  0   id                     696 non-null    object        
#  1   n_victimas             696 non-null    int64         
#  2   lugar_del_hecho        696 non-null    object        
#  3   tipo_de_calle          696 non-null    object        
#  4   direccion_normalizada  696 non-null    object        
#  5   comuna                 696 non-null    int64         
#  6   pos_x                  684 non-null    float64       
#  7   pos_y                  684 non-null    float64       
#  8   acusado                696 non-null    object        
#  9   anio                   696 non-null    int32         
#  10  mes                    696 non-null    int32         
#  11  dia                    696 non-null    int32         
#  12  fecha_hora             696 non-null    datetime64[ns]
#  13  fecha_formato          696 non-null    object        
#  14  hora_formato           696 non-null    object        
#  15  hora_i                 696 non-null    int32         
#  16  coordenada_x           682 non-null    float64       
#  17  coordenada_y           682 non-null    float64       
# dtypes: datetime64[ns](1), float64(4), int32(4), int64(2), object(7)
# memory usage: 87.1+ KB

# Crear la aplicación Dash
# Obtener nombres de columnas numéricas

data = df[["id", "n_victimas","acusado","anio", "mes", "dia"]].copy()
# columnas_numericas = df.select_dtypes(include=['int64','int32']).columns




#'AUTO', 'PASAJEROS', 'SNR', 'OBJETO FIJO', 'CARGAS', 'MOTO','MULTIPLE', 'OTRO', 'BICICLETA', 'TREN'
columnDefs = [
    {
        "headerName": "Id Sinisestro",
        "field": "id",
    },
    {
        "headerName": "Q Victimas",
        "field": "n_victimas",
    },
    {
        "headerName": "Acusado",
        "field": "acusado",
        "editable": True,
        "cellEditor": "agSelectCellEditor",
        "cellEditorParams": {
            "values": ['AUTO', 'PASAJEROS', 'SNR', 'OBJETO FIJO', 'CARGAS', 'MOTO','MULTIPLE', 'OTRO', 'BICICLETA', 'TREN'],
        },
    },
    {
        "headerName": "Anio",
        "field": "anio",
        "type": "rightAligned",
        "filter": "agNumberColumnFilter",
        "editable": True,
    },
    {
        "headerName": "Mes",
        "field": "mes",
        "type": "rightAligned",
        "filter": "agNumberColumnFilter",
        "editable": True,
    },
    {
        "headerName": "Dia",
        "field": "dia",
        "type": "rightAligned",
        "filter": "agNumberColumnFilter",
        "editable": True,
    },
]

cellStyle = {
    "styleConditions": [
        {
            "condition": "params.value == 'AUTO'",
            "style": {"backgroundColor": "#196A4E", "color": "white"},
        },
        {
            "condition": "params.value == 'PASAJEROS'",
            "style": {"backgroundColor": "#800000", "color": "white"},
        },
        {
            "condition": "params.colDef.headerName == 'Q Victimas'",
            "style": {"backgroundColor": "#444"},
        },
    ]
}

defaultColDef = {
    "filter": True,
    "resizable": True,
    "sortable": True,
    "editable": False,
    "floatingFilter": True,
    "minWidth": 125,
    "cellStyle": cellStyle,
}


defaultColDef = {
    "filter": True,
    "resizable": True,
    "sortable": True,
    "editable": False,
    "floatingFilter": True,
    "minWidth": 125,
    "cellStyle": cellStyle,
}

grid = dag.AgGrid(
    id="portfolio-grid",
    className="ag-theme-alpine-dark",
    columnDefs=columnDefs,
    rowData=df.to_dict("records"),
    columnSize="sizeToFit",
    defaultColDef=defaultColDef,
    dashGridOptions={"undoRedoCellEditing": True, "rowSelection": "single"},
)

box_anio = dcc.Graph(
        id='boxplot-n-anio',
        figure={
            'data': [
                go.Box(y=df['anio'], name='Número de Víctimas', marker_color="#FA8072")
            ],
            'layout': go.Layout(
                title='Número de Víctimas',
                yaxis=dict(title='Número de Víctimas')
            )
        }
    )

box_mes = dcc.Graph(
        id='boxplot-n-mes',
        figure={
            'data': [
                go.Box(y=df['mes'], name='Número de Víctimas', marker_color="#FA8072")
            ],
            'layout': go.Layout(
                title='Número de Víctimas',
                yaxis=dict(title='Número de Víctimas')
            )
        }
    )

dataNumerica = data.select_dtypes(include=['number']) 
corr = dataNumerica.corr().round(2)
head_corr = dcc.Graph(
        id='heatmap-num',
        figure={
            'data': [
                go.Heatmap(corr)
            ],
            'layout': go.Layout(
                title='Número de Víctimas',
                yaxis=dict(title='Número de Víctimas')
            )
        }
    )

# # Definir el diseño de la aplicación
title = html.Div(children=[html.H1(children='Gráficos de Caja', className="text-white bg-primary text-center")])
app.layout = dbc.Container(
    [   
        title,
        #dbc.Row([dbc.Col(box_anio), dbc.Col(box_mes)]),
        #dbc.Col([box_anio,box_mes]),
        dbc.Row([dbc.Col(box_anio), dbc.Col(box_mes)]),
        dbc.Row(dbc.Col(head_corr)),
        dbc.Row(dbc.Col(grid, className="py-4")),
    ],
)


if __name__ == "__main__":
    app.run_server(debug=True, port=8060)