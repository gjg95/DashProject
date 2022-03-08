from functools import reduce
import pandas as pd
import glob
import os

variable = 'Variables'

todrop = ["$RT_DIS$","$RT_COUNT$","$RT_OFF$"]

fileList = {1:"InformesPW",2:"InformesWFI",3:"Variables"}


tipoList={
    1:'Caudal_PW',2:'Caudal_WFI',3:'Conductividad_PW',
    4:'Conductividad_WFI',5:'Nivel_PW',6:'Nivel_WFI',
    7:'Temperatura_PW',8:'Temperatura_WFI',9:'TOC_WFI'
}

def csvMaker():
    results1 = pd.DataFrame()
    os.chdir("C:/HMI/")
    for counter, current_file1 in enumerate(glob.glob(
            'InformesPW/**/'+tipoList[i]+'*',recursive=True)):
        namedf = pd.read_csv(current_file1,sep=';', usecols=[0,1,2])
        results1 = pd.concat([results1, namedf])
        print(counter)
    for counter, current_file1 in enumerate(glob.glob(
            'InformesWFI/**/'+tipoList[i]+'*',recursive=True)):
        namedf = pd.read_csv(current_file1,sep=';', usecols=[0,1,2])
        results1 = pd.concat([results1, namedf])
        print(counter)
    for counter, current_file1 in enumerate(glob.glob(
            'Variables/'+tipoList[i]+'*',recursive=True)):
        namedf = pd.read_csv(current_file1,sep=';', usecols=[0,1,2])
        results1 = pd.concat([results1, namedf])
        print(counter)

    results1.drop_duplicates(subset=["VarName","TimeString"], inplace=True)
    results1["VarValue"] = results1['VarValue'].replace(',','.',regex=True)
    results1['TimeString'] = pd.to_datetime(
        results1['TimeString'],
        dayfirst=True,
        errors='coerce',
        format="%d.%m.%Y %H:%M:%S"
    )
    results1 = results1[~results1["VarName"].isin(todrop)]
    results1 = results1.set_index("TimeString")
    results1 = results1.pivot(columns=["VarName"], values=["VarValue"])
    results1.columns = results1.columns.droplevel(0)
    
    results1.info()
    results1.head()
    os.chdir("C:/Users/***/Desktop/Planta aguas Project/")
    results1.to_csv(
        str('Data/'+tipoList[i])+'_Master.csv', 
        index_label="TimeString"
    )
    print (str(tipoList[i])+" Done")
    
    
for i in tipoList:
    csvMaker()
    
    

    
os.chdir(r"C:\Users\***\Desktop\Planta aguas Project")

df1 = pd.read_table('Data/Caudal_PW_Master.csv', sep=',')
df2 = pd.read_table('Data/Caudal_WFI_Master.csv', sep=',')
df3 = pd.read_table('Data/Conductividad_PW_Master.csv', sep=',')
df4 = pd.read_table('Data/Conductividad_WFI_Master.csv', sep=',')
df5 = pd.read_table('Data/Nivel_PW_Master.csv', sep=',')
df6 = pd.read_table('Data/Nivel_WFI_Master.csv', sep=',')
df7 = pd.read_table('Data/Temperatura_PW_Master.csv', sep=',')
df8 = pd.read_table('Data/Temperatura_WFI_Master.csv', sep=',')
df9 = pd.read_table('Data/TOC_WFI_Master.csv', sep=',')

data_frames = [df1, df2, df3, df4, df5, df6, df7, df8 , df9]

df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['TimeString'],
                                            how='outer',sort=True), data_frames)

df_merged['TimeString'] = pd.to_datetime(
    df_merged['TimeString'],
    dayfirst=True,
    errors='coerce',
    format="%Y-%m-%d %H:%M:%S"
)
df_merged.sort_values('TimeString')

def try_cutoff(x):
    try:
        return round(float(x), 2)
    except Exception:
        return x

for field in df_merged.columns:
    df_merged[field] = df_merged[field].map(try_cutoff)




df_merged.to_csv('Data/Database_Lazos.csv', index=None)

for i in tipoList:
    os.remove("Data/"+str(tipoList[i])+"_Master.csv")
