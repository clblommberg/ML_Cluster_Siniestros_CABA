import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_ag_grid as dag
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, html, dcc, Input, Output, State

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
# Cargar datos
df = pd.read_csv('../datasets/processed/homicidios_lm.csv', sep=',', index_col='Unnamed: 0', encoding='utf-8')

# Seleccionar columnas numéricas
data = df[["id", "n_victimas", "acusado", "anio", "mes", "dia"]].copy()

# Configurar columnDefs para ag-Grid
columnDefs = [
    {"headerName": "Id Siniestro", "field": "id"},
    {"headerName": "Q Victimas", "field": "n_victimas"},
    {"headerName": "Acusado", "field": "acusado", "editable": True, "cellEditor": "agSelectCellEditor",
     "cellEditorParams": {"values": ['AUTO', 'PASAJEROS', 'SNR', 'OBJETO FIJO', 'CARGAS', 'MOTO', 'MULTIPLE', 'OTRO', 'BICICLETA', 'TREN']}},
    {"headerName": "Anio", "field": "anio", "type": "rightAligned", "filter": "agNumberColumnFilter", "editable": True},
    {"headerName": "Mes", "field": "mes", "type": "rightAligned", "filter": "agNumberColumnFilter", "editable": True},
    {"headerName": "Dia", "field": "dia", "type": "rightAligned", "filter": "agNumberColumnFilter", "editable": True},
]

# Configurar estilo de celda para ag-Grid
cellStyle = {
    "styleConditions": [
        {"condition": "params.value == 'AUTO'", "style": {"backgroundColor": "#196A4E", "color": "white"}},
        {"condition": "params.value == 'PASAJEROS'", "style": {"backgroundColor": "#800000", "color": "white"}},
        {"condition": "params.colDef.headerName == 'Q Victimas'", "style": {"backgroundColor": "#444"}},
    ]
}

# Configurar opciones predeterminadas para ag-Grid
defaultColDef = {
    "filter": True,
    "resizable": True,
    "sortable": True,
    "editable": False,
    "floatingFilter": True,
    "minWidth": 125,
    "cellStyle": cellStyle,
}

# Crear componente ag-Grid
grid = dag.AgGrid(
    id="portfolio-grid",
    className="ag-theme-alpine-dark",
    columnDefs=columnDefs,
    rowData=data.to_dict("records"),
    columnSize="sizeToFit",
    defaultColDef=defaultColDef,
    dashGridOptions={"undoRedoCellEditing": True, "rowSelection": "single"},
)

# Crear gráficos de caja
box_anio = dcc.Graph(
    id='boxplot-n-anio',
    figure=px.box(df, y='anio', title='Distribución de Años')
)

box_mes = dcc.Graph(
    id='boxplot-n-mes',
    figure=px.box(df, y='mes', title='Distribución de Meses')
)

# Crear matriz de correlación
data_numerica = data.select_dtypes(include=['number'])
corr = data_numerica.corr().round(2)
head_corr = dcc.Graph(
    id='heatmap-num',
    figure=go.Figure(go.Heatmap(z=corr.values,
                                x=corr.columns,
                                y=corr.index,
                                colorscale='Viridis')).update_layout(
        title='Matriz de Correlación',
        yaxis=dict(title='Variables'),
        xaxis=dict(title='Variables'),
    )
)

# Definir el diseño de la aplicación
title = html.Div(children=[html.H1(children='Panel de Control', className="text-white bg-primary text-center")])

app.layout = dbc.Container(
    [
        title,
        dbc.Row([dbc.Col(box_anio), dbc.Col(box_mes)]),
        dbc.Row([dbc.Col(head_corr)]),
        dbc.Row([dbc.Col(grid, className="py-4")]),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True, port=8060)
