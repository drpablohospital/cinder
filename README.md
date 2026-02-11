¡Me encanta! Vamos a dejar la bitácora **impecable, profesional y lista para GitHub**. Aquí tienes el **README.md** completo, con **markdown limpio, tablas, emojis técnicos y estructura de paper**.

---

# 📓 Diario de Procesamiento - Proyecto CINDER  
**Análisis retrospectivo de intoxicaciones agudas en un hospital de tercer nivel**  
*De 36,581 PDFs a fenotipos clínicos: un pipeline de minería de datos toxicológicos*

---

## 🧭 **1. Objetivo**
Construir una base de datos estructurada, limpia y enriquecida a partir de **hojas de valoración inicial de adultos (triage)** para identificar factores asociados a gravedad en intoxicaciones agudas, mediante técnicas de **procesamiento de lenguaje natural (NLP)**, **minería de datos** y **aprendizaje no supervisado**.

---

## 📦 **2. Materiales y Métodos**

### 2.1. Fuente de datos
- **Archivos fuente**: 36,581 PDFs extraídos de **3 computadoras del servicio de Urgencias** (formato `triageadulto_0000xxxxx.pdf`).
- **Período**: Enero 2025 – Febrero 2026.
- **Contenido**: Hoja de Valoración Inicial - Adultos (formato institucional homogéneo).

---

### 2.2. Pipeline de procesamiento

| **Etapa** | **Script** | **Descripción** | **Resultado** |
|-----------|------------|-----------------|---------------|
| **1. Deduplicación** | `dupdel.py` | Eliminación de archivos duplicados (mismo nombre con sufijos `(1)`, `(2)`, etc.). | **11,483** eliminados · **25,098** restantes |
| **2. Unión de PDFs** | `unify2.py` | Fusión de archivos en lotes de ~1,000 páginas para evitar errores de memoria. | 26 archivos PDF (~1,000 páginas c/u) |
| **3. Extracción de texto** | `ptt.py` | Conversión de PDF a TXT (PyMuPDF / pdftotext). | 26 archivos TXT (~50 MB total) |
| **4. Unificación de texto** | `unitxt.py` | Concatenación de todos los TXT en un solo archivo. | `base_unificada.txt` (50 MB) |
| **5. Extracción estructurada** | `cinder_containers_1y2.ipynb` | Parsing del texto mediante expresiones regulares. Generación de CSV con 22 campos (demografía, signos vitales, NEWS‑2, diagnóstico, etc.). | `db-cinder.csv` · **25,098 registros** |
| **6. Filtrado toxicológico (amplio)** | `cinder_container_3.ipynb` | Selección automática por **80+ palabras clave** (sobredosis, tóxicos, animales, drogas, raíces léxicas). | `db-cinder-a.csv` · **2,131 registros** |
| **7. Filtrado toxicológico (estricto)** | `cinder_container_4.ipynb` | Filtros contextuales: solo especialidad URGENCIAS, exclusión de mordeduras no ponzoñosas, patrones de alta certeza. | `db-cinder-toxi.csv` · **195 registros** ✅ |
| **8. Análisis exploratorio y enriquecimiento** | `cinder_container_5.ipynb` | • Extracción de variables semánticas (tóxico principal, intencionalidad, polifarmacia, co‑ingesta de alcohol).<br>• Clustering no supervisado (k-means) para fenotipos.<br>• Random Forest para importancia de variables.<br>• Correlaciones de Spearman. | `db-cinder-toxi-enriquecida.csv` · **34 columnas** |
| **9. Dashboard interactivo** | `cinder_dashboard_avanzado.ipynb` | Generación de reporte HTML con 15+ visualizaciones (clusters, reglas de gravedad, distribuciones, análisis semántico). | `dashboard_toxicologico_avanzado_.html` |

---

## 🧪 **3. Variables derivadas (enriquecimiento)**

| **Variable** | **Descripción** | **Método de extracción** |
|-------------|-----------------|---------------------------|
| `tox_*` (8 categorías) | Tipo de tóxico mencionado (benzodiacepinas, antidepresivos, alcohol, etc.) | Búsqueda por diccionario en `motivo_atencion` + `impresion_diagnostica` |
| `intencional` | Intento autolítico / suicida | Patrón regex: `intento\|autolisis\|suicida\|autoagresion` |
| `num_farmacos` | Número de fármacos distintos mencionados | Conteo de coincidencias de lista predefinida |
| `con_alcohol` | Co‑ingesta de alcohol | Presencia de `alcohol\|etanol` en texto |
| `tipo_toxico_principal` | Categoría del primer tóxico detectado | Orden de prioridad según diccionario |
| `cluster` | Fenotipo clínico (k-means, k=3) | Escalamiento y clustering sobre `[edad, NEWS‑2, FC, SpO₂, num_farmacos]` |
| `regla_gravedad` | Regla de árbol de decisión: `FR > 22.5 AND TAS ≤ 91.5` | Aplicación directa sobre columnas numéricas |

---

## 📊 **4. Resultados principales**

### 4.1. Perfil demográfico (n = 195)
- **Edad mediana**: 29 años (RIC: 22–38)
- **Género**: 61% mujeres, 39% hombres
- **Procedencia**: 78% CDMX, 9% Estado de México
- **Nivel de atención**: 69% nivel III, 30% nivel II

