from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from typing import List, Dict
from models import jugador_input, resultados
from procesamiento import calcular_est
import pandas as pd
from pathlib import Path 

CSV_PATH = Path(r"C:\Users\cristian\parcial_api_futbol\datos\jugadores_limpios.csv")
df_jugadores = pd.read_csv(CSV_PATH)

app = FastAPI(
    title="Rendimiento jugador",
    description="Mediante las metricas ingresadas del jugador, se dirá si es consistente durante la temporada y si es una buena opcion de compra",
    version="1.1.2"
)

historial: Dict[int, resultados] = {}
contador_id: int = 0

@app.get("/", response_class=HTMLResponse, tags=["🏠 Inicio"])
def bienvenida():
    return """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚽ Football Scout API</title>
    <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --verde: #00ff87;
            --verde-oscuro: #00c96a;
            --fondo: #060a0f;
            --card: #0d1520;
            --card2: #111d2e;
            --borde: #1a2d45;
            --texto: #c8d8e8;
            --blanco: #ffffff;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'DM Sans', sans-serif;
            background: var(--fondo);
            color: var(--texto);
            min-height: 100vh;
        }
        /* HEADER */
        header {
            background: linear-gradient(135deg, #060a0f 0%, #0a1628 100%);
            border-bottom: 1px solid var(--borde);
            padding: 24px 40px;
            display: flex;
            align-items: center;
            gap: 16px;
            position: sticky;
            top: 0;
            z-index: 100;
            backdrop-filter: blur(10px);
        }
        header h1 {
            font-family: 'Bebas Neue', sans-serif;
            font-size: 2rem;
            color: var(--blanco);
            letter-spacing: 2px;
        }
        header span {
            background: var(--verde);
            color: #000;
            font-size: 11px;
            font-weight: 600;
            padding: 3px 10px;
            border-radius: 20px;
            letter-spacing: 1px;
        }
        /* LAYOUT */
        .container { max-width: 1100px; margin: 0 auto; padding: 40px 24px; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        /* CARDS */
        .card {
            background: var(--card);
            border: 1px solid var(--borde);
            border-radius: 16px;
            padding: 28px;
        }
        .card h2 {
            font-family: 'Bebas Neue', sans-serif;
            font-size: 1.3rem;
            color: var(--verde);
            letter-spacing: 2px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        /* INPUTS */
        input, select {
            width: 100%;
            background: var(--card2);
            border: 1px solid var(--borde);
            border-radius: 10px;
            padding: 12px 16px;
            color: var(--blanco);
            font-family: 'DM Sans', sans-serif;
            font-size: 14px;
            margin-bottom: 12px;
            outline: none;
            transition: border 0.2s;
        }
        input:focus, select:focus { border-color: var(--verde); }
        select option { background: var(--card2); }
        label {
            font-size: 12px;
            color: #6a8aaa;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 6px;
            display: block;
        }
        /* BOTONES */
        button {
            width: 100%;
            background: var(--verde);
            color: #000;
            border: none;
            border-radius: 10px;
            padding: 13px;
            font-family: 'Bebas Neue', sans-serif;
            font-size: 1.1rem;
            letter-spacing: 2px;
            cursor: pointer;
            transition: all 0.2s;
            margin-top: 4px;
        }
        button:hover { background: var(--verde-oscuro); transform: translateY(-1px); }
        .btn-rojo { background: #ff4560; color: #fff; }
        .btn-rojo:hover { background: #cc2040; }
        /* RESULTADOS */
        .resultado {
            background: var(--card2);
            border: 1px solid var(--borde);
            border-radius: 12px;
            padding: 20px;
            margin-top: 16px;
            display: none;
        }
        .resultado.visible { display: block; }
        .stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 12px; }
        .stat {
            background: var(--card);
            border-radius: 10px;
            padding: 12px;
            text-align: center;
        }
        .stat .valor {
            font-family: 'Bebas Neue', sans-serif;
            font-size: 1.6rem;
            color: var(--verde);
        }
        .stat .etiqueta { font-size: 11px; color: #6a8aaa; text-transform: uppercase; }
        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            margin: 4px;
        }
        .badge-verde { background: rgba(0,255,135,0.15); color: var(--verde); }
        .badge-amarillo { background: rgba(255,200,0,0.15); color: #ffc800; }
        .badge-rojo { background: rgba(255,69,96,0.15); color: #ff4560; }
        .jugador-item {
            background: var(--card2);
            border: 1px solid var(--borde);
            border-radius: 10px;
            padding: 14px 16px;
            margin-bottom: 8px;
            cursor: pointer;
            transition: border 0.2s;
        }
        .jugador-item:hover { border-color: var(--verde); }
        .jugador-item .nombre { font-weight: 600; color: var(--blanco); font-size: 15px; }
        .jugador-item .detalle { font-size: 12px; color: #6a8aaa; margin-top: 4px; }
        .pos-badge {
            display: inline-block;
            background: rgba(0,255,135,0.1);
            color: var(--verde);
            border-radius: 6px;
            padding: 2px 8px;
            font-size: 11px;
            font-weight: 600;
            margin-left: 8px;
        }
        .error { color: #ff4560; font-size: 13px; margin-top: 8px; }
        .historial-item {
            background: var(--card2);
            border: 1px solid var(--borde);
            border-radius: 10px;
            padding: 14px 16px;
            margin-bottom: 8px;
            cursor: pointer;
            transition: border 0.2s;
        }
        .historial-item:hover { border-color: var(--verde); }
        .historial-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .historial-item .info .nombre { font-weight: 600; color: var(--blanco); }
        .historial-item .info .detalle { font-size: 12px; color: #6a8aaa; margin-top: 2px; }
        .btn-small {
            width: auto;
            padding: 6px 14px;
            font-size: 0.85rem;
            margin: 0;
        }
        .full-width { grid-column: 1 / -1; }
        hr { border: none; border-top: 1px solid var(--borde); margin: 16px 0; }
        .seccion-titulo {
            font-family: 'Bebas Neue', sans-serif;
            font-size: 1rem;
            color: #6a8aaa;
            letter-spacing: 2px;
            margin-bottom: 12px;
        }
    </style>
</head>
<body>
<header>
    <div>⚽</div>
    <h1>Football Scout API</h1>
    <span>TEMPORADA 2024/25</span>
</header>

<div class="container">

    <div style="margin-bottom:30px">
        <p style="color:#c8d8e8;font-size:15px">Sistema de análisis de rendimiento y consistencia de jugadores de las <strong style="color:#00ff87">5 grandes ligas europeas</strong>. Busca jugadores de la temporada 2024/25 e ingresa métricas actuales desde <a href="https://sofascore.com" target="_blank" style="color:#00ff87">Sofascore</a> o <a href="https://fbref.com" target="_blank" style="color:#00ff87">FBref</a> para analizar cualquier temporada.</p>
        <div style="display:flex;gap:12px;margin-top:16px;flex-wrap:wrap">
            <span style="background:#1a2d45;padding:6px 14px;border-radius:20px;font-size:13px">🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League</span>
            <span style="background:#1a2d45;padding:6px 14px;border-radius:20px;font-size:13px">🇪🇸 La Liga</span>
            <span style="background:#1a2d45;padding:6px 14px;border-radius:20px;font-size:13px">🇩🇪 Bundesliga</span>
            <span style="background:#1a2d45;padding:6px 14px;border-radius:20px;font-size:13px">🇮🇹 Serie A</span>
            <span style="background:#1a2d45;padding:6px 14px;border-radius:20px;font-size:13px">🇫🇷 Ligue 1</span>
        </div>
        <div style="display:flex;gap:16px;margin-top:16px;flex-wrap:wrap">
            <div style="background:#0d1520;border:1px solid #1a2d45;border-radius:10px;padding:12px 20px;text-align:center">
                <div style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;color:#00ff87">1,982</div>
                <div style="font-size:11px;color:#6a8aaa;text-transform:uppercase">Jugadores</div>
            </div>
            <div style="background:#0d1520;border:1px solid #1a2d45;border-radius:10px;padding:12px 20px;text-align:center">
                <div style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;color:#00ff87">5</div>
                <div style="font-size:11px;color:#6a8aaa;text-transform:uppercase">Ligas</div>
            </div>
            <div style="background:#0d1520;border:1px solid #1a2d45;border-radius:10px;padding:12px 20px;text-align:center">
                <div style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;color:#00ff87">450+</div>
                <div style="font-size:11px;color:#6a8aaa;text-transform:uppercase">Min mínimos</div>
            </div>
            <div style="background:#0d1520;border:1px solid #1a2d45;border-radius:10px;padding:12px 20px;text-align:center">
                <div style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;color:#00ff87">165</div>
                <div style="font-size:11px;color:#6a8aaa;text-transform:uppercase">Variables</div>
            </div>
        </div>
    </div>

    <div class="grid">

        <!-- BUSCAR JUGADOR -->
        <div class="card">
            <h2>🔍 Buscar Jugador</h2>
            <label>Nombre del jugador</label>
            <input type="text" id="buscar-nombre" placeholder="Ej: Vinicius, Bellingham...">
            <button onclick="buscarJugador()">BUSCAR</button>
            <div id="buscar-resultado" class="resultado"></div>
        </div>

        <!-- MÉTRICAS POR POSICIÓN -->
        <div class="card">
            <h2>📊 Métricas por Posición</h2>
            <label>Selecciona la posición</label>
            <select id="pos-select" onchange="verMetricas()">
                <option value="">-- Selecciona --</option>
                <option value="FW">FW → Delantero</option>
                <option value="MF">MF → Mediocampista</option>
                <option value="DF">DF → Defensa</option>
                <option value="GK">GK → Portero</option>
            </select>
            <div id="metricas-resultado" class="resultado"></div>
        </div>

        <!-- ANALIZAR JUGADOR -->
        <div class="card full-width">
            <h2>⚽ Analizar Jugador</h2>
            <div class="grid">
                <div>
                    <label>Nombre</label>
                    <input type="text" id="a-player" placeholder="Nombre completo">
                    <label>Nacionalidad</label>
                    <input type="text" id="a-nation" placeholder="Ej: es ESP">
                    <label>Posición</label>
                    <select id="a-pos">
                        <option value="FW">FW → Delantero</option>
                        <option value="MF">MF → Mediocampista</option>
                        <option value="DF">DF → Defensa</option>
                        <option value="GK">GK → Portero</option>
                    </select>
                    <label>Club</label>
                    <input type="text" id="a-squad" placeholder="Ej: Real Madrid">
                </div>
                <div>
                    <label>Liga</label>
                    <input type="text" id="a-comp" placeholder="Ej: es La Liga">
                    <label>Edad</label>
                    <input type="number" id="a-age" placeholder="15 - 45" min="15" max="45">
                    <label>Minutos jugados</label>
                    <input type="number" id="a-min" placeholder="Ej: 2253" min="2" max="5400">
                    <label>Métricas por partido (separadas por coma)</label>
                    <input type="text" id="a-metricas" placeholder="Ej: 0.96, 0.36, 0.71, 0.44, 1.76">
                </div>
            </div>
            <button onclick="analizarJugador()">ANALIZAR JUGADOR</button>
            <div id="analizar-resultado" class="resultado"></div>
        </div>

        <!-- HISTORIAL -->
        <div class="card full-width">
            <h2>📋 Historial de Análisis</h2>
            <button onclick="verHistorial()" style="margin-bottom:16px">ACTUALIZAR HISTORIAL</button>
            <div id="historial-lista"></div>
        </div>

    </div>
</div>

<script>
const API = "http://127.0.0.1:8000";

// BUSCAR JUGADOR
async function buscarJugador() {
    const nombre = document.getElementById("buscar-nombre").value.trim();
    if (!nombre) return;
    const div = document.getElementById("buscar-resultado");
    div.className = "resultado visible";
    div.innerHTML = "Buscando...";
    try {
        const res = await fetch(`${API}/jugador/${nombre}`);
    if (!res.ok) { 
        div.innerHTML = `<div class="error" style="background:#0d0a0a;border:1px solid #ff4560;border-radius:10px;padding:16px">
        <b>❌ Error ${res.status} — ${res.status === 404 ? "Not Found" : "Error"}</b><br>
        <span style="color:#6a8aaa;font-size:12px">No se encontró ningún jugador con ese nombre en el dataset.</span>
        </div>`;
        return; 
    }
        const data = await res.json();
        div.innerHTML = data.map(j => `
            <div class="jugador-item" onclick="rellenarFormulario('${j.Player}','${j.Nation}','${j.Pos}','${j.Squad}','${j.Comp}',${j.Age},${j.Min})">
                <div class="nombre">${j.Player} <span class="pos-badge">${j.Pos}</span></div>
                <div class="detalle">${j.Squad} · ${j.Comp} · ${j.Age} años · ${j.Min} min</div>
                <div class="detalle" style="color:#00ff87;margin-top:4px">← Clic para rellenar el formulario</div>
            </div>
        `).join("");
    } catch(e) { div.innerHTML = '<p class="error">Error conectando con la API.</p>'; }
}

// RELLENAR FORMULARIO CON DATOS DEL JUGADOR
function rellenarFormulario(player, nation, pos, squad, comp, age, min) {
    document.getElementById("a-player").value = player;
    document.getElementById("a-nation").value = nation;
    document.getElementById("a-pos").value = pos;
    document.getElementById("a-squad").value = squad;
    document.getElementById("a-comp").value = comp;
    document.getElementById("a-age").value = age;
    document.getElementById("a-min").value = min;
    document.getElementById("a-metricas").focus();
    window.scrollTo({top: 400, behavior: 'smooth'});
}

// VER MÉTRICAS
async function verMetricas() {
    const pos = document.getElementById("pos-select").value;
    if (!pos) return;
    const div = document.getElementById("metricas-resultado");
    div.className = "resultado visible";
    try {
        const res = await fetch(`${API}/metricas/${pos}`);
        const data = await res.json();
        div.innerHTML = `
            <p class="seccion-titulo">Métricas sugeridas para ${pos}</p>
            ${data.metricas_sugeridas.map(m => `
                <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--borde)">
                    <span style="color:var(--verde);font-weight:600">${m.columna}</span>
                    <span style="font-size:13px;color:#6a8aaa">${m.descripcion}</span>
                </div>
            `).join("")}
            <p style="font-size:12px;color:#6a8aaa;margin-top:12px">💡 ${data.nota}</p>
        `;
    } catch(e) { div.innerHTML = '<p class="error">Error cargando métricas.</p>'; }
}

// ANALIZAR JUGADOR
async function analizarJugador() {
    const metricas = document.getElementById("a-metricas").value
        .split(",").map(v => parseFloat(v.trim())).filter(v => !isNaN(v));
    const body = {
        Player: document.getElementById("a-player").value,
        Nation: document.getElementById("a-nation").value,
        Pos: document.getElementById("a-pos").value,
        Squad: document.getElementById("a-squad").value,
        Comp: document.getElementById("a-comp").value,
        Age: parseInt(document.getElementById("a-age").value),
        Min: parseInt(document.getElementById("a-min").value),
        metricas_por_partido: metricas
    };
    const div = document.getElementById("analizar-resultado");
    div.className = "resultado visible";
    div.innerHTML = "Analizando...";
    try {
        const res = await fetch(`${API}/Analizar`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(body)
        });
        if (!res.ok) {
    const err = await res.json();
    let mensajeAmigable = `<b style="font-size:15px">❌ Error 422 — Unprocessable Entity</b><br><span style="color:#6a8aaa;font-size:12px">Pydantic rechazó los datos. Revisa los siguientes campos:</span>`;
    if (Array.isArray(err.detail)) {
    err.detail.forEach(e => {
        const campo = e.loc[e.loc.length - 1];
        const ubicacion = e.loc.join(" → ");
        let descripcion = "";
        if (e.type === "less_than_equal") descripcion = `el valor <b>${e.input}</b> supera el máximo permitido de <b>${e.ctx?.le}</b>`;
        else if (e.type === "greater_than_equal") descripcion = `el valor <b>${e.input}</b> es menor al mínimo permitido de <b>${e.ctx?.ge}</b>`;
        else if (e.type === "too_short") descripcion = `se ingresaron <b>${e.ctx?.actual_length}</b> métricas — se requieren mínimo <b>${e.ctx?.min_length}</b>`;
        else if (e.type === "string_too_short") descripcion = `el texto es demasiado corto`;
        else descripcion = e.msg;

        mensajeAmigable += `
        <div style="background:#1a0a0a;border:1px solid #ff4560;border-radius:8px;padding:10px 14px;margin-top:10px">
            <div style="font-size:12px;color:#6a8aaa">📍 Ubicación: <b style="color:#fff">${ubicacion}</b></div>
            <div style="font-size:12px;color:#6a8aaa">🔖 Tipo: <b style="color:#ffc800">${e.type}</b></div>
            <div style="font-size:13px;color:#ff4560;margin-top:4px">⚠️ <b>${campo}</b>: ${descripcion}</div>
        </div>`;
    });
    }
    div.innerHTML = `<div class="error" style="background:#0d0a0a;border:1px solid #ff4560;border-radius:10px;padding:16px">${mensajeAmigable}</div>`;
    return;
    }
        const d = await res.json();
        const perfilColor = d.perfil_consistencia === "Consistente" ? "badge-verde" :
                            d.perfil_consistencia === "De rachas" ? "badge-amarillo" : "badge-rojo";
        const recColor = d.recomendacion === "Fichar" ? "badge-verde" :
                         d.recomendacion === "Observar" ? "badge-amarillo" : "badge-rojo";
        div.innerHTML = `
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
                <div>
                    <div style="font-size:1.1rem;font-weight:600;color:var(--blanco)">${d.nombre}</div>
                    <div style="font-size:13px;color:#6a8aaa">${d.equipo} · ${d.liga} · ID #${d.id}</div>
                    <div style="margin-top:4px"><span style="background:rgba(0,255,135,0.15);color:#00ff87;border-radius:6px;padding:3px 10px;font-size:12px;font-weight:600">✅ 200 — OK</span></div>
                </div>
                <div>
                    <span class="badge ${perfilColor}">${d.perfil_consistencia}</span>
                    <span class="badge ${recColor}">${d.recomendacion}</span>
                </div>
            </div>
            <div class="stat-grid">
                <div class="stat"><div class="valor">${d.promedio}</div><div class="etiqueta">Promedio</div></div>
                <div class="stat"><div class="valor">${d.desvi_std}</div><div class="etiqueta">Desv. Std</div></div>
                <div class="stat"><div class="valor">${d.maximo}</div><div class="etiqueta">Máximo</div></div>
                <div class="stat"><div class="valor">${d.minimo}</div><div class="etiqueta">Mínimo</div></div>
                <div class="stat"><div class="valor">${d.varianza}</div><div class="etiqueta">Varianza</div></div>
                <div class="stat"><div class="valor">${d.rango}</div><div class="etiqueta">Rango</div></div>
            </div>
        `;
        verHistorial();
    } catch(e) { div.innerHTML = '<p class="error">Error conectando con la API.</p>'; }
}

// HISTORIAL
async function verHistorial() {
    const div = document.getElementById("historial-lista");
    try {
        const res = await fetch(`${API}/historial`);
        const data = await res.json();
        if (data.length === 0) { div.innerHTML = '<p style="color:#6a8aaa">No hay análisis aún.</p>'; return; }
        div.innerHTML = data.map(d => {
            const perfilColor = d.perfil_consistencia === "Consistente" ? "badge-verde" :
                                d.perfil_consistencia === "De rachas" ? "badge-amarillo" : "badge-rojo";
            const recColor = d.recomendacion === "Fichar" ? "badge-verde" :
                             d.recomendacion === "Observar" ? "badge-amarillo" : "badge-rojo";
            return `
            <div class="historial-item" onclick="toggleDetalle(${d.id})">
            <div class="historial-header">
                <div class="info">
                    <div class="nombre">#${d.id} ${d.nombre} <span class="pos-badge">${d.posicion}</span></div>
                    <div class="detalle">${d.equipo} · ${d.liga} · ${d.edad} años</div>
                    <div class="detalle">Prom: ${d.promedio} · Std: ${d.desvi_std} · Rango: ${d.rango}</div>
                    <div style="margin-top:6px">
                        <span class="badge ${perfilColor}">${d.perfil_consistencia}</span>
                        <span class="badge ${recColor}">${d.recomendacion}</span>
                    </div>
                </div>
                <button class="btn-rojo btn-small" onclick="event.stopPropagation();eliminar(${d.id})">ELIMINAR</button>
                 </div>
                <div id="detalle-${d.id}" style="display:none;margin-top:12px">
                <div class="stat-grid">
                    <div class="stat"><div class="valor">${d.promedio}</div><div class="etiqueta">Promedio</div></div>
                    <div class="stat"><div class="valor">${d.desvi_std}</div><div class="etiqueta">Desv. Std</div></div>
                    <div class="stat"><div class="valor">${d.maximo}</div><div class="etiqueta">Máximo</div></div>
                    <div class="stat"><div class="valor">${d.minimo}</div><div class="etiqueta">Mínimo</div></div>
                    <div class="stat"><div class="valor">${d.varianza}</div><div class="etiqueta">Varianza</div></div>
                    <div class="stat"><div class="valor">${d.rango}</div><div class="etiqueta">Rango</div></div>
                    </div>
                    </div>
                </div>`;
                }).join("");
            } catch(e) { div.innerHTML = '<p class="error">Error cargando historial.</p>'; }
}


async function eliminar(id) {
    await fetch(`${API}/historial/${id}`, {method: "DELETE"});
    verHistorial();
}

function toggleDetalle(id) {
    const div = document.getElementById(`detalle-${id}`);
    div.style.display = div.style.display === "none" ? "block" : "none";
}

// Cargar historial al inicio
verHistorial();
</script>
</body>
</html>
    """

