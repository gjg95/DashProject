import sys
import os
from waitress import serve

module_path = os.path.abspath(os.getcwd())    

if module_path not in sys.path:       

    sys.path.append(module_path)



import app
import index


serve(app.server, host="127.0.0.1", port="8050", threads= 6)
