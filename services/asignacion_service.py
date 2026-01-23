import json
import os

from services.postulante_service import PostulanteService
from services.oferta_academica_service import OfertaAcademicaService
from services.periodo_service import PeriodoService
from services.asignador_cupos import AsignadorCupos


class AsignacionService:

    def __init__(self):
        self.periodo_service = PeriodoService()
        self.postulante_service = PostulanteService()
        self.oferta_service = OfertaAcademicaService()

    # -------------------------------------------------
    # PROCESO PRINCIPAL
    # -------------------------------------------------

    def ejecutar_asignacion(self):
        # 👇 SOLO se leen postulantes desde el service
        postulantes = self.postulante_service.leer_postulantes()
        ofertas = self.oferta_service.leer_ofertas()

        if not postulantes:
            raise ValueError("No existen postulantes cargados para el período activo")

        if not ofertas:
            raise ValueError("No existe oferta académica cargada para el período activo")

        # 👇 RESETEAR CUPOS ANTES DE ASIGNAR (IMPORTANTE)
        self._resetear_cupos_ofertas(ofertas)
        
        # Calcular cupos totales disponibles
        cupos_totales = sum(oferta.cupos_disponibles for oferta in ofertas)
        postulantes_totales = len(postulantes)
        
        print(f"[ASIGNACIÓN] Cupos disponibles: {cupos_totales}")
        print(f"[ASIGNACIÓN] Postulantes a asignar: {postulantes_totales}")
        print(f"[ASIGNACIÓN] Ratio: {postulantes_totales}/{cupos_totales}")

        asignador = AsignadorCupos(postulantes, ofertas)
        resultados = asignador.ejecutar()

        # Guardar cupos actualizados
        self.oferta_service.guardar_ofertas(ofertas)

        # Guardar resultados
        self._guardar_resultados(resultados)
        
        # Mostrar resumen
        asignados = sum(1 for r in resultados if r.estudiante.oferta_asignada)
        no_asignados = len(resultados) - asignados
        print(f"[ASIGNACIÓN] Resultado: {asignados} asignados, {no_asignados} no asignados")
    
    def _resetear_cupos_ofertas(self, ofertas):
        """
        Resetea los cupos disponibles a sus valores originales.
        Esto asegura que no haya cupos duplicados de asignaciones previas.
        """
        for oferta in ofertas:
            oferta.cupos_disponibles = oferta.total_cupos
            print(f"[RESETEAR] {oferta.nombre_carrera}: {oferta.total_cupos} cupos")

    # -------------------------------------------------
    # GUARDAR RESULTADOS (PERIODO ACTIVO)
    # -------------------------------------------------

    def _guardar_resultados(self, resultados):
        ruta = self.periodo_service.obtener_ruta_periodo_activo()
        archivo = f"{ruta}/resultados_asignacion.json"

        data = []

        for r in resultados:
            estudiante = r.estudiante
            oferta = estudiante.oferta_asignada

            # Determinar la razón/observación
            observacion = None
            if oferta:
                # Si fue asignado
                if hasattr(estudiante, 'gano_desempate') and estudiante.gano_desempate:
                    observacion = "Ganó en el desempate"
                else:
                    observacion = "Asignación exitosa"
            else:
                # Si no fue asignado
                if hasattr(estudiante, 'perdio_desempate') and estudiante.perdio_desempate:
                    observacion = "Perdió en el desempate"
                else:
                    observacion = "No había cupos disponibles"
            
            data.append({
                "id_estudiante": estudiante.id_postulante,
                "nombres": estudiante.nombres,
                "apellidos": estudiante.apellidos,
                "correo": estudiante.correo,
                "nota_postulacion": estudiante.nota_postulacion,
                "segmento": estudiante.obtener_segmento(),
                "carrera": oferta.nombre_carrera if oferta else None,
                "jornada": oferta.jornada if oferta else None,
                "modalidad": oferta.modalidad if oferta else None,
                "estado_asignacion": "ASIGNADO" if oferta else "NO ASIGNADO",
                "razon_no_asignacion": observacion
            })

        os.makedirs(ruta, exist_ok=True)

        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
    def diagnosticar_ofertas(self):
        """
        Diagnóstico de ofertas para detectar problemas de cupos
        """
        ofertas = self.oferta_service.leer_ofertas()
        
        print("\n=== DIAGNÓSTICO DE OFERTAS ===")
        print(f"Total de carreras: {len(ofertas)}\n")
        
        cupos_totales = 0
        cupos_disponibles_totales = 0
        ofertas_sin_cupos = []
        
        for oferta in ofertas:
            print(f"Carrera: {oferta.nombre_carrera}")
            print(f"  Total cupos: {oferta.total_cupos}")
            print(f"  Cupos disponibles: {oferta.cupos_disponibles}")
            print(f"  Cupos consumidos: {oferta.total_cupos - oferta.cupos_disponibles}")
            print()
            
            cupos_totales += oferta.total_cupos
            cupos_disponibles_totales += oferta.cupos_disponibles
            
            if oferta.cupos_disponibles == 0:
                ofertas_sin_cupos.append(oferta.nombre_carrera)
        
        print(f"TOTALES:")
        print(f"  Total de cupos en el período: {cupos_totales}")
        print(f"  Cupos disponibles: {cupos_disponibles_totales}")
        print(f"  Cupos consumidos: {cupos_totales - cupos_disponibles_totales}")
        print(f"  Carreras sin cupos: {len(ofertas_sin_cupos)}")
        
        if ofertas_sin_cupos:
            print(f"  Listado: {', '.join(ofertas_sin_cupos)}")
        
        print("=" * 40 + "\n")


