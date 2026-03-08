from pydantic import BaseModel, Field 
from typing import Optional, List 

class jugador_input(BaseModel):

    #---Informacion basica---
    Player: str = Field(...,min_length=2, description="Nombre del jugador")
    Nation: str = Field(...,min_length=2, description="Nacionalidad")
    Pos: str = Field(..., description="Posicion: FW, MF, DF o GK")
    Squad: str = Field(...,min_length=2, description="Club o equipo")
    Comp: str = Field(..., description="Liga donde juega")
    Age: int = Field(...,ge=15, le=45, description="Edad del jugador")
    Min: int = Field(...,ge=2, le=5400, description="Minutos jugados" )

    metricas_por_partido: List[float] = Field(
    ..., 
    min_length=5,
    description="""Ingresa mínimo 5 métricas del jugador, TODAS en la misma escala.
    OPCIÓN A - Por partido: [0.52, 0.38, 0.71, 0.44, 1.2] (xG, Ast, KP, PrgC, SoT por partido)
    OPCIÓN B - Temporada completa: [24, 9, 18, 72, 3] (Gls, Ast, KP, Tkl, Int totales)
    ⚠️ NO mezcles valores por partido con totales de temporada.""")

    nombres_metricas: Optional[List[str]]= Field(default=None, description="Nombre de cada metrica (ej; 'xG', 'KP', PrgP')")

class resultados(BaseModel):

    #ID
    id: int
    nombre: str
    equipo: str
    posicion: str
    liga: str
    edad: int


    promedio: float
    varianza: float
    desvi_std: float
    maximo: float
    minimo: float
    rango: float

    perfil_consistencia: str
    recomendacion: str

    minutos_analizados:int
    n_metricas: int