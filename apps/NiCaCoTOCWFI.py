import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from datetime import datetime as dt
from datetime import timedelta
from app import app
from app import conn
import plotly.io as pio



def NiCaCoTOCWFI_display():
    return html.Div(
        children=[
        html.H1(
            children="GRÁFICOS DE NIVEL, CAUDAL, CONDUCTIVIDAD Y TOC WFI", 
            style={"textAlign": "center","marginTop":"0.5em"}
        ),
        html.P(
            children=
                "Diagnóstico de la temperatura del lazo"
                " de agua WFI de la planta de"
                " inyectables", 
            style={"textAlign": "center"
            }
        ),
        dcc.DatePickerRange(
            id='my-date-picker-range-NivelWFI',  # ID to be used for callback
            calendar_orientation='horizontal',  # vertical or horizontal
            day_size=39,  # size of calendar image. Default is 39
            end_date_placeholder_text="Return",  # text that appears when no end date chosen
            with_portal=False,  # if True calendar will open in a full screen overlay portal
            first_day_of_week=1,  # Display of calendar when open (0 = Sunday)
            reopen_calendar_on_clear=True,
            is_RTL=False,  # True or False for direction of calendar
            clearable=True,  # whether or not the user can clear the dropdown
            number_of_months_shown=1,  # number of months shown when calendar is open
            min_date_allowed=dt(2021, 1, 1),  # minimum date allowed on the DatePickerRange component
            max_date_allowed=dt(2030, 1, 1),  # maximum date allowed on the DatePickerRange component
            initial_visible_month=dt.today(),  # the month initially presented when the user opens the calendar
            start_date=dt.today() - timedelta(days=7),
            end_date=dt.today(),
            display_format='DD MMM, YYYY',  # how selected dates are displayed in the DatePickerRange component.
            month_format='MMMM, YYYY',  # how calendar headers are displayed when the calendar is opened.
            minimum_nights=0,  # minimum number of days between start and end date
            updatemode='bothdates'  # singledate or bothdates. Determines when callback is triggered
        ),
        dbc.Button(
            "Descargar gráfica", 
            id="btnNivelWFI", 
            color="success", 
            style={"margin-left":"100px","scale":"1.1"}
        ), 
        dbc.Button(
            "Descargar CSV", 
            id="btnCsvNivelWFI", 
            color="warning", 
            style={
                "margin-left":"100px","scale":"1.1"}
        ), 
        dcc.Download(
            id="downloadNivelWFI"
        ),
        dcc.Loading(
            id="downloadNivelWFI", 
            color="#18bc9c", 
            style={"z-index": "1"}
        ),
        dcc.Graph(
            id='mychartNivelWFI', 
            config={"toImageButtonOptions": {
                "format":"jpeg",
                "height":1080,
                "width":1920,
                "filename":"Nivel WFI",
                "scale":3
                }
            }
        ),
        dcc.DatePickerRange(
            id='my-date-picker-range-CaudalWFI', 
            calendar_orientation='horizontal',
            day_size=39, 
            end_date_placeholder_text="Return",  # n
            with_portal=False,  # if True calendar will open in a full screen overlay portal
            first_day_of_week=1,  # Display of calendar when open (0 = Sunday)
            reopen_calendar_on_clear=True,
            is_RTL=False,  # True or False for direction of calendar
            clearable=True,  # whether or not the user can clear the dropdown
            number_of_months_shown=1,  # number of months shown when calendar is open
            min_date_allowed=dt(2021, 1, 1),  # minimum date allowed on the DatePickerRange component
            max_date_allowed=dt(2030, 1, 1),  # maximum date allowed on the DatePickerRange component
            initial_visible_month=dt.today(),  # the month initially presented when the user opens the calendar
            start_date=dt.today() - timedelta(days=7),
            end_date=dt.today(),
            display_format='DD MMM, YYYY',  # how selected dates are displayed in the DatePickerRange component.
            month_format='MMMM, YYYY',  # how calendar headers are displayed when the calendar is opened.
            minimum_nights=0,  # minimum number of days between start and end date
            updatemode='bothdates'  # singledate or bothdates. Determines when callback is triggered
        ),
        dbc.Button(
            "Descargar gráfica", 
            id="btnCaudalWFI", 
            color="success", 
            style={"margin-left":"100px","scale":"1.1"}
        ), 
        dbc.Button(
            "Descargar CSV", 
            id="btnCsvCaudalWFI", 
            color="warning", 
            style={
                "margin-left":"100px","scale":"1.1"}
        ), 
        dcc.Download(id="downloadCaudalWFI"),
        dcc.Loading(
            id="downloadCaudalWFI", 
            color="#18bc9c", 
            style={"z-index": "1"}
        ),
        dcc.Graph(
            id='mychartCaudalWFI', 
            config={"toImageButtonOptions": {
                "format":"jpeg",
                "height":1080,
                "width":1920,
                "filename":"Caudal WFI",
                "scale":3
                }
            }
        ),
        
        dcc.DatePickerRange(
            id='my-date-picker-range-ConductividadWFI',  # ID to be used for callback
            calendar_orientation='horizontal',  # vertical or horizontal
            day_size=39,  # size of calendar image. Default is 39
            end_date_placeholder_text="Return",  # text that appears when no end date chosen
            with_portal=False,  # if True calendar will open in a full screen overlay portal
            first_day_of_week=1,  # Display of calendar when open (0 = Sunday)
            reopen_calendar_on_clear=True,
            is_RTL=False,  # True or False for direction of calendar
            clearable=True,  # whether or not the user can clear the dropdown
            number_of_months_shown=1,  # number of months shown when calendar is open
            min_date_allowed=dt(2021, 1, 1),  # minimum date allowed on the DatePickerRange component
            max_date_allowed=dt(2030, 1, 1),  # maximum date allowed on the DatePickerRange component
            initial_visible_month=dt.today(),  # the month initially presented when the user opens the calendar
            start_date=dt.today() - timedelta(days=7),
            end_date=dt.today(),
            display_format='DD MMM, YYYY',  # how selected dates are displayed in the DatePickerRange component.
            month_format='MMMM, YYYY',  # how calendar headers are displayed when the calendar is opened.
            minimum_nights=0,  # minimum number of days between start and end date
            updatemode='bothdates'  # singledate or bothdates. Determines when callback is triggered
        ),
        dbc.Button(
            "Descargar gráfica", 
            id="btnConductividadWFI", 
            color="success", 
            style={"margin-left":"100px","scale":"1.1"}
        ), 
        dbc.Button(
            "Descargar CSV", 
            id="btnCsvConductividadWFI", 
            color="warning", 
            style={
                "margin-left":"100px","scale":"1.1"}
        ), 
        dcc.Download(
            id="downloadConductividadWFI"
        ),
        dcc.Loading(
            id="downloadConductividadWFI", 
            color="#18bc9c", 
            style={"z-index": "1"}
        ),
        dcc.Graph(
            id='mychartConductividadWFI', 
            config={"toImageButtonOptions": {
                "format":"jpeg",
                "height":1080,
                "width":1920,
                "filename":"Conductividad WFI",
                "scale":3
                }
            }
        ),
        
        dcc.DatePickerRange(
            id='my-date-picker-range-TOCWFI',  # ID to be used for callback
            calendar_orientation='horizontal',  # vertical or horizontal
            day_size=39,  # size of calendar image. Default is 39
            end_date_placeholder_text="Return",  # text that appears when no end date chosen
            with_portal=False,  # if True calendar will open in a full screen overlay portal
            first_day_of_week=1,  # Display of calendar when open (0 = Sunday)
            reopen_calendar_on_clear=True,
            is_RTL=False,  # True or False for direction of calendar
            clearable=True,  # whether or not the user can clear the dropdown
            number_of_months_shown=1,  # number of months shown when calendar is open
            min_date_allowed=dt(2021, 1, 1),  # minimum date allowed on the DatePickerRange component
            max_date_allowed=dt(2030, 1, 1),  # maximum date allowed on the DatePickerRange component
            initial_visible_month=dt.today(),  # the month initially presented when the user opens the calendar
            start_date=dt.today() - timedelta(days=7),
            end_date=dt.today(),
            display_format='DD MMM, YYYY',  # how selected dates are displayed in the DatePickerRange component.
            month_format='MMMM, YYYY',  # how calendar headers are displayed when the calendar is opened.
            minimum_nights=0,  # minimum number of days between start and end date
            updatemode='bothdates'  # singledate or bothdates. Determines when callback is triggered
        ),
        dbc.Button(
            "Descargar gráfica", 
            id="btnTOCWFI", 
            color="success", 
            style={"margin-left":"100px","scale":"1.1"}
        ), 
        dbc.Button(
            "Descargar CSV", 
            id="btnCsvTOCWFI", 
            color="warning", 
            style={"margin-left":"100px","scale":"1.1"}
        ), 
        dcc.Download(
            id="downloadTOCWFI"
        ),
        dcc.Loading(
            id="downloadTOCWFI", 
            color="#18bc9c", 
            style={"z-index": "1"}
        ),
        dcc.Graph(
            id='mychartTOCWFI', 
            config={"toImageButtonOptions": {
                "format":"jpeg",
                "height":1080,
                "width":1920,
                "filename":"TOC WFI",
                "scale":3
                }
            }
        ),
    ]
    )

