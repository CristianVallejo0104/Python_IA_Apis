import numpy as np 
from models import jugador_input, resultados
import time                  
from functools import wraps

def medir_tiempo(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fin = time.time()
        print(f"⏱️ {func.__name__} tardó {round(fin - inicio, 4)} segundos")
        return resultado
    return wrapper

@medir_tiempo                  
def calcular_est(jugador: jugador_input, id_registro: int) -> resultados:    
    datos= np.array(jugador.metricas_por_partido)
    prom= round(float(np.mean(datos)),4)
    vari= round(float(np.var(datos, ddof=1)),4)
    des_std=round(float(np.std(datos, ddof=1)),4)
    maxi=round(float(np.max(datos)),4)
    mini=round(float(np.min(datos)),4)
    rang= round(float(maxi-mini),4)


    if des_std < 0.5:
        perfil="Consistente"
    elif des_std <1:
        perfil= "De rachas"
    else:
        perfil="Irregular"

    if prom > 0.6 and des_std < 1:
        recomendacion= "Fichar"
    elif prom > 0.3:
        recomendacion= "Observar"
    else:
        recomendacion= "Descartar"

    return resultados(
        id       = id_registro,
        nombre   = jugador.Player,
        equipo   = jugador.Squad,
        posicion = jugador.Pos,
        liga     = jugador.Comp,        
        edad     = jugador.Age,

        promedio  = prom,
        varianza  = vari,
        desvi_std = des_std,            
        maximo    = maxi,
        minimo    = mini,
        rango     = rang,

        perfil_consistencia = perfil,
        recomendacion       = recomendacion,  

        minutos_analizados = jugador.Min,     
        n_metricas         = len(jugador.metricas_por_partido)
    )


if __name__ == "__main__":
    jugador_prueba = jugador_input(
        Player = "Erling Haaland",
        Nation = "NOR",
        Pos    = "FW",
        Squad  = "Manchester City",
        Comp   = "Premier League",
        Age    = 24,
        Min    = 2500,
        metricas_por_partido = [0.82, 0.45, 1.2, 0.9, 0.6, 0.75]
    )

    resultado = calcular_est(jugador_prueba, id_registro=1)
    print(resultado)