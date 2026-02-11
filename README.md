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



Comandos:
venv: source pdf_env/bin/activate
dependencias: PyMuPDF, PyPDF2
