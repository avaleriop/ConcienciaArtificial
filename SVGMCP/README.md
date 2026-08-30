# SVGMCP — LLM Código vs Difusión para Planos

> **Prueba:** reproducir la lámina **BLUE VALLEY · CU-03 · Elevación ampliada de mobiliario (esc. 1:25)** con código, estética y precisa, con textos y dimensiones reales. No difusión.
> **Documentación completa:** [`DOCUMENTACION_COMPLETA.md`](DOCUMENTACION_COMPLETA.md) (15 secciones, geometría, 4 métodos, validación, comparativa)

## Qué hay aquí (`/SVGMCP`)

| Archivo | Método | Tamaño | Qué demuestra |
|---|---|---|---|
| **CU-03_elevacion_precisa.svg** | **1 — SVG puro declarativo** | 29 KB | Lámina completa de entrega, exacta a la referencia. Abrir en Chrome/Inkscape/Illustrator. Imprime a 1:25. |
| **generador_parametrico.py → CU-03_parametrico.svg** | **2 — SVG generativo paramétrico (Python)** | 14 KB | Cambias `CONFIG` (vanos, alturas, profundidades) y regeneras. Validación automática `Σ vanos = 6,67 m`. |
| **index.html** (Canvas live) | **3 — Canvas / JS procedural** | — | Mismo modelo paramétrico en vivo. Sliders para vano central / profundidad closet, recalcula cotas al vuelo. |
| *(mencionado en index)* | **4 — TikZ / DXF / PDF** | — | Export a CAD: `ezdxf`, `ReportLab`, `cairosvg.svg2pdf`. Te lo genero si lo pides. |

Previews raster (para vista rápida):
- `CU-03_preview.png` (desde SVG 1)
- `CU-03_parametrico_preview.png` (desde SVG 2)

## Fotos del resultado

Abre `index.html` en el navegador (doble click) o arrastra los `.svg` a Chrome.

```bash
open index.html
open CU-03_elevacion_precisa.svg
open CU-03_parametrico.svg
python3 generador_parametrico.py  # regenera paramétrico
```

Para PDF a escala:

```bash
pip install cairosvg
cairosvg CU-03_elevacion_precisa.svg -o CU-03.pdf
# o con rsvg:
rsvg-convert CU-03_elevacion_precisa.svg -f pdf -o CU-03.pdf
```

## Precisión verificada

```
entre_muros = 6.67 m
vano_izq (2.735) + vano_centro (1.20) + vano_der (2.735) = 6.670 m ✓
puerta ancho = 2.735 / 4 = 0.6837 m (espec 0.684 m, error <0.3 mm)
h_puerta = 2.50 m, h_superior = 0.45 m, h_zocalo = 0.08 m, h_escritorio = 0.76 m
prof_closet = 0.60 m, prof_escritorio = 0.70 m
```

Vectorial = zoom infinito, plotter, escalímetro.

## Por qué código gana a difusión aquí

| Criterio | Código | Difusión |
|---|---|---|
| Cotas | exactas al mm | alucina números |
| Texto | vectorial editable | borroso con faltas |
| Escala 1:25 | medible | sin escala |
| Editabilidad | 1 línea | regenerar y rezar |
| Capas CAD | layers/dimensions | imagen plana |
| Git | diff legible | binario |

## Cómo pedir variantes

> “Cámbiame vano central a 1,50 m y closet a 0,65 m, en DXF con layers”

Edito `CONFIG` y en segundos tienes nuevo SVG/DXF/PDF.

## Documentación

- **Completa (15 secciones):** [`DOCUMENTACION_COMPLETA.md`](DOCUMENTACION_COMPLETA.md) — análisis de lámina, geometría paramétrica exacta, detalle de los 4 métodos (SVG puro, Python, Canvas, TikZ/DXF), validación (xmllint, ET.parse, cairosvg, aritmética 6,67 m), estructura de archivos, guía de uso y export a PDF/CAD, comparativa código vs difusión, decisiones de diseño y próximos pasos.
- **Visor interactivo:** `index.html` — comparativa visual + Canvas live con sliders.

---
Generado con **Muse Spark** — 2026-08-30 — SVGMCP — 1 063 líneas código · 44 KB SVG · Validado XML + PNG
