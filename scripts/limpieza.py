import pandas as pd 
from pathlib import Path

csv_path = Path(r"C:\Users\cristian\parcial_api_futbol\datos\players_data_light-2024_2025.csv")

CSV_SALIDA = Path(r"C:\Users\cristian\parcial_api_futbol\datos\jugadores_limpios.csv")


def cargar_datos():
    df=pd.read_csv(csv_path)
    print(f" jugadores cargados: {len(df)}")
    return df 

def filtrar_minutos(df):
    antes = len(df)
    df= df[df["Min"]>=450]
    despues= len(df)

    print(f"Jugadores eliminados: {antes- despues}")
    print(f"Jugadores restantes: {despues}")
    return df

def limpiar_nulos(df):
    df["Nation"] = df["Nation"].fillna("desconocido")
    df["Age"] = df["Age"].fillna(0).astype(int)

    # Imputación con mediana para columnas numéricas
    columnas = ["Gls", "Ast", "xG", "xAG", "KP", "Tkl", "Int"]
    for col in columnas:
        if col in df.columns:
            mediana = df[col].median()
            df[col] = df[col].fillna(mediana)
            print(f"  {col}: imputado con mediana={round(mediana,2)}")

    print("Nulos limpios")
    return df

def simplificar_pos(df):
    df["Pos"]= df["Pos"].str.split(",").str[0]
    print("Posiciones simplificadas:")
    print(df["Pos"].value_counts())
    return df 

def guardar_datos(df):
    df.to_csv(CSV_SALIDA, index=False)
    print(f"Archivo guardado con {len(df)} jugadores")

def ejecutar_limpieza():
    print("\n🧹 === LIMPIEZA DEL DATASET ===")
    df = cargar_datos()
    df = filtrar_minutos(df)
    df = limpiar_nulos(df)
    df = simplificar_pos(df)
    guardar_datos(df)
    print("✅ Limpieza completada\n")

if __name__=="__main__":
    df=cargar_datos()
    df=filtrar_minutos(df)
    df=limpiar_nulos(df)
    df=simplificar_pos(df)
    guardar_datos(df)