layout = NiCaCoTOCWFI_display

# Callbacks de los botones #


### NIVEL WFI ###
@app.callback(
    Output('mychartNivelWFI', 'figure'),
    Output('downloadNivelWFI','data'),
    Input('my-date-picker-range-NivelWFI', 'start_date'),
    Input('my-date-picker-range-NivelWFI', 'end_date'),
    Input('btnNivelWFI','n_clicks'),
    Input('btnCsvNivelWFI','n_clicks')
)

def update_output(start_date,end_date, n_clicks, n_clicks2):
    query = """
        SELECT TimeString,[WFI-LT-100] 
        FROM Main 
        WHERE [WFI-LT-100] IS NOT NULL 
        AND TimeString BETWEEN ? AND ?
    """
    dff_NivelWFI = pd.read_sql_query(
        query,
        conn,
        index_col=["TimeString"],
        parse_dates=["TimeString"],
        params=[start_date,end_date]
    ) 
    
    
    figure = px.line(
        dff_NivelWFI, 
        x= dff_NivelWFI.index, 
        y= ["WFI-LT-100"],
        height=700, 
        labels={"value":"Nivel (%)",
                "TimeString":"Fecha", 
                "variable":"Sonda"
        }, 
        template= "plotly_white", 
        title= "Nivel WFI",
        color_discrete_sequence = ['green'], 
        range_y=(0,105)
    )
    figure.update_traces(connectgaps=True)
    figure.update_layout(font=dict(size = 16))
    figure.update_xaxes(
        showline=True, 
        linewidth=2, 
        linecolor='black', 
        mirror=False, 
        gridcolor="silver"
    )
    figure.update_yaxes(
        showline=True, 
        linewidth=2, 
        linecolor='black', 
        mirror=False, 
        gridcolor="silver"
    )
    trigger = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    end_date = end_date.split("T")[0]
    start_date = start_date.split("T")[0]
    
    if trigger == 'btnNivelWFI':
        return figure, pio.write_image(
            figure, 
            "Gráficas/Nivel WFI/"+"Nivel WFI "+start_date+"_"+end_date+".pdf", 
            format="pdf", 
            width=1770, 
            height=1250, 
            scale=1
        )
    elif trigger == 'btnCsvNivelWFI':
        return figure, dff_NivelWFI.to_csv(
            "CSV/Nivel WFI/"+"Nivel WFI "+start_date+"_"+end_date+".csv", 
            sep=';',
            decimal=','
        )
    elif trigger == 'my-date-picker-range-NivelWFI':
        return figure, dash.no_update
    else:
        return figure, dash.no_update

