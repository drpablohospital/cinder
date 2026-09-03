import os
import re
import sys
import hashlib  # <--- NUEVO
from pathlib import Path

def calcular_md5(ruta_archivo):
    """Calcula el hash MD5 de un archivo en bloques para no consumir mucha RAM."""
    hash_md5 = hashlib.md5()
    with open(ruta_archivo, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def eliminar_duplicados():
    """
    Elimina archivos PDF duplicados basándose en:
    1. Hash MD5 del contenido (prioritario)
    2. Patrón de nombre (nombre_base (número).pdf) como complemento
    """
    carpeta = os.path.dirname(os.path.abspath(__file__))
    print(f"📂 Trabajando en la carpeta: {carpeta}")
    
    # 1. ELIMINAR POR HASH MD5 (CONTENIDO IDÉNTICO)
    print("\n🔍 Paso 1: Buscando duplicados por contenido (MD5)...")
    hashes_vistos = {}
    archivos_eliminados_hash = 0
    
    archivos_pdf = [f for f in os.listdir(carpeta) if f.lower().endswith('.pdf')]
    
    for archivo in archivos_pdf:
        ruta = os.path.join(carpeta, archivo)
        try:
            md5 = calcular_md5(ruta)
            if md5 in hashes_vistos:
                # Es duplicado, lo eliminamos
                os.remove(ruta)
                archivos_eliminados_hash += 1
                print(f"   ✅ Eliminado por MD5: {archivo} (duplicado de {hashes_vistos[md5]})")
            else:
                hashes_vistos[md5] = archivo
        except Exception as e:
            print(f"   ⚠️  Error al procesar {archivo}: {e}")
    
    print(f"\n   🗑️  Eliminados por contenido: {archivos_eliminados_hash} archivos")
    
    # 2. ELIMINAR POR PATRÓN DE NOMBRE (COMPLEMENTARIO)
    print("\n🔍 Paso 2: Buscando duplicados por patrón de nombre (paréntesis)...")
    patron_duplicado = re.compile(r'^(.+?) \(\d+\)\.pdf$')
    archivos_eliminados_nombre = 0
    archivos_renombrados = 0
    
    for archivo in os.listdir(carpeta):
        if not archivo.lower().endswith('.pdf'):
            continue
            
        match = patron_duplicado.match(archivo)
        if match:
            nombre_base = match.group(1)
            archivo_original = f"{nombre_base}.pdf"
            ruta_duplicado = os.path.join(carpeta, archivo)
            ruta_original = os.path.join(carpeta, archivo_original)
            
            if os.path.exists(ruta_original):
                try:
                    os.remove(ruta_duplicado)
                    archivos_eliminados_nombre += 1
                    print(f"   ✅ Eliminado por nombre: {archivo}")
                except Exception as e:
                    print(f"   ❌ Error al eliminar {archivo}: {e}")
            else:
                try:
                    os.rename(ruta_duplicado, ruta_original)
                    archivos_renombrados += 1
                    print(f"   🔄 Renombrado: {archivo} → {archivo_original}")
                except Exception as e:
                    print(f"   ❌ Error al renombrar {archivo}: {e}")
    
    # Resumen final
    print("\n" + "="*50)
    print("📊 RESUMEN FINAL:")
    print(f"   🗑️  Eliminados por contenido (MD5): {archivos_eliminados_hash}")
    print(f"   🗑️  Eliminados por nombre (paréntesis): {archivos_eliminados_nombre}")
    print(f"   📝 Renombrados (original no existía): {archivos_renombrados}")
    print("="*50)

def menu_principal():
    print("\n" + "="*50)
    print("🧹 LIMPIADOR DE PDFS DUPLICADOS (MD5 + NOMBRE)")
    print("="*50)
    print("\n1. 🔍 Previsualizar y ejecutar limpieza")
    print("2. ❌ Salir")
    
    opcion = input("\nSelecciona una opción (1-2): ").strip()
    
    if opcion == "1":
        eliminar_duplicados()
        input("\nPresiona Enter para salir...")
        return False
    elif opcion == "2":
        return False
    else:
        print("Opción no válida.")
        return True

if __name__ == "__main__":
    while menu_principal():
        pass
