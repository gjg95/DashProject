import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import subprocess
from datetime import datetime
import dash
from apscheduler.schedulers.background import BackgroundScheduler
from app import app
from app import conn
# Imports de los scripts que contienen los layout de la aplicación web.
from apps import (
    TemperaturaGenPW, 
    TempDest, 
    PresionDest, 
    CauConDest, 
    OtrosGenPW, 
    CaudalGenPW, 
    ConductGenPW, 
    TempWFI, 
    TempPW, 
    NiCaCoPW, 
    NiCaCoTOCWFI
)
# Imports de todos los layout de las diferentes páginas de la aplicación web.
from apps.TemperaturaGenPW import TemperaturaGenPW_display
from apps.ConductGenPW import ConductGenPW_display
from apps.CaudalGenPW import CaudalGenPW_display
from apps.OtrosGenPW import OtrosGenPW_display
from apps.PresionDest import PresionDest_display
from apps.TempDest import TempDest_display
from apps.CauConDest import CauConDest_display
from apps.TempWFI import TempWFI_display
from apps.TempPW import TempPW_display
from apps.NiCaCoPW import NiCaCoPW_display
from apps.NiCaCoTOCWFI import NiCaCoTOCWFI_display



now = datetime.now()
current_time = now.strftime("%d/%m/%Y %H:%M:%S")


