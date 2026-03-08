# ⚽ API de Scouting de Fútbol

> Mediante las métricas ingresadas del jugador, se dirá si es consistente durante la temporada y si es una buena opción de compra.

## 📌 Descripción

API REST desarrollada con **FastAPI** para el análisis de rendimiento y consistencia de jugadores de las 5 grandes ligas europeas. Usa datos de la temporada 2024/25 de FBref con 1,982 jugadores limpios.

## 🏆 Ligas incluidas

| Liga | País |
|------|------|
| Premier League | 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra |
| La Liga | 🇪🇸 España |
| Bundesliga | 🇩🇪 Alemania |
| Serie A | 🇮🇹 Italia |
| Ligue 1 | 🇫🇷 Francia |

## 🗂️ Estructura del proyecto
```
parcial_api_futbol/
├── scripts/
│   ├── eda.py           → Análisis exploratorio del dataset
│   ├── limpieza.py      → Filtrado e imputación de datos
│   ├── models.py        → Modelos Pydantic con validaciones
│   ├── procesamiento.py → Cálculos estadísticos con NumPy
│   └── main.py          → API FastAPI con 7 endpoints
├── datos/               → No incluido en el repositorio
└── .gitignore
```

## 🚀 Cómo ejecutar

1. Instala las dependencias:
```bash
pip install fastapi uvicorn pandas numpy
```

2. Ejecuta la API:
```bash
cd scripts
uvicorn main:app --reload
```

3. Abre en el navegador:
```
http://127.0.0.1:8000
```

## 📡 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Página principal |
| POST | `/Analizar` | Analizar rendimiento de un jugador |
| GET | `/historial` | Ver todos los análisis |
| GET | `/historial/{id}` | Ver análisis por ID |
| DELETE | `/historial/{id}` | Eliminar análisis |
| GET | `/metricas/{posicion}` | Ver métricas sugeridas por posición |
| GET | `/jugador/{nombre}` | Buscar jugador en el dataset |

## 📊 Clasificación de consistencia

| Desv. Estándar | Perfil |
|----------------|--------|
| < 0.5 | ✅ Consistente |
| 0.5 - 1.0 | 🟡 De rachas |
| > 1.0 | ❌ Irregular |

## 💡 Recomendación de fichaje

| Condición | Recomendación |
|-----------|---------------|
| Promedio > 0.6 y Std < 1.0 | ✅ Fichar |
| Promedio > 0.3 | 🟡 Observar |
| Promedio ≤ 0.3 | ❌ Descartar |

## 🛠️ Tecnologías

- **FastAPI** — Framework web para la API
- **Pydantic** — Validación de datos
- **NumPy** — Cálculos estadísticos
- **Pandas** — Manejo del dataset
- **Uvicorn** — Servidor ASGI

## 👨‍💻 Autor

Cristian Vallejo — Estudiante de Estadística  
Curso: Python para APIs e IA