### Caudal WFI ###
@app.callback(
    Output('mychartCaudalWFI', 'figure'),
    Output('downloadCaudalWFI','data'),
    Input('my-date-picker-range-CaudalWFI', 'start_date'),
    Input('my-date-picker-range-CaudalWFI', 'end_date'),
    Input('btnCaudalWFI','n_clicks'),
    Input('btnCsvCaudalWFI','n_clicks')
)

def update_output2(end_date, start_date, n_clicks, n_clicks2):
    query = """
        SELECT TimeString,[WFI-FT-500] 
        FROM Main 
        WHERE [WFI-FT-500] IS NOT NULL 
        AND TimeString BETWEEN ? AND ?
    """
    dff_CaudalWFI = pd.read_sql_query(
        query,
        conn,
        index_col=["TimeString"],
        parse_dates=["TimeString"],
        params=[end_date,start_date]
    )  
    
    figure = px.line(
        dff_CaudalWFI,
        x=dff_CaudalWFI.index, 
        y=["WFI-FT-500"],
        height=700, 
        labels={"value":"Caudal (L/h)",
                "TimeString":"Fecha",
                "variable":"Sonda"
        }, 
        template="plotly_white", 
        title="Caudal WFI",
        color_discrete_sequence=['red'], 
        range_y=(0,12000)
    )
    figure.update_traces(connectgaps=True)
    figure.update_layout(font=dict(size = 16))
    figure.update_xaxes(
        showline=True, 
        linewidth=2, 
        linecolor='black', 
        mirror=False, 
        gridcolor="silver"
    )
    figure.update_yaxes(
        showline=True, 
        linewidth=2, 
        linecolor='black', 
        mirror=False, 
        gridcolor="silver"
    )
    trigger = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    end_date = end_date.split("T")[0]
    start_date = start_date.split("T")[0]
    
    if trigger == 'btnCaudalWFI':
        return figure, pio.write_image(
            figure, 
            "Gráficas/Caudal WFI/"+"Caudal WFI "+start_date+"_"+end_date+".pdf", 
            format="pdf", 
            width=1770, 
            height=1250, 
            scale=1
        )
    elif trigger == 'btnCsvCaudalWFI':
        return figure, dff_CaudalWFI.to_csv(
            "CSV/Caudal WFI/"+"Caudal WFI "+start_date+"_"+end_date+".csv", 
            sep=';',
            decimal=','
        )
    elif trigger == 'my-date-picker-range-CaudalWFI':
        return figure, dash.no_update
    else:
        return figure, dash.no_update

