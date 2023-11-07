import pygame, sys
from pygame.locals import *
from Class_Personaje import *
from Class_Enemigo import *
from configuraciones import *
from modo import *

def crear_plataforma(path, ancho, alto, x, y, es_visible, tiene_premio=False):
    plataforma = {}
    
    if es_visible:
        plataforma["imagen"] = pygame.image.load(path)
    
        plataforma["imagen"] = pygame.transform.scale(plataforma["imagen"], (ancho,alto))
    else:
        plataforma["imagen"] = pygame.Surface((ancho, alto))
        
    plataforma["rectangulo"] = plataforma["imagen"].get_rect() 
    plataforma["rectangulo"].x = x
    plataforma["rectangulo"].y = y
    plataforma["premio"] = tiene_premio

    return plataforma

##############################INICIALIZACIONES##########################################

#############Pantalla##########
#ANCHO W - ALTO H
W,H = 1280,720
FPS = 18 #para desacelerar la pantalla

pygame.init()
RELOJ = pygame.time.Clock()
PANTALLA = pygame.display.set_mode((W,H)) # en pixeles

#Fondo
fondo = pygame.image.load(r"Corre\fondo.jpg").convert()#Acelera el juego y hace que consuma menos recursos
fondo = pygame.transform.scale(fondo, (W,H))

#PERSONAJE

diccionario = {}
diccionario["Quieto"] = personaje_quieto
diccionario["Derecha"] = personaje_corre
diccionario["Izquierda"] = personaje_camina_izquierda
diccionario["Salta"] = personaje_salta
diccionario["Super"] = super_mario



mario = Personaje(diccionario, (70,60), 50, 600,5)


#PLATAFORMAS

piso = crear_plataforma("",W,20,0,0,False)
piso["rectangulo"].top = mario.rectangulo_principal.bottom


plataforma_caño = crear_plataforma(r"Corre\Caño (2).png", 100,100,0,0,True)
plataforma_caño["rectangulo"].x = 850
plataforma_caño["rectangulo"].bottom = piso["rectangulo"].top
plataforma_invisible = crear_plataforma("", 247, 167, 950, 495, False)

enemigos = Enemigo.crear_lista(piso)


################################################FLOR

premio = crear_plataforma("", 60, 50, 703, 439, False, True)

flor = {}

flor["superficie"] = flor_fuego[0]
flor["superficie"] = pygame.transform.scale(flor["superficie"], (80, 80))
flor["rectangulo"] = flor["superficie"].get_rect()

flor["rectangulo"].bottom = premio["rectangulo"].top
flor["rectangulo"].x = 703
flor["rectangulo"].y = 360
flor["descubierta"] = False
flor["tocada"] = False




plataformas = [piso, plataforma_caño, plataforma_invisible, premio]






while True:
    RELOJ.tick(FPS) 
    for evento in pygame.event.get():
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit(0)
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            print(evento.pos)
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_TAB:
                cambiar_modo()
    keys = pygame.key.get_pressed()


    if(keys[pygame.K_RIGHT]):
        mario.que_hace = "Derecha"
    elif(keys[pygame.K_LEFT]):
        mario.que_hace = "Izquierda"
    elif(keys[pygame.K_SPACE]):
        mario.que_hace = "Salta"
    else:
        mario.que_hace = "Quieto"
        
    PANTALLA.blit(fondo,(0,0))
    PANTALLA.blit(plataforma_caño["imagen"], plataforma_caño["rectangulo"])
    
    mario.actualizar(PANTALLA, plataformas)
    for enemigo in enemigos:
        if not enemigo.esta_muriendo and not enemigo.esta_muerto:
            enemigo.actualizar(PANTALLA)

    for enemigo in enemigos[:]:
        if enemigo.esta_muerto:
            enemigos.remove(enemigo)
            del enemigo
            break
    
    mario.verificar_colision_enemigo(PANTALLA, enemigos)
    mario.romper_bloque(plataformas, flor)
    mario.verificar_colision_flor(flor)
    
    if flor["descubierta"] and not flor["tocada"]:
        PANTALLA.blit(flor["superficie"], flor["rectangulo"])

    
    if get_mode() == True:
        pygame.draw.rect(PANTALLA,"green",mario.rectangulo_principal,3)
        for plataforma in plataformas:
            pygame.draw.rect(PANTALLA,"blue",plataforma["rectangulo"],3)
        for enemigo in enemigos:
            pygame.draw.rect(PANTALLA,"red",enemigo.rectangulo,3)
    
        for enemigo in enemigos:
            pygame.draw.rect(PANTALLA,"orange",enemigo.rectangulo,3)
    pygame.display.update()