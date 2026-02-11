DIARIO

MATERIALES Y MÉTODOS

1. Archivos .pdf recabados: 36,581 (Tres computadoras de triage)

2. Script "dupdel.py"
Archivos .pdf eliminados por duplicado: 11,483. Archivos restantes: 25,098

3. Script "unify2.py"
Fusiona todos los archivos .pdf en grupos de mil.

4. Script "ptt.py"
Convierte archivos .pdf fusionados en formato .txt

5. Script "unitxt.py"
Se unieron los archivos .txt en uno solo, resultando en 50 mb de información.

6. Containers 1 y 2 de cinder.ipynb
Scripts que procesan el archivo .txt, extraen información para generar un .csv con campos ordenados.
Se obtuvo un archivo .csv con 25,098 registros estructurados.

7. Container 3 de cinder.ipynb
Se seleccionaron automáticamente casos que contengan las siguientes palabras clave:
| Categoría	| Ejemplos
| Sobredosis | Ingesta	SOBREINGESTA, SOBREDOSIS, PASTILLAS, INTENTO SUICIDA, AUTOLISIS
| Animales |	ARAÑA, SERPIENTE, CASCABEL, VIUDA NEGRA, VIOLINISTA, ALACRAN, ESCORPION, ABEJA
| Sustancias químicas |	CLORO, GAS, DETERGENTE, RODENTICIDA, INSECTICIDA, HERBICIDA, PLAGUICIDA
| Drogas | Fármacos	ETANOL, COCAINA, MARIHUANA, OPIOIDES, BENZODIAZEPINAS, PARACETAMOL
| Términos clínicos	| INTOXICACION, ENVENENAMIENTO, TOXINDROME, VENENO, MORDEDURA, PICADURA
| Raíces | TOXIC, VENEN, PICAD, MORD, SOBRED, INGEST, SUICID, AUTOLIS
Se obtuvieron 2,131 registros de casos que probablemente corresponda a un caso relativo a la toxicología.



Libreta de comandos:
Activar venv: source pdf_env/bin/activate | dependencias: PyMuPDF, PyPDF2
