import os
import sys
import re
import shutil  # <--- NUEVA IMPORTACIÓN
import gc
from pathlib import Path
from PyPDF2 import PdfMerger, PdfReader

def unir_pdfs_optimizado():
    """
    Une PDFs optimizado para MANEJAR MILES DE ARCHIVOS.
    """
    carpeta = os.path.dirname(os.path.abspath(__file__))
    
    print(f"📂 Carpeta de trabajo: {carpeta}")
    print(f"⚠️  Detectados múltiples archivos - Usando modo optimizado")
    
    # Buscar todos los archivos PDF
    archivos_pdf = []
    for archivo in os.listdir(carpeta):
        if archivo.lower().endswith('.pdf') and archivo != os.path.basename(__file__):
            if not archivo.startswith('~$') and not archivo.startswith('todos_unidos'):
                archivos_pdf.append(archivo)
    
    if not archivos_pdf:
        print("❌ No se encontraron archivos PDF en la carpeta.")
        return
    
    # Ordenar archivos numéricamente si es posible
    def extraer_numero(nombre):
        match = re.search(r'(\d+)', nombre)
        return int(match.group(1)) if match else 0
    
    archivos_pdf.sort(key=extraer_numero)
    
    total_archivos = len(archivos_pdf)
    print(f"\n📄 Total de archivos PDF encontrados: {total_archivos:,}")
    
    if total_archivos > 5000:
        print("⚠️  ADVERTENCIA: Estás procesando MILES de archivos.")
        print("   Esto puede tomar varios minutos y mucha memoria RAM.")
        respuesta = input("   ¿Continuar de todas formas? (s/no): ").lower()
        if respuesta not in ['s', 'si', 'sí', 'y', 'yes']:
            print("❌ Operación cancelada.")
            return
    
    # Preguntar nombre del archivo de salida
    nombre_salida = input("\n📝 Nombre para el PDF unido (Enter para 'todos_unidos.pdf'): ").strip()
    if not nombre_salida:
        nombre_salida = "todos_unidos.pdf"
    if not nombre_salida.lower().endswith('.pdf'):
        nombre_salida += '.pdf'
    
    ruta_salida = os.path.join(carpeta, nombre_salida)
    
    # Verificar si ya existe
    if os.path.exists(ruta_salida):
        respuesta = input(f"⚠️  {nombre_salida} ya existe. ¿Sobrescribir? (s/no): ").lower()
        if respuesta not in ['s', 'si', 'sí', 'y', 'yes']:
            print("❌ Operación cancelada.")
            return
    
    print("\n🔄 Uniendo PDFs (modo optimizado para miles de archivos)...")
    print("   Procesando en lotes para evitar errores de memoria...\n")
    
    try:
        merger = PdfMerger()
        
        # Procesar en lotes de 500 archivos
        lote_size = 500
        lotes = (total_archivos + lote_size - 1) // lote_size
        
        for lote in range(lotes):
            inicio = lote * lote_size
            fin = min(inicio + lote_size, total_archivos)
            
            print(f"\n📦 Lote {lote + 1}/{lotes} (archivos {inicio + 1:,} a {fin:,})")
            
            for i in range(inicio, fin):
                pdf = archivos_pdf[i]
                ruta_pdf = os.path.join(carpeta, pdf)
                
                try:
                    with open(ruta_pdf, 'rb') as file:
                        merger.append(file)
                    
                    if (i + 1) % 100 == 0 or i == fin - 1:
                        print(f"   Progreso: {i + 1 - inicio}/{fin - inicio} del lote actual")
                        
                except Exception as e:
                    print(f"   ⚠️  Error con {pdf}: {e}")
            
            gc.collect()
        
        print("\n💾 Guardando archivo final...")
        merger.write(ruta_salida)
        merger.close()
        
        tamano = os.path.getsize(ruta_salida) / (1024 * 1024 * 1024)
        tamano_mb = os.path.getsize(ruta_salida) / (1024 * 1024)
        
        print(f"\n✅ ¡PDFs unidos exitosamente!")
        print(f"📁 Archivo creado: {nombre_salida}")
        print(f"📊 Tamaño: {tamano:.2f} GB ({tamano_mb:,.0f} MB)")
        print(f"📄 Archivos procesados: {total_archivos:,}")
        print(f"⏱️  Fecha: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except MemoryError:
        print(f"\n❌ ERROR DE MEMORIA: Los archivos son demasiado grandes.")
        print("   Sugerencias:")
        print("   1. Divide en grupos más pequeños (ej: por rangos de números)")
        print("   2. Usa una computadora con más RAM")
        print("   3. Procesa en lotes separados y luego únelos")
        
    except Exception as e:
        print(f"\n❌ Error al unir los PDFs: {e}")
        print("   Tipo de error:", type(e).__name__)

def unir_pdfs_por_rango():
    """
    Une PDFs por rangos numéricos (ideal para MILES de archivos)
    """
    carpeta = os.path.dirname(os.path.abspath(__file__))
    
    print("\n🔢 UNIÓN POR RANGOS NUMÉRICOS")
    print("="*50)
    print("Útil cuando tienes MILES de archivos como:")
    print("   triageadulto_0000199091.pdf")
    print("   triageadulto_0000199195.pdf")
    
    archivos = [f for f in os.listdir(carpeta) if f.endswith('.pdf') and 'triageadulto' in f]
    if archivos:
        print(f"\n📄 Ejemplo detectado: {archivos[0]}")
    
    inicio = input("\n🏁 Número de inicio (Enter para 0000000000): ").strip()
    fin = input("🏁 Número de fin (Enter para 9999999999): ").strip()
    
    inicio = inicio.zfill(10) if inicio else "0000000000"
    fin = fin.zfill(10) if fin else "9999999999"
    
    nombre_base = input("📝 Nombre base del archivo (Enter para 'triageadulto_'): ").strip()
    if not nombre_base:
        nombre_base = "triageadulto_"
    
    archivos_rango = []
    patron = re.compile(f"{nombre_base}(\d+)\.pdf")
    
    for archivo in os.listdir(carpeta):
        match = patron.match(archivo)
        if match:
            numero = match.group(1)
            if inicio <= numero <= fin:
                archivos_rango.append(archivo)
    
    archivos_rango.sort()
    
    print(f"\n📄 Archivos en rango {inicio} - {fin}: {len(archivos_rango):,}")
    
    if len(archivos_rango) > 0:
        nombre_salida = f"{nombre_base}{inicio}_a_{fin}.pdf"
        respuesta = input(f"\n💾 ¿Guardar como '{nombre_salida}'? (s/no): ").lower()
        
        if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
            procesar_lotes(carpeta, archivos_rango, nombre_salida)

def procesar_lotes(carpeta, archivos, nombre_salida):
    """Función auxiliar para procesar lotes de archivos"""
    merger = PdfMerger()
    total = len(archivos)
    
    print(f"\n🔄 Procesando {total:,} archivos...")
    
    for i, archivo in enumerate(archivos, 1):
        try:
            with open(os.path.join(carpeta, archivo), 'rb') as f:
                merger.append(f)
            
            if i % 100 == 0:
                print(f"   Progreso: {i:,}/{total:,} ({i/total*100:.1f}%)")
                gc.collect()
                
        except Exception as e:
            print(f"   ⚠️  Error en {archivo}: {e}")
    
    ruta_salida = os.path.join(carpeta, nombre_salida)
    merger.write(ruta_salida)
    merger.close()
    
    tamano = os.path.getsize(ruta_salida) / (1024 * 1024 * 1024)
    print(f"\n✅ Completado: {nombre_salida} ({tamano:.2f} GB)")

# =============================================================================
# NUEVA FUNCIÓN: Agrupa de 1000 en 1000 y crea dbp.pdf
# =============================================================================
def agrupar_por_miles_y_unir():
    """
    Agrupa automáticamente todos los PDFs en grupos de 1000,
    crea un PDF por grupo, y luego une todos los grupos en dbp.pdf.
    """
    carpeta = os.path.dirname(os.path.abspath(__file__))
    
    print("\n" + "="*50)
    print("🤖 AGRUPACIÓN AUTOMÁTICA EN LOTES DE 1000")
    print("="*50)
    print(f"📂 Carpeta de trabajo: {carpeta}")
    
    # Archivos a excluir (resultados previos, temporales, el propio script)
    excluir = {'dbp.pdf', 'todos_unidos.pdf', os.path.basename(__file__)}
    excluir.update(f for f in os.listdir(carpeta) if f.startswith('temp_grupo_') and f.endswith('.pdf'))
    
    archivos_pdf = []
    for archivo in os.listdir(carpeta):
        if archivo.lower().endswith('.pdf') and archivo not in excluir:
            if not archivo.startswith('~$') and not archivo.startswith('.'):
                archivos_pdf.append(archivo)
    
    if not archivos_pdf:
        print("❌ No se encontraron archivos PDF para procesar.")
        return
    
    # Ordenar numéricamente (por el primer número que aparezca)
    def extraer_numero(nombre):
        match = re.search(r'(\d+)', nombre)
        return int(match.group(1)) if match else 0
    
    archivos_pdf.sort(key=extraer_numero)
    total = len(archivos_pdf)
    print(f"📄 Total de archivos PDF a procesar: {total:,}")
    
    # Crear carpeta temporal para los grupos
    temp_dir = os.path.join(carpeta, "temp_grupos")
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)
    
    tamano_grupo = 1000
    num_grupos = (total + tamano_grupo - 1) // tamano_grupo
    archivos_grupo = []  # Lista con las rutas de los PDFs de cada grupo
    
    print(f"\n🔄 Creando {num_grupos} grupos de hasta {tamano_grupo} archivos cada uno...")
    
    for i in range(num_grupos):
        inicio = i * tamano_grupo
        fin = min(inicio + tamano_grupo, total)
        grupo_actual = archivos_pdf[inicio:fin]
        
        nombre_grupo = f"temp_grupo_{i+1:04d}.pdf"
        ruta_grupo = os.path.join(temp_dir, nombre_grupo)
        archivos_grupo.append(ruta_grupo)
        
        print(f"\n📦 Grupo {i+1}/{num_grupos}: {len(grupo_actual)} archivos → {nombre_grupo}")
        
        merger = PdfMerger()
        for idx, archivo in enumerate(grupo_actual, 1):
            try:
                with open(os.path.join(carpeta, archivo), 'rb') as f:
                    merger.append(f)
                if idx % 200 == 0:
                    print(f"   Progreso: {idx}/{len(grupo_actual)}")
            except Exception as e:
                print(f"   ⚠️  Error en {archivo}: {e}")
        
        try:
            merger.write(ruta_grupo)
            print(f"   ✅ Grupo guardado: {nombre_grupo}")
        except Exception as e:
            print(f"   ❌ Error al guardar grupo: {e}")
        finally:
            merger.close()
            gc.collect()
    
    # ===== UNIÓN FINAL =====
    print("\n🔄 Uniendo todos los grupos en dbp.pdf...")
    ruta_final = os.path.join(carpeta, "dbp.pdf")
    
    # Verificar si ya existe
    if os.path.exists(ruta_final):
        resp = input("⚠️  dbp.pdf ya existe. ¿Sobrescribir? (s/no): ").strip().lower()
        if resp not in ['s', 'si', 'sí', 'y', 'yes']:
            print("❌ Operación cancelada.")
            shutil.rmtree(temp_dir, ignore_errors=True)
            return
    
    merger_final = PdfMerger()
    for idx, archivo_grupo in enumerate(archivos_grupo, 1):
        try:
            with open(archivo_grupo, 'rb') as f:
                merger_final.append(f)
            print(f"   Añadido grupo {idx}/{num_grupos}: {os.path.basename(archivo_grupo)}")
        except Exception as e:
            print(f"   ⚠️  Error al leer grupo {archivo_grupo}: {e}")
    
    try:
        merger_final.write(ruta_final)
        tamano = os.path.getsize(ruta_final) / (1024 * 1024 * 1024)  # GB
        print(f"\n✅ dbp.pdf creado exitosamente ({tamano:.2f} GB)")
    except Exception as e:
        print(f"❌ Error al guardar dbp.pdf: {e}")
    finally:
        merger_final.close()
    
    # Limpiar carpeta temporal
    print("\n🧹 Limpiando archivos temporales...")
    shutil.rmtree(temp_dir, ignore_errors=True)
    print("✅ Limpieza completada.")

