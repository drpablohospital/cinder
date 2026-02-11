import os
import glob

def unir_txts(con_separador=True):
    """
    Une todos los archivos .txt de la carpeta actual en un solo archivo.
    Args:
        con_separador (bool): Si True, añade cabecera con nombre de archivo entre cada TXT.
    """
    carpeta = os.path.dirname(os.path.abspath(__file__))
    
    # Buscar todos los archivos .txt (excluir el propio script y el archivo de salida)
    archivos_txt = [f for f in glob.glob(os.path.join(carpeta, "*.txt")) 
                    if os.path.basename(f) != os.path.basename(__file__)
                    and os.path.basename(f) != "base_unificada.txt"]
    
    archivos_txt.sort()  # Orden alfabético
    
    if not archivos_txt:
        print("❌ No se encontraron archivos .txt en la carpeta.")
        return
    
    print(f"📄 Archivos TXT encontrados: {len(archivos_txt)}")
    
    # Nombre del archivo de salida
    salida = os.path.join(carpeta, "base_unificada.txt")
    
    # Calcular tamaño total aproximado (para referencia)
    tamano_total_mb = sum(os.path.getsize(f) for f in archivos_txt) / (1024 * 1024)
    print(f"📊 Tamaño total estimado: {tamano_total_mb:.2f} MB")
    
    try:
        with open(salida, 'w', encoding='utf-8') as outfile:
            for i, archivo in enumerate(archivos_txt, 1):
                nombre = os.path.basename(archivo)
                print(f"   [{i}/{len(archivos_txt)}] Procesando: {nombre}")
                
                if con_separador:
                    outfile.write(f"\n{'='*80}\n")
                    outfile.write(f"--- INICIO DE: {nombre} ---\n")
                    outfile.write(f"{'='*80}\n\n")
                
                # Leer y escribir línea por línea (no carga todo en memoria)
                with open(archivo, 'r', encoding='utf-8') as infile:
                    for linea in infile:
                        outfile.write(linea)
                
                if con_separador:
                    outfile.write(f"\n{'='*80}\n")
                    outfile.write(f"--- FIN DE: {nombre} ---\n")
                    outfile.write(f"{'='*80}\n\n")
        
        tamano_final = os.path.getsize(salida) / (1024 * 1024)
        print(f"\n✅ Archivo unificado creado: base_unificada.txt")
        print(f"📊 Tamaño final: {tamano_final:.2f} MB")
        print(f"📍 Ubicación: {salida}")
        
    except Exception as e:
        print(f"\n❌ Error al unir archivos: {e}")

def menu():
    print("\n" + "="*50)
    print("📚 UNIR TXTS - Base de datos unificada")
    print("="*50)
    print("\n1. 🔗 Unir con separadores (recomendado)")
    print("2. 📦 Unir sin separadores (un solo bloque)")
    print("3. ❌ Salir")
    
    opcion = input("\nSelecciona una opción (1-3): ").strip()
    
    if opcion == "1":
        unir_txts(con_separador=True)
    elif opcion == "2":
        unir_txts(con_separador=False)
    elif opcion == "3":
        return False
    else:
        print("❌ Opción no válida.")
    
    input("\nPresiona Enter para continuar...")
    return True

if __name__ == "__main__":
    while menu():
        pass
    print("👋 ¡Hasta luego!")