### Conductividad WFI ###
@app.callback(
    Output('mychartConductividadWFI', 'figure'),
    Output('downloadConductividadWFI','data'),
    Input('my-date-picker-range-ConductividadWFI', 'start_date'),
    Input('my-date-picker-range-ConductividadWFI', 'end_date'),
    Input('btnConductividadWFI','n_clicks'),
    Input('btnCsvConductividadWFI','n_clicks')
)

def update_output3(start_date,end_date, n_clicks, n_clicks2):
    query = """
        SELECT TimeString,[WFI-CT-500] 
        FROM Main 
        WHERE [WFI-CT-500] IS NOT NULL 
        AND TimeString BETWEEN ? AND ?
    """
    dff_ConductividadWFI = pd.read_sql_query(
        query,
        conn,
        index_col=["TimeString"],
        parse_dates=["TimeString"],
        params=[start_date,end_date]
    )   
    figure = px.line(
        dff_ConductividadWFI , 
        x = dff_ConductividadWFI.index, 
        y = ["WFI-CT-500"],
        height=700, 
        labels = {
            "value":"Conductividad (S/m)",
            "TimeString":"Fecha",
            "variable":"Sonda"
        }, 
        template = "plotly_white", 
        title= "Conductividad WFI",
        color_discrete_sequence = ['purple'],
        range_y = (0,1.8))
    figure.update_traces(connectgaps=True)
    
    figure.update_layout(font=dict(size = 16))
    
    figure.update_xaxes(
        showline=True, 
        linewidth=2, 
        linecolor='black', 
        mirror=False, 
        gridcolor="silver"
    )
    figure.update_yaxes(
        showline=True, 
        linewidth=2, 
        linecolor='black', 
        mirror=False, 
        gridcolor="silver"
    )
    
    trigger = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    end_date = end_date.split("T")[0]
    start_date = start_date.split("T")[0]
    
    if trigger == 'btnConductividadWFI':
        return figure, pio.write_image(
            figure, 
            "Gráficas/Conductividad WFI/"+"Conductividad WFI "+start_date+"_"+end_date+".pdf", 
            format="pdf", 
            width=1770, 
            height=1250, 
            scale=1
        )
    elif trigger == 'btnCsvConductividadWFI':
        return figure, dff_ConductividadWFI.to_csv(
            "CSV/Conductividad WFI/"+"Conductividad WFI "+start_date+"_"+end_date+".csv", 
            sep=';',
            decimal=','
        )
    elif trigger == 'my-date-picker-range-ConductividadWFI':
        return figure, dash.no_update
    else:
        return figure, dash.no_update



