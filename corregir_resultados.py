"""
Script para corregir datos de resultados existentes
Añade campos faltantes (segmento, razon_no_asignacion)
"""
import json
from pathlib import Path

def corregir_resultados():
    """Corrige el archivo de resultados agregando campos faltantes"""
    
    ruta_json = Path("data/periodos/2025-2/resultados_asignacion.json")
    
    if not ruta_json.exists():
        print(f"❌ Archivo no encontrado: {ruta_json}")
        return
    
    # Leer JSON existente
    with open(ruta_json, 'r', encoding='utf-8') as f:
        resultados = json.load(f)
    
    print(f"📖 Leyendo {len(resultados)} resultados...")
    
    # Corregir cada resultado
    for resultado in resultados:
        # Agregar segmento si no existe
        if 'segmento' not in resultado:
            resultado['segmento'] = 'Población General'  # Por defecto
        
        # Agregar razon_no_asignacion si no existe
        if 'razon_no_asignacion' not in resultado:
            if resultado.get('estado_asignacion') == 'NO ASIGNADO':
                resultado['razon_no_asignacion'] = 'No había cupos disponibles en sus opciones de carrera'
            else:
                resultado['razon_no_asignacion'] = None
    
    # Guardar JSON corregido
    with open(ruta_json, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=4, ensure_ascii=False)
    
    print(f"✅ {len(resultados)} resultados corregidos exitosamente")
    print(f"✅ Guardado en: {ruta_json}")
    
    # Mostrar ejemplo
    print("\n📋 Ejemplo de resultado corregido:")
    print(json.dumps(resultados[0], indent=2, ensure_ascii=False))

if __name__ == "__main__":
    corregir_resultados()
