import pandas as pd 
from pathlib import Path

csv_path = Path(r"C:\Users\cristian\parcial_api_futbol\datos\players_data_light-2024_2025.csv")
def cargar_datos():
    df=pd.read_csv(csv_path)
    print(f" jugadores cargados: {len(df)}")
    return df 

def est_desc(df):
    print("Filas y columnas:", df.shape)
    print("Columnas:", df.columns.tolist())
    print("Tipos de dato:")
    print(df.dtypes)

def analizar_nulos(df):
    nulos=df.isnull().sum()
    porcentaje= (nulos/len(df)*100).round(2)

    reporte= pd.DataFrame(
    {
        "nulos": nulos,
        "porcentaje": porcentaje
    })

    reporte= reporte[reporte["nulos"]>0]

    print("Columnas con valores faltantes:")
    print(reporte)
    return reporte 

def analizar_jugadores(df):
    print("jugadores por posicion")
    print(df["Pos"].value_counts())

    pocos_min= df[df["Min"]<450]
    print(f"Jugadores con menos de 450: {len(pocos_min)}")
    print(f"Jugadores que si usaremos: {len(df)-len(pocos_min)}")

if __name__=="__main__":
    df=cargar_datos()
    est_desc(df)
    analizar_nulos(df)
    analizar_jugadores(df)