### 4.2. Características clínicas
- **NEWS‑2 promedio**: 3.7 ± 2.3 (rango 0–12)
- **Intencionalidad**: 41% de los casos (n=80)
- **Polifarmacia**: media de 0.8 fármacos por caso; máximo 6
- **Tóxico principal más frecuente**: benzodiacepinas (38%), seguido de alcohol (22%)

### 4.3. Fenotipos identificados (clusters)

| **Fenotipo** | **Edad** | **NEWS‑2** | **FC** | **SpO₂** | **Nº fármacos** | **Interpretación clínica** |
|--------------|----------|------------|--------|----------|------------------|----------------------------|
| **Cluster 0** | 26.8 | 3.8 | 86.7 | 94.2 | **2.1** | Joven · Polifarmacia · Intencional · Gravedad moderada |
| **Cluster 1** | 33.9 | **2.4** | 83.3 | **95.2** | **0.1** | Adulto · Sin polifarmacia · Gravedad baja |
| **Cluster 2** | 33.2 | **5.8** | **114.4** | 93.2 | 0.2 | Mayor · Taquicardia/Hipoxemia · Gravedad alta |

### 4.4. Predictores de gravedad (NEWS‑2 ≥ 5)
- **Random Forest** (importancia):
  1. Frecuencia respiratoria (FR) – **0.24**
  2. Tensión arterial sistólica (TAS) – **0.18**
  3. Frecuencia cardíaca (FC) – **0.14**
- **Regla de decisión**:  
  `FR > 22.5` **Y** `TAS ≤ 91.5` → **100%** de estos casos presentan NEWS‑2 ≥ 5  
  *(n=11; especificidad 100%, sensibilidad 18%)*

### 4.5. Correlaciones destacadas (Spearman)
- `SpO₂` vs `NEWS‑2`: **r = –0.41** (p < 0.001)
- `FC` vs `NEWS‑2`: **r = +0.32** (p < 0.001)
- `num_farmacos` vs `edad`: **r = –0.23** (p = 0.001)  
  *→ Los jóvenes ingieren más fármacos, pero esto no se asocia a mayor gravedad.*

### 4.6. Intencionalidad y gravedad
- **No se encontró asociación significativa** entre `intencional` y `NEWS‑2` (p = 0.43).
- **Hipótesis**: La gravedad depende del tóxico y la dosis, no de la intencionalidad.

---

## 📁 **5. Estructura final de archivos**

```
📂 proyecto-cinder/
│
├── 📜 README.md
├── 📜 dupdel.py
├── 📜 unify2.py
├── 📜 ptt.py
├── 📜 unitxt.py
│
├── 📓 cinder_containers_1y2.ipynb   # Extracción inicial → db-cinder.csv
├── 📓 cinder_container_3.ipynb      # Filtro amplio → db-cinder-a.csv
├── 📓 cinder_container_4.ipynb      # Filtro estricto → db-cinder-toxi.csv
├── 📓 cinder_container_5.ipynb      # Enriquecimiento + clustering → db-cinder-toxi-enriquecida.csv
├── 📓 cinder_dashboard_avanzado.ipynb  # Dashboard HTML
│
├── 📊 db-cinder.csv
├── 📊 db-cinder-a.csv
├── 📊 db-cinder-toxi.csv
├── 📊 db-cinder-toxi-enriquecida.csv
│
└── 📈 dashboard_toxicologico_avanzado_20260211_XXXXXX.html
```

---

## 🧠 **6. Conclusiones**

1. **El paciente intoxicado tipo** en nuestra unidad es: **mujer, 29 años, ingesta medicamentosa intencional, llega entre las 17‑19 h, con NEWS‑2 leve‑moderado (3‑4)**.
2. **La frecuencia respiratoria es el predictor más infravalorado**: supera a la SpO₂ en importancia para NEWS‑2 ≥ 5.
3. **Existen tres fenotipos clínicos diferenciados** con implicaciones pronósticas y terapéuticas.
4. **La polifarmacia es un marcador de juventud e intencionalidad, no de gravedad**.
5. **La regla `FR > 22.5 + TAS ≤ 91.5`** identifica un subgrupo de alto riesgo con especificidad perfecta en nuestra muestra.

---

## 🚀 **7. Próximos pasos**

- Validación prospectiva de la regla de gravedad.
- Inclusión de **tiempo desde la ingesta** como variable.
- Desarrollo de una **calculadora de riesgo** para triage.
- Redacción de artículo científico para revista de toxicología.

---

## 👨‍⚕️ **8. Autoría y contacto**

**Proyecto CINDER** (Clinical INtelligence for Drug Emergency Response)  
Desarrollado por: *Sindy Ortega, José Pablo Fernández Magaña*  
Contacto: *drpablo.hospital@gmail.com*  
Institución: *[Hospital General Dr. Gea González]*  
Fecha de cierre: **11 de febrero de 2026, 23:59 h (tiempo del oriente, reina el silencio).**

---

> *“De 36,581 PDFs a 195 vidas que podemos entender mejor.”*  
> — Cierre de trabajos, media noche en punto. 🕛

---
