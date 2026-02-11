import os
import re
import sys
from pathlib import Path

def eliminar_duplicados():
    """
    Elimina archivos PDF duplicados que contienen números entre paréntesis en su nombre.
    Se ejecuta en la misma carpeta donde está el script.
    """
    
    # Obtener la carpeta donde está ubicado el script
    carpeta = os.path.dirname(os.path.abspath(__file__))
    
    print(f"📂 Trabajando en la carpeta: {carpeta}")
    
    # Patrón para identificar archivos duplicados: nombre_base (número).pdf
    patron_duplicado = re.compile(r'^(.+?) \(\d+\)\.pdf$')
    
    archivos_eliminados = 0
    archivos_conservados = 0
    
    print("\n🔍 Buscando archivos duplicados...\n")
    
    # Recorrer todos los archivos de la carpeta
    for archivo in os.listdir(carpeta):
        if not archivo.lower().endswith('.pdf'):
            continue
            
        # Verificar si es un archivo duplicado (tiene paréntesis con número)
        match = patron_duplicado.match(archivo)
        
        if match:
            nombre_base = match.group(1)  # Nombre sin el (número)
            archivo_original = f"{nombre_base}.pdf"
            ruta_duplicado = os.path.join(carpeta, archivo)
            ruta_original = os.path.join(carpeta, archivo_original)
            
            # Verificar si existe el archivo original
            if os.path.exists(ruta_original):
                try:
                    os.remove(ruta_duplicado)
                    archivos_eliminados += 1
                    print(f"✅ Eliminado: {archivo}")
                except Exception as e:
                    print(f"❌ Error al eliminar {archivo}: {e}")
            else:
                # Si no existe el original, renombrar el duplicado
                try:
                    os.rename(ruta_duplicado, ruta_original)
                    archivos_conservados += 1
                    print(f"🔄 Renombrado: {archivo} → {archivo_original}")
                except Exception as e:
                    print(f"❌ Error al renombrar {archivo}: {e}")
    
    # Resumen
    print("\n" + "="*50)
    print("📊 RESUMEN:")
    print(f"📁 Carpeta procesada: {carpeta}")
    print(f"🗑️  Archivos duplicados eliminados: {archivos_eliminados}")
    print(f"📝 Archivos renombrados (original no existía): {archivos_conservados}")
    print("="*50)

def previsualizar_duplicados():
    """
    Muestra una previsualización de los archivos que se eliminarían sin eliminarlos realmente.
    """
    carpeta = os.path.dirname(os.path.abspath(__file__))
    patron_duplicado = re.compile(r'^(.+?) \(\d+\)\.pdf$')
    duplicados = []
    renombrables = []
    
    print(f"\n🔍 ANALIZANDO CARPETA: {carpeta}")
    print("="*60)
    
    for archivo in os.listdir(carpeta):
        if not archivo.lower().endswith('.pdf'):
            continue
            
        match = patron_duplicado.match(archivo)
        if match:
            nombre_base = match.group(1)
            archivo_original = f"{nombre_base}.pdf"
            
            if os.path.exists(os.path.join(carpeta, archivo_original)):
                duplicados.append(archivo)
            else:
                renombrables.append((archivo, archivo_original))
    
    print(f"\n📋 ARCHIVOS ENCONTRADOS:")
    print(f"   📄 Total PDFs: {len([f for f in os.listdir(carpeta) if f.lower().endswith('.pdf')])}")
    print(f"   🔁 Duplicados con original: {len(duplicados)}")
    print(f"   📝 Duplicados sin original (se renombrarán): {len(renombrables)}")
    
    if duplicados:
        print(f"\n🗑️  Archivos que se ELIMINARÁN ({len(duplicados)}):")
        for archivo in sorted(duplicados)[:15]:  # Mostrar primeros 15
            print(f"   - {archivo}")
        if len(duplicados) > 15:
            print(f"   ... y {len(duplicados) - 15} más")
    
    if renombrables:
        print(f"\n📝 Archivos que se RENOMBRARÁN ({len(renombrables)}):")
        for dup, orig in sorted(renombrables)[:15]:
            print(f"   - {dup}")
            print(f"     → {orig}")
        if len(renombrables) > 15:
            print(f"   ... y {len(renombrables) - 15} más")
    
    return len(duplicados) + len(renombrables)

def menu_principal():
    """Muestra el menú principal y maneja la interacción con el usuario."""
    
    print("\n" + "="*50)
    print("🧹 LIMPIADOR DE PDFS DUPLICADOS")
    print("="*50)
    print("\n1. 🔍 Previsualizar archivos duplicados")
    print("2. 🗑️  Eliminar duplicados directamente")
    print("3. ❌ Salir")
    
    opcion = input("\nSelecciona una opción (1-3): ").strip()
    
    if opcion == "1":
        total = previsualizar_duplicados()
        if total > 0:
            input("\nPresiona Enter para volver al menú...")
        else:
            print("\n✨ ¡No hay archivos duplicados para procesar!")
            input("Presiona Enter para volver al menú...")
        return True
        
    elif opcion == "2":
        total = previsualizar_duplicados()
        if total > 0:
            print(f"\n⚠️  Se encontraron {total} archivos para procesar.")
            respuesta = input("¿Estás seguro de que quieres eliminarlos? (sí/no): ").lower()
            
            if respuesta in ['sí', 'si', 's', 'yes', 'y']:
                print("\n🔄 Procesando archivos...\n")
                eliminar_duplicados()
                print("\n✨ Proceso completado!")
            else:
                print("❌ Operación cancelada.")
        else:
            print("\n✨ ¡No hay archivos duplicados para eliminar!")
        
        input("\nPresiona Enter para volver al menú...")
        return True
        
    elif opcion == "3":
        print("\n👋 ¡Hasta luego!")
        return False
    
    else:
        print("\n❌ Opción no válida. Por favor, selecciona 1, 2 o 3.")
        input("Presiona Enter para continuar...")
        return True

if __name__ == "__main__":
    try:
        while menu_principal():
            pass
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrumpido por el usuario. ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        input("Presiona Enter para salir...")