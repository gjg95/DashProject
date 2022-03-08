import dash
import sqlite3



conn = sqlite3.connect(
    'C:/Users/***/Desktop/Planta aguas Project/Data/DATABASE.db',
    check_same_thread=False
)
cur = conn.cursor()

# meta_tags are required for the app layout to be mobile responsive
app = dash.Dash(__name__, suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}
                ]
)

server = app.server

print("APP READY, dashboard visualización planta de aguas") 
