from configuraciones import *

class Personaje:
    def __init__(self, animaciones, tamaño, pos_x, pos_y, velocidad):
        self.animaciones = animaciones
        reescalar_imagenes(self.animaciones, *tamaño)
        self.rectangulo_principal = animaciones["Quieto"][0].get_rect()
        self.rectangulo_principal.x = pos_x
        self.rectangulo_principal.y = pos_y
        self.velocidad = velocidad
        self.contador_pasos = 0
        self.que_hace = "Quieto"
        self.animacion_actual = self.animaciones["Quieto"]
        
        ####SALTO######
        self.desplazamiento_y = 0 
        self.potencia_salto = -25 
        self.limite_velocidad_salto = 25 
        self.esta_saltando = False
        self.gravedad = 1 

        ###SUPER MARIO####

        self.habilidad_especial = False
        self.tiempo_habilidad_especial = 10000
        self.tiempo_anterior = 0
        


    def caminar(self, pantalla):
        velocidad_actual =  self.velocidad
        if self.que_hace == "Izquierda":
            velocidad_actual *= -1
            
        nueva_posicion = self.rectangulo_principal.x + velocidad_actual
        if nueva_posicion > 0 and nueva_posicion <= (pantalla.get_width() - self.rectangulo_principal.width):
            self.rectangulo_principal.x += velocidad_actual


    def animar(self, pantalla):
        largo = len(self.animacion_actual)
        if self.contador_pasos >= largo:
            self.contador_pasos = 0
        pantalla.blit(self.animacion_actual[self.contador_pasos], self.rectangulo_principal)
        self.contador_pasos +=1
    
    
    def actualizar(self, pantalla, plataformas):

        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual > self.tiempo_habilidad_especial + self.tiempo_anterior:
            self.habilidad_especial = False

        if self.habilidad_especial:
            self.animacion_actual = self.animaciones["Super"]
        else:
            self.animacion_actual = self.animaciones[self.que_hace]

        match self.que_hace:
            case "Derecha":
                if not self.esta_saltando:
                    # self.animacion_actual = self.animaciones["Derecha"]
                    self.animar(pantalla)
                self.caminar(pantalla)
            case "Izquierda":
                if not self.esta_saltando:
                    # self.animacion_actual = self.animaciones["Izquierda"]
                    self.animar(pantalla)
                self.caminar(pantalla)
            case "Salta":
                if not self.esta_saltando:
                    self.esta_saltando = True
                    self.desplazamiento_y = self.potencia_salto
                    # self.animacion_actual = self.animaciones["Salta"]
            case "Quieto":
                if not self.esta_saltando:
                    # self.animacion_actual = self.animaciones["Quieto"]
                    self.animar(pantalla)
                
        self.aplicar_gravedad(pantalla, plataformas)

    
    def aplicar_gravedad(self, pantalla, plataformas):
        
        if self.esta_saltando:
            self.animar(pantalla)
            self.rectangulo_principal.y += self.desplazamiento_y
            if self.desplazamiento_y + self.gravedad < self.limite_velocidad_salto:
                self.desplazamiento_y += self.gravedad
    
        for pl in plataformas:
            if not pl["premio"]:
                if self.rectangulo_principal.colliderect(pl["rectangulo"]):
                    self.esta_saltando = False
                    self.desplazamiento_y = 0
                    self.rectangulo_principal.bottom = pl["rectangulo"].top  
                    break
                else:
                    self.esta_saltando = True

    def verificar_colision_enemigo(self, pantalla, lista_enemigos):
        for enemigo in lista_enemigos:
            if self.rectangulo_principal.colliderect(enemigo.rectangulo):
                enemigo.animacion_actual = enemigo.animaciones["aplasta"]
                enemigo.animar(pantalla)
                enemigo.esta_muriendo = True
                enemigo.rectangulo.y += 3
    
    def romper_bloque(self, lista_plataformas, flor):
        for plataforma in lista_plataformas:
            if plataforma["premio"]:
                if self.rectangulo_principal.colliderect(plataforma["rectangulo"]):
                    flor["descubierta"] = True
                    plataforma["premio"] = False

    def verificar_colision_flor(self,flor):
        if flor["descubierta"]:
            if self.rectangulo_principal.colliderect(flor["rectangulo"]):
                flor["tocada"] = True
                flor["descubierta"] = False
                self.tiempo_anterior = pygame.time.get_ticks()
                self.habilidad_especial = True