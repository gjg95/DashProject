import pandas as pd
import os
import glob

tipoList={1:'Conductividades0',2:'Caudales0',3:'Otros0',4:'Temperaturas0'}

todrop = ["$RT_DIS$","$RT_COUNT$","$RT_OFF$"]

fulldata = list()

def csvMaker():
    results = pd.DataFrame()
    os.chdir("C:/Users/jsolana/Desktop/Datos Gen PW")
    for counter, current_file in enumerate(glob.glob('**/**/'+tipoList[i]+'*',recursive=True)):
        namedf = pd.read_csv(current_file,sep=';', usecols=[0,1,2])
        results = pd.concat([results, namedf])
    results.drop_duplicates(subset=["VarName","TimeString"], inplace=True)
    results["VarValue"] = results['VarValue'].replace(',','.',regex=True)
    results['TimeString'] = pd.to_datetime(
        results['TimeString'],
        dayfirst=True,
        errors='coerce',
        format="%d.%m.%Y %H:%M:%S"
    )
    results = results[~results["VarName"].isin(todrop)]
    results = results.set_index("TimeString")
    results = results.pivot(columns=["VarName"], values=["VarValue"])
    results.columns = results.columns.droplevel(0)
    return fulldata.append(results)
    
for i in tipoList:
    csvMaker()
    
final = pd.concat(fulldata)
final.rename({
    "db_ALAN_ALAN1_rEA":"Retorno Tensión CEDI",
    "db_ALAN_ALAN6_rEA":"Tª Entrada Intercambiador",
    "db_ALAN_ALAN7_rEA":"Cond entrada intercambiador",
    "db_ALAN_ALAN8_rEA":"Tª Salida Intercambiador",
    "db_ALAN_ALAN9_rEA":"Redox Entrada RO",
    "db_ALAN_ALAN10_rEA":"Presión impulsión bomba alta presión",
    "db_ALAN_ALAN11_rEA":"Tª Rechazo RO",
    "db_ALAN_ALAN12_rEA":"Caudal Rechazo RO",
    "db_ALAN_ALAN13_rEA":"Caudal Recirculación RO",
    "db_ALAN_ALAN14_rEA":"Caudal Permeado RO",
    "db_ALAN_ALAN15_rEA":"Cond permeado RO",
    "db_ALAN_ALAN16_rEA":"Tª Permeado CEDI",
    "db_ALAN_ALAN17_rEA":"Tª Rechazo CEDI",
    "db_ALAN_ALAN18_rEA":"Caudal Permeado CEDI Salida UV",
    "db_ALAN_ALAN19_rEA":"Cond Salida UV / CEDI",
    "db_ALAN_ALAN22_rEA":"Pretratamiento Cloro",
    "db_ALAN_ALAN33_rEA":"Caudal Concentrado CEDI",
    },
    axis=1,
    inplace=True
)
final.info()
os.chdir(r"C:\Users\jsolana\Desktop\Planta aguas Project")
final.to_csv('Data/Database_GenPW.csv')
