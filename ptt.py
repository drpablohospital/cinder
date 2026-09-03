import os
import fitz  # PyMuPDF
import time

def pdf_a_txt_fitz(ruta_pdf, ruta_txt):
    """Extrae texto de un PDF usando PyMuPDF (ultrarrápido)"""
    doc = fitz.open(ruta_pdf)
    with open(ruta_txt, 'w', encoding='utf-8') as f:
        for num_pag in range(len(doc)):
            pagina = doc.load_page(num_pag)
            texto = pagina.get_text()
            f.write(texto)
            f.write('\n--- PÁGINA {} ---\n'.format(num_pag + 1))
    doc.close()

def procesar_carpeta():
    carpeta = os.path.dirname(os.path.abspath(__file__))
    pdfs = [f for f in os.listdir(carpeta) if f.lower().endswith('.pdf') and 'todos_unidos' not in f]
    
    print(f"📄 Archivos PDF a convertir: {len(pdfs)}")
    total_paginas = 0
    inicio_total = time.time()
    
    for i, pdf in enumerate(pdfs, 1):
        nombre_txt = pdf[:-4] + '.txt'
        ruta_pdf = os.path.join(carpeta, pdf)
        ruta_txt = os.path.join(carpeta, nombre_txt)
        
        print(f"\n[{i}/{len(pdfs)}] Procesando: {pdf}")
        try:
            inicio = time.time()
            doc = fitz.open(ruta_pdf)
            num_paginas = len(doc)
            total_paginas += num_paginas
            doc.close()
            
            pdf_a_txt_fitz(ruta_pdf, ruta_txt)
            fin = time.time()
            
            print(f"   ✅ {num_paginas} páginas → {nombre_txt} ({fin-inicio:.1f} seg)")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    fin_total = time.time()
    print(f"\n✅ Proceso completado en {fin_total-inicio_total:.1f} seg")
    print(f"📊 Total páginas procesadas: {total_paginas}")

if __name__ == '__main__':
    procesar_carpeta()