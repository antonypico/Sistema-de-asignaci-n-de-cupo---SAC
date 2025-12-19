from clases.gestion_periodo import GestionPeriodo

class Universidad:
    def __init__(self, nombre):
        # Nombre de la universidad
        self.nombre = nombre
        
        # Gestor que maneja todos los periodos académicos
        self.gestor_periodos = GestionPeriodo()
        

    def mostrar_informacion(self):
        # Muestra información básica de la universidad
        print(f"Universidad: {self.nombre}")
        print("Periodos registrados:")
        self.gestor_periodos.listar_periodos()


    def crear_periodo(self, codigo, fecha_inicio, fecha_fin, descripcion=""):
        # Permite crear un nuevo periodo académico
        from clases.periodo_academico import PeriodoAcademico
        nuevo_periodo = PeriodoAcademico(codigo, fecha_inicio, fecha_fin, descripcion)
        self.gestor_periodos.agregar_periodo(nuevo_periodo)


    def buscar_periodo(self, codigo):
        # Busca un periodo académico por su código
        for p in self.gestor_periodos.periodos:
            if p.codigo == codigo:
                return p
        print(f"No se encontró ningún periodo con el código {codigo}.")
        return None
