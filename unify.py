import os
import sys
import re
from PyPDF2 import PdfMerger  # o PdfFileMerger dependiendo de la versión
from pathlib import Path
from PyPDF2 import PdfMerger, PdfReader
import gc  # Garbage collector

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
    import re
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
                    # Leer el PDF y añadirlo
                    with open(ruta_pdf, 'rb') as file:
                        merger.append(file)
                    
                    # Mostrar progreso
                    if (i + 1) % 100 == 0 or i == fin - 1:
                        print(f"   Progreso: {i + 1 - inicio}/{fin - inicio} del lote actual")
                        
                except Exception as e:
                    print(f"   ⚠️  Error con {pdf}: {e}")
            
            # Forzar recolección de basura entre lotes
            gc.collect()
        
        print("\n💾 Guardando archivo final...")
        
        # Guardar el archivo unido
        merger.write(ruta_salida)
        merger.close()
        
        # Obtener tamaño del archivo
        tamano = os.path.getsize(ruta_salida) / (1024 * 1024 * 1024)  # Convertir a GB
        tamano_mb = os.path.getsize(ruta_salida) / (1024 * 1024)  # Convertir a MB
        
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
    
    # Detectar patrón
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
    
    # Buscar archivos en el rango
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
            # Usar el mismo método optimizado pero solo con estos archivos
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

def menu_principal():
    """Menú principal optimizado para grandes volúmenes"""
    
    print("\n" + "="*50)
    print("📚 UNIR PDFS - MODO MILES DE ARCHIVOS")
    print("="*50)
    print(f"\n📊 Detectados: {len([f for f in os.listdir('.') if f.endswith('.pdf')]):,} archivos PDF")
    print("\n1. 📄 Unir TODOS (miles de archivos) - OPTIMIZADO")
    print("2. 🔢 Unir por RANGO numérico (recomendado)")
    print("3. 🖱️  Seleccionar archivos manualmente")
    print("4. 🔍 Unir por patrón")
    print("5. ❌ Salir")
    print("\n⚠️  RECOMENDACIÓN: Usa opción 2 para procesar por rangos")
    
    opcion = input("\nSelecciona una opción (1-5): ").strip()
    
    if opcion == "1":
        unir_pdfs_optimizado()
        input("\nPresiona Enter para continuar...")
        return True
    elif opcion == "2":
        unir_pdfs_por_rango()
        input("\nPresiona Enter para continuar...")
        return True
    elif opcion == "3":
        print("🚧 Opción en desarrollo - Usa 1 o 2")
        input("Presiona Enter...")
        return True
    elif opcion == "4":
        # Tu código existente de unión por patrón
        return True
    elif opcion == "5":
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
