import json
import csv
import os


class ExportarResultadosService:

    ARCHIVO_JSON = "data/resultados_asignacion.json"

    def exportar_csv(self, ruta_csv):
        # Debug: mostrar archivo actual
        print("DEBUG: __file__ =", os.path.abspath(__file__))
        print("DEBUG: cwd     =", os.getcwd())

        abs_file = os.path.abspath(__file__)
        base_dir = os.path.dirname(os.path.dirname(abs_file))  # carpeta del proyecto (intención)

        # Debug adicional: listar directorios y buscar ficheros parecidos
        data_dir_base = os.path.join(base_dir, "data")
        data_dir_cwd = os.path.join(os.getcwd(), "data")
        print("DEBUG: base_dir     =", base_dir)
        print("DEBUG: data_dir_base=", data_dir_base, "isdir:", os.path.isdir(data_dir_base))
        print("DEBUG: data_dir_cwd =", data_dir_cwd, "isdir:", os.path.isdir(data_dir_cwd))
        try:
            print("DEBUG: listado data_dir_base =", os.listdir(data_dir_base))
        except Exception as ex:
            print("DEBUG: no se puede listar data_dir_base:", ex)
        try:
            print("DEBUG: listado data_dir_cwd  =", os.listdir(data_dir_cwd))
        except Exception as ex:
            print("DEBUG: no se puede listar data_dir_cwd:", ex)

        # Buscar cualquier archivo con nombre parecido dentro del proyecto
        matches = []
        for root, _, files in os.walk(base_dir):
            for fn in files:
                if "resultados_asignacion" in fn.lower():
                    matches.append(os.path.join(root, fn))
        print("DEBUG: matches encontrados:", matches)

        candidatos = [
            os.path.join(base_dir, self.ARCHIVO_JSON),                      # <proyecto>/data/...
            os.path.join(base_dir, "data", os.path.basename(self.ARCHIVO_JSON)),  # alternativa
            os.path.join(os.getcwd(), self.ARCHIVO_JSON),                   # cwd/data/...
            os.path.join(os.getcwd(), "data", os.path.basename(self.ARCHIVO_JSON)),
            os.path.abspath(self.ARCHIVO_JSON)                              # ruta relativa absoluta
        ]

        # Imprimir candidatos (debug)
        for c in candidatos:
            print("DEBUG: candidato ->", c)

        # Elegir el primero que exista entre los candidatos
        ruta_json = None
        for c in candidatos:
            if os.path.exists(c):
                ruta_json = c
                break

        # Si no hay candidatos existentes, usar el primer 'match' encontrado recorriendo el proyecto
        if not ruta_json and 'matches' in locals() and matches:
            ruta_json = matches[0]
            print("DEBUG: usando match encontrado ->", ruta_json)

        if not ruta_json:
            detalles = "\n".join(candidatos)
            if 'matches' in locals() and matches:
                detalles += "\nMatches encontrados:\n" + "\n".join(matches)
            raise ValueError(
                "No hay resultados para exportar (archivo JSON no encontrado). "
                "Se comprobaron las siguientes rutas:\n" + detalles
            )

        with open(ruta_json, "r", encoding="utf-8") as f:
            try:
                resultados = json.load(f)
            except json.JSONDecodeError:
                raise ValueError("El archivo de resultados está vacío o no es un JSON válido")

        if not resultados:
            raise ValueError("No hay resultados para exportar")

        with open(ruta_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            # Encabezados
            writer.writerow([
                "ID Estudiante",
                "Nombres",
                "Apellidos",
                "Correo",
                "Nota Postulación",
                "Carrera",
                "Jornada",
                "Modalidad",
                "Estado Asignación"
            ])

            # Datos (usar .get para evitar KeyError)
            for r in resultados:
                writer.writerow([
                    r.get("id_estudiante", ""),
                    r.get("nombres", ""),
                    r.get("apellidos", ""),
                    r.get("correo", ""),
                    r.get("nota_postulacion", ""),
                    r.get("carrera", ""),
                    r.get("jornada", ""),
                    r.get("modalidad", ""),
                    r.get("estado_asignacion", "")
                ])