def menu_principal():
    """Menú principal optimizado para grandes volúmenes"""
    
    print("\n" + "="*50)
    print("📚 UNIR PDFS - MODO MILES DE ARCHIVOS")
    print("="*50)
    
    # Contar PDFs excluyendo resultados típicos
    excluir_contar = {'dbp.pdf', 'todos_unidos.pdf'}
    num_pdfs = sum(1 for f in os.listdir('.') 
                   if f.lower().endswith('.pdf') and f not in excluir_contar)
    print(f"\n📊 Detectados: {num_pdfs:,} archivos PDF (sin contar resultados previos)")
    
    print("\n1. 📄 Unir TODOS (miles de archivos) - OPTIMIZADO")
    print("2. 🔢 Unir por RANGO numérico (recomendado)")
    print("3. 🖱️  Seleccionar archivos manualmente")
    print("4. 🔍 Unir por patrón")
    print("5. 🤖 Agrupar automáticamente de 1000 en 1000 y crear dbp.pdf (NUEVO)")
    print("6. ❌ Salir")
    print("\n⚠️  RECOMENDACIÓN: Usa opción 5 para miles de archivos sin intervención manual")
    
    opcion = input("\nSelecciona una opción (1-6): ").strip()
    
    if opcion == "1":
        unir_pdfs_optimizado()
        input("\nPresiona Enter para continuar...")
        return True
    elif opcion == "2":
        unir_pdfs_por_rango()
        input("\nPresiona Enter para continuar...")
        return True
    elif opcion == "3":
        print("🚧 Opción en desarrollo - Usa 1, 2 o 5")
        input("Presiona Enter...")
        return True
    elif opcion == "4":
        print("🚧 Opción en desarrollo - Usa 1, 2 o 5")
        input("Presiona Enter...")
        return True
    elif opcion == "5":
        agrupar_por_miles_y_unir()
        input("\nPresiona Enter para continuar...")
        return True
    elif opcion == "6":
        return False
    else:
        input("Opción no válida. Enter para continuar...")
        return True

if __name__ == "__main__":
    try:
        while menu_principal():
            pass
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!")