# Función que describe el layout de la aplicación, la barra de navegación, los
# diferentes botones, y el layout vacío que se rellena con una de las apps a 
# las que llama cuando cambia de url.
def serve_layout():
    # Este bloque de código actualiza la fecha límite de descarga de los datos
    # de GenPW, está dentro de la función para que se actualice con cada
    # refresh de la página web.
    query = """
        SELECT TimeString 
        FROM Main 
        WHERE [Cond permeado RO] IS NOT NULL 
        ORDER BY TimeString 
        DESC LIMIT 1
    """
    dff_time = pd.read_sql_query(
        query,
        conn,
        index_col=["TimeString"],
        parse_dates=["TimeString"]
    )
    rawtime = dff_time.index.values
    enddate = pd.to_datetime(rawtime) + pd.DateOffset(days=10)
    postdate = enddate.strftime('%Y-%m-%d')
    printdate = postdate.values[0] # Fecha que aparece en el layout

    # El layout como tal de la apliación, aquí está todo el código del frontend
    # de la barra de navegación, llamando al contenido de cada página desde un
    # callback.
    return html.Div([
     dcc.Location(
         id='url', 
         refresh=False
     ),
     dcc.Store(
         id="my-data", 
         storage_type='session'
     ),
     dbc.Navbar([
        html.Div(id='dummy1'),
        html.Div(id='dummy2'),
        html.A(
            dbc.Row(
                dbc.Col(
                    dbc.NavbarBrand(
                        "DATOS PLANTA DE AGUAS", 
                        className="ml-2",
                        style={"margin-right":"3em",
                               "margin-left":"0.5em"
                        } 
                    )
                ),
                align="center",
                no_gutters=True,
            )
        ), 
        html.Div(
            dbc.DropdownMenu(
                nav=False,
                in_navbar=False,
                label= "LAZO WFI",
                children =[
                    dbc.DropdownMenuItem(
                        "Temperatura WFI", 
                        href="/apps/Temp-WFI"
                    ),
                    dbc.DropdownMenuItem(
                        "Variables WFI", 
                        href="/apps/Caudal_Nivel_Conductividad_TOC-WFI"
                    )
                ], 
                style={"margin-right":"1em"}
            )
        ),
        html.Div(
            dbc.DropdownMenu(
                nav=False,
                in_navbar=False,
                label= "DESTILADOR",
                children = [
                    dbc.DropdownMenuItem(
                        "Temperatura Destilador", 
                        href="/apps/Temp-Dest"
                    ),
                    dbc.DropdownMenuItem(
                        "Presión Destilador", 
                        href="/apps/Pre-Dest"
                    ),
                    dbc.DropdownMenuItem(
                        "Variables Destilador", 
                        href="/apps/Caudal-Conduc-Destilador"
                    ),
                ], 
                style={"margin-right":"1em"}
            )
        ),
        html.Div(
            dbc.DropdownMenu(
                nav=False,
                in_navbar=False,
                label= "LAZO PW",
                children =[
                    dbc.DropdownMenuItem(
                        "Temperatura PW", 
                        href="/apps/Temp-PW"
                    ),
                    dbc.DropdownMenuItem(
                        "Variables PW",
                        href="/apps/Caudal_Nivel_Conductividad-PW"
                    ),
                ], 
                style={"margin-right":"1em"}
            )
        ),  
        html.Div(
            dbc.DropdownMenu(
                nav=False,
                in_navbar=False,
                label= "GENERACIÓN PW",
                children =[
                    dbc.DropdownMenuItem(
                        "Conductividad Gen PW", 
                        href="/apps/Conduct-GenPW"
                    ),
                    dbc.DropdownMenuItem(
                        "Caudal Gen PW", 
                        href="/apps/Caudal-GenPW"
                    ),
                    dbc.DropdownMenuItem(
                        "Temperatura Gen PW", 
                        href="/apps/Temperatura-GenPW"
                    ),
                    dbc.DropdownMenuItem(
                        "Otros Gen PW",
                        href="/apps/Otros-GenPW"
                    ),
                ],
            )
        ),
        html.Div(
            dbc.Row([
                dbc.Col([
                    dbc.Button(
                        'FORCE UPDATE', 
                        id='apply-button2', 
                        n_clicks=0, 
                        color="warning", 
                        outline=True,
                        style={"margin-left":"100px","margin-bottom":"0px"}
                    ),
                    dcc.Loading(
                        id='output-container-button2', 
                        fullscreen=True,
                        color="#18bc9c"
                    )
                ]),
            ]),
        ),
        html.Div(
            html.P(
                children=str("Extraer datos de Gen PW antes del: "+printdate), 
                style={
                    "textAlign": "center",
                    "marginLeft":"3em",
                    "color":"white",
                    "width":"250px", 
                    "height":"2em"
                }
            )
        ),
        html.Div([
            dbc.Button(
                "Ayuda",
                id="botonAyuda",
                n_clicks=0,
                color="info",
                style={"margin-left":"4em"}
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader("Guía de uso"),
                    dbc.ModalBody(dcc.Markdown("""
##### El dashboard tiene las siguientes características:
    
Permite la visualización de los equipos de la planta de aguas: 
**Lazo WFI y PW, Generación PW y Destilador.**

La barra superior de navegación contiene unos menús desplegables con las
diferentes páginas donde están alojados los gráficos. Cada menú que se
despliega trae la descripción de los gráficos que contiene esa página.
Si se accede  a una página cualquiera se observan distintos elementos:
    
* **Selector de fechas:** En la parte superior de cada gráfica aparecen dos 
fechas, la selección entre estas dos fechas es la dibujada en la gráfica 
situdada en la parte inferior.

* **Botones de impresión:** Estos botones permiten realizar una impresión 
rápida de la gráfica que se observa en ese momento en pantalla y de los datos
en formato .csv que el programa utiliza para realizarla.
  + Nombredelagráfica fechainicio_fechafin.pdf 
    (C:/Users/***/Desktop/Planta aguas Project/Gráficas)
  + Nombredelagráfica fechainicio_fechafin.csv
    (C:/Users/***/Desktop/Planta aguas Project/CSV)

* **Gráfica:** Cada una de las gráficas cuenta con un títutlo que describe su
contenido, una descripción en el eje y que indica las unidades que se están
midiendo, una leyenda en la parte derecha con las sondas que se utilizan y un
menú flotante con distintas opciones para que el usuario pueda manipular el 
gráfico.

##### **NOTAS**

En caso de que no se vean datos que ya deberían estar en la base de datos
actualizar con el botón de recarga del navegador o pulsando F5 en el teclado
para que los datos cargados de forma automática se visualicen en las gráficas.

El programa se actualiza de manera autónoma todos los días a las 01:12 h, en
caso de necesitar forzar la actualización para visualizar datos cargados de 
forma manual existe un botón en la parte superior de la barra de navegación
"FORCE UPDATE" que fuerza la actualización. Una vez pulsado aparece una 
pantalla de carga y una vez esta ha finalizado se puede proceder a actualizar
la página web para que aparezcan los nuevos datos.

En la barra superior existe un recordatorio para cargar de forma manual
los datos de la generación PW y que no se pierdan ya que el controlador del
equipo solo es capaz de almacenar datos durante 12 días. El programa 
coge el último valor que tiene en la base de datos de la generación PW y 
establece un recordatorio 10 días después de esta última fecha.

Actualmente solo está automatizada la toma de datos de los lazos WFI y PW, para
la generacion PW y el destilador hay que hacer un volcado manual de los datos
en sus correspondientes carpetas situadas en el escritorio de este equipo.
"""
                        ),
                    ),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Cerrar",
                            id="botonCerrar",
                            className="ms-auto",
                            n_clicks=0
                        ),
                    ),
                ],
                id="modal",
                is_open=False,
                size="xl",
                autoFocus=True
            ),
        ])
    ],
    color="primary",
    dark=True,
    ),
    html.Div(id='page-content', children=[], style={"float":"center"})
  ]
  )


