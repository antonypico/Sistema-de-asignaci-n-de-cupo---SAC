

class Estudiante:
    def __init__(self,idEstudiante,nombre,cedula,correo,telefono,puntaje,carreraPostulada,estadoAsignacion):
        self.idEstudiante = idEstudiante
        self.nombre = nombre
        self.cedula = cedula 
        self.correo = correo
        self.telefono = telefono
        self.puntaje = puntaje
        self.carreraPostulada = carreraPostulada
        self.estadoAsignacion = estadoAsignacion
        
    def consultarResultado(self):
        pass