@app.post("/Analizar", response_model=resultados, tags=["⚽ Análisis"])
def analizar_jugador(jugador: jugador_input):
    global contador_id
    contador_id += 1
    resultado = calcular_est(jugador, id_registro=contador_id)
    historial[contador_id] = resultado
    return resultado

@app.get("/historial", response_model=List[resultados], tags=["📋 Historial"])
def ver_historial():
    return list(historial.values())

@app.get("/historial/{id}", response_model=resultados, tags=["📋 Historial"])
def obtener_analisis(id: int):
    if id not in historial:
        raise HTTPException(status_code=404, detail="No se encontró el análisis con ese ID")
    return historial[id]

@app.delete("/historial/{id}", tags=["📋 Historial"])
def eliminar_analisis(id: int):
    if id not in historial:
        raise HTTPException(status_code=404, detail="No se encontró análisis con ese ID")
    del historial[id]
    return {"mensaje": "Análisis eliminado correctamente"}

@app.get("/metricas/{posicion}", tags=["📊 Métricas"])
def metricas_sugeridas(posicion: str):
    metricas = {
        "FW": [
            {"columna": "Gls/90",  "descripcion": "Goles por partido (Gls totales / partidos jugados)"},
            {"columna": "Ast/90",  "descripcion": "Asistencias por partido (Ast totales / partidos jugados)"},
            {"columna": "xG/90",   "descripcion": "Goles esperados por partido"},
            {"columna": "xAG/90",  "descripcion": "Asistencias esperadas por partido"},
            {"columna": "KP/90",   "descripcion": "Pases clave por partido (KP totales / partidos jugados)"}
        ],
        "DF": [
            {"columna": "Tkl/90",    "descripcion": "Tackles por partido (Tkl totales / partidos jugados)"},
            {"columna": "Int/90",    "descripcion": "Intercepciones por partido"},
            {"columna": "Blocks/90", "descripcion": "Bloqueos por partido"},
            {"columna": "Clr/90",    "descripcion": "Despejes por partido"},
            {"columna": "Err/90",    "descripcion": "Errores por partido"}
        ],
        "MF": [
            {"columna": "KP/90",   "descripcion": "Pases clave por partido"},
            {"columna": "PrgP/90", "descripcion": "Pases progresivos por partido"},
            {"columna": "Ast/90",  "descripcion": "Asistencias por partido"},
            {"columna": "xAG/90",  "descripcion": "Asistencias esperadas por partido"},
            {"columna": "PrgC/90", "descripcion": "Conducciones progresivas por partido"}
        ],
        "GK": [
            {"columna": "Saves/90", "descripcion": "Atajadas por partido"},
            {"columna": "Save%",    "descripcion": "Porcentaje de atajadas (ya viene en %)"},
            {"columna": "CS/90",    "descripcion": "Porterías en cero por partido"},
            {"columna": "GA/90",    "descripcion": "Goles recibidos por partido"},
            {"columna": "PKsv",     "descripcion": "Penaltis atajados en la temporada"}
        ]
    }
    if posicion not in metricas:
        raise HTTPException(status_code=404, detail="Posición no valida. Usa FW, DF, MF o GK")
    return {
        "posicion": posicion,
        "metricas_sugeridas": metricas[posicion],
        "nota": "Busca los valores por partido en fbref.com o sofascore.com y mételos en el mismo orden"
    }

@app.get("/jugador/{nombre}", tags=["🔍 Búsqueda"])
def buscar_jugador(nombre: str):
    resultado = df_jugadores[
        df_jugadores["Player"].str.contains(nombre, case=False, na=False)
    ]
    if resultado.empty:
        raise HTTPException(status_code=404, detail=f"No se encontró ningún jugador con el nombre '{nombre}'")
    return resultado[["Player", "Nation", "Pos", "Squad", "Comp", "Age", "Min"]].to_dict(orient="records")