# Indica que el layout de la aplicación web es la función serve_layout.
app.layout= serve_layout

# Callback que cambia el cuerpo de la página web en función de la url que se
# seleccione a través de los Dropdown que hay en la barra de navegación.
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname')
)

def display_page(pathname):
    if pathname == '/apps/Conduct-GenPW':
        ConductGenPW.layout = ConductGenPW_display()
        return ConductGenPW.layout
    elif pathname == '/apps/Caudal-GenPW':
        CaudalGenPW.layout = CaudalGenPW_display()
        return CaudalGenPW.layout
    elif pathname == '/apps/Temperatura-GenPW':
        TemperaturaGenPW.layout = TemperaturaGenPW_display()
        return TemperaturaGenPW.layout   
    elif pathname == '/apps/Otros-GenPW':
        OtrosGenPW.layout = OtrosGenPW_display()
        return OtrosGenPW.layout  
    elif pathname == '/apps/Temp-WFI':
        TempWFI.layout = TempWFI_display()
        return TempWFI.layout
    elif pathname == "/apps/Temp-PW":
        TempPW.layout = TempPW_display()
        return TempPW.layout
    elif pathname == '/apps/Caudal_Nivel_Conductividad-PW':
        NiCaCoPW.layout = NiCaCoPW_display()
        return NiCaCoPW.layout    
    elif pathname == '/apps/Caudal_Nivel_Conductividad_TOC-WFI':
        NiCaCoTOCWFI.layout = NiCaCoTOCWFI_display()
        return NiCaCoTOCWFI.layout
    elif pathname == '/apps/Temp-Dest':
        TempDest.layout = TempDest_display()
        return TempDest.layout
    elif pathname == '/apps/Pre-Dest':
        PresionDest.layout = PresionDest_display()
        return PresionDest.layout
    elif pathname == '/apps/Caudal-Conduc-Destilador':
        CauConDest.layout = CauConDest_display()
        return CauConDest.layout
    else:
        return "404 Error! Por favor selecciona un enlace "
    
# Callback que controla el botón "FORCE UPDATE. Lanza de forma paralela al
# script principal los 4 scripts ETL de cada una de las máquinas de las que se
# tienen datos. Se ejecutan las tres extracciones y transformaciones de datos y
# por último se cargan en una base de datos.
@app.callback(
    dash.dependencies.Output('output-container-button2', 'children'),
    [dash.dependencies.Input('apply-button2', 'n_clicks')]
)

def run_script_onClick(n_clicks):
    if not n_clicks:
        return dash.no_update
    print("Comienzo actualización FORZADA base de datos", current_time)    
    result1 = subprocess.check_output('python LazosData.py', shell=True)
    result1 = result1.decode()
    print("Lazos DONE")
    result2 = subprocess.check_output('python GeneracionPWData.py', shell=True)
    result2 = result2.decode(encoding='latin-1')
    print("Generación PW DONE")
    result3 = subprocess.check_output('python DestiladorData.py', shell=True)
    result3 = result3.decode()
    print("Destilador DONE")
    result4 = subprocess.check_output('python CreateDatabaseGlobal.py', shell=True)
    result4 = result4.decode()
    print("GLOBAL DATABASE DONE, LISTO PARA VISUALIZAR", current_time)


# Callback del modal que contiene una ayuda de usuario para el manejo de la 
# aplicación, abre y cierra el modal.
@app.callback(
    Output("modal", "is_open"),
    [Input("botonAyuda", "n_clicks"), Input("botonCerrar", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# Esta función realiza la misma tarea de actualización pero está controlada por
# un trigger diario.
def job():
    print("Comienzo actualización base de datos", current_time)
    result1 = subprocess.check_output('python LazosData.py', shell=True)
    result1 = result1.decode()
    print("Lazos DONE")
    result2 = subprocess.check_output('python GeneracionPWData.py', shell=True)
    result2 = result2.decode(encoding='latin-1')
    print("Generación PW DONE")
    result3 = subprocess.check_output('python DestiladorData.py', shell=True)
    result3 = result3.decode()
    print("Destilador DONE")
    result4 = subprocess.check_output('python CreateDatabaseGlobal.py', shell=True)
    result4 = result4.decode()
    print("GLOBAL DATABASE DONE, LISTO PARA VISUALIZAR", current_time)


# Trigger diario que ejecuta la función job para actualizar la base de datos
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(job, trigger='cron',hour="01", minute="12")
scheduler.start()


if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=False,use_reloader=False)
    
