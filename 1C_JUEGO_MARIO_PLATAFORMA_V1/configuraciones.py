import pygame

def girar_imagenes(lista_original,flip_x,flip_y):
    lista_girada = []
    for img in lista_original:
        lista_girada.append(pygame.transform.flip(img, flip_x, flip_y))
        
    return lista_girada

def reescalar_imagenes(diccionario_animaciones, ancho, alto):
    for clave in diccionario_animaciones:
        for i in range(len(diccionario_animaciones[clave])):
            img = diccionario_animaciones[clave][i]
            diccionario_animaciones[clave][i] = pygame.transform.scale(img, (ancho, alto))
            
           
#Definimos los fotogramas de cada animacion.            

personaje_quieto = [pygame.image.load(r"Corre\0.png")]

personaje_corre = [pygame.image.load(r"Corre\1.png"),
                    pygame.image.load(r"Corre\2.png")]

personaje_salta = [pygame.image.load(r"Corre\\3.png")]


personaje_camina_izquierda = girar_imagenes(personaje_corre, True, False)

enemigo_camina = [pygame.image.load(r"Corre\ene1.png"),
                    pygame.image.load(r"Corre\ene2.png"),pygame.image.load(r"Corre\ene3.png")]

enemigo_aplasta = [pygame.image.load(r"Corre\ene3.png"),pygame.image.load(r"Corre\ene3.png")]


flor_fuego = [pygame.image.load(r"Corre\flor.png")]


super_mario= [pygame.image.load(r"Corre\sm1.png"),
                    pygame.image.load(r"Corre\sm2.png"),pygame.image.load(r"Corre\sm3.png")]