from configuraciones import *

staticmethod
def crear_lista(piso):
    diccionario_enemigo = {}
    diccionario_enemigo["izquierda"] = enemigo_camina
    diccionario_enemigo["aplasta"] = enemigo_aplasta
    coopa = Enemigo(diccionario_enemigo)
    coopa.rectangulo.bottom = piso["rectangulo"].top

    d = {"aplastado":diccionario_enemigo["aplasta"]}
    reescalar_imagenes(d, 50, 25)

    lista_enemigos = [coopa]

    return lista_enemigos

class Enemigo:
    def __init__(self, animaciones) -> None:
        self.animaciones = animaciones
        reescalar_imagenes(self.animaciones, 50, 50)
        self.rectangulo = self.animaciones["izquierda"][0].get_rect()
        self.rectangulo.x = 1200
        self.rectangulo.y = 600
        self.contador_pasos = 0
        self.animacion_actual = self.animaciones["izquierda"]

        self.estado_muerto = False
        self.esta_muriendo = False

    def avanzar(self):
        self.rectangulo -= 5

    def animar(self, pantalla):
        largo = len(self.animacion_actual)
        if self.contador_pasos >= largo:
            self.contador_pasos = 0
        pantalla.blit(self.animacion_actual[self.contador_pasos], self.rectangulo)
        self.contador_pasos +=1 

        if self.esta_muriendo and self.contador_pasos == largo:
            self.estado_muerto = True



    def actualizar(self, pantalla):
        if not self.estado_muerto:
            self.rectangulo.animar(pantalla)
            self.rectangulo.avanzar()