### TOC WFI ###
@app.callback(
    Output('mychartTOCWFI', 'figure'),
    Output('downloadTOCWFI','data'),
    Input('my-date-picker-range-TOCWFI', 'start_date'),
    Input('my-date-picker-range-TOCWFI', 'end_date'),
    Input('btnTOCWFI','n_clicks'),
    Input('btnCsvTOCWFI','n_clicks')
)

def update_output4(end_date,start_date, n_clicks, n_clicks2):
    query = """
        SELECT TimeString,[WFI-TOC] 
        FROM Main 
        WHERE [WFI-TOC] IS NOT NULL 
        AND TimeString BETWEEN ? AND ?
    """
    dff_TOCWFI = pd.read_sql_query(
        query,
        conn,
        index_col = ["TimeString"],
        parse_dates = ["TimeString"],
        params = [end_date,start_date]
    ) 
    
    figure = px.line(
        dff_TOCWFI, 
        x = dff_TOCWFI.index, 
        y= ["WFI-TOC"],
        height=700, 
        labels={
            "value":"ppb",
            "TimeString":"Fecha",
            "variable":"Sonda"
        }, 
        template= "plotly_white", 
        title= "TOC WFI",
        range_y=(0,500)
    )
    figure.update_traces(connectgaps=True)
    
    figure.update_layout(font=dict(size = 16))
    
    figure.update_xaxes(
        showline=True, 
        linewidth=2, 
        linecolor='black', 
        mirror=False, 
        gridcolor="silver"
    )
    figure.update_yaxes(
        showline=True, 
        linewidth=2, 
        linecolor='black', 
        mirror=False, 
        gridcolor="silver"
    )
    
    trigger = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    end_date = end_date.split("T")[0]
    start_date = start_date.split("T")[0]
    
    if trigger == 'btnTOCWFI':
        return figure, pio.write_image(
            figure, 
            "Gráficas/TOC WFI/"+"TOC WFI "+start_date+"_"+end_date+".pdf", 
            format="pdf", 
            width=1770, 
            height=1250, 
            scale=1
        )
    elif trigger == 'btnCsvTOCWFI':
        return figure, dff_TOCWFI.to_csv(
            "CSV/TOC WFI/"+"TOC WFI "+start_date+"_"+end_date+".csv", 
            sep=';',
            decimal=','
        )
    elif trigger == 'my-date-picker-range-TOCWFI':
        return figure, dash.no_update
    else:
        return figure, dash.no_update
