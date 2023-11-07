import pygame
from pygame.locals import *

from UI.GUI_button import *
from UI.GUI_slider import *
from UI.GUI_textbox import *
from UI.GUI_label import *
from UI.GUI_form import *
from UI.GUI_button_image import *
from GUI_form_menu_score import *

    
class FormPrueba(Form):
    def __init__(self, screen, x,y,w,h,color_background, color_border = "Black", border_size = -1, active = True):
        super().__init__(screen, x,y,w,h,color_background, color_border, border_size, active)

        ##COMPLETAR
        pygame.mixer.init()
        self.volumen = 0.2
        self.flag_play = True

        pygame.mixer.music.load("Recursos\Vengeance (Loopable).wav")
        pygame.mixer.music.set_volume(self.volumen)
        pygame.mixer.music.play(-1)





        self.txt_nombre = TextBox(self._slave,
                                  x,y,
                                  50,50,
                                  150,30,
                                  "Gray","White","Red","Blue",2,
                                  font="Comic Sans",font_size=15,font_color="Black")

        self.boton_play= Button(self._slave,
                                x,y,
                                100,100,
                                100,50,
                                "Red","Blue",
                                self.btn_play_click,"Nombre","Pausa",
                                font="Verdana",font_color="Black",font_size=15)
        

        self.slider_volumen = Slider(self._slave,x,y,
                                     100,200,
                                     500,15,
                                     self.volumen,"blue","white")

        self.label_volumen = Label(self._slave,650,190,10,150,
                                   "20%","Comic Sans",15,"white","Recursos\Table.png")

        self.boton_score = Button_Image(self._slave,x,y,
                                        255,100,
                                        50,50,
                                        "Recursos\Menu_BTN.png",
                                        self.btn_tabla_click,"")
        self.lista_widgets.append(self.txt_nombre)
        self.lista_widgets.append(self.boton_play)
        self.lista_widgets.append(self.slider_volumen)
        self.lista_widgets.append(self.label_volumen)
        self.lista_widgets.append(self.boton_score)

        self.render()

    def render(self):
        self._slave.fill(self._color_background)

    def update(self, lista_eventos):
        if self.verificar_dialog_result():
            if self.active:
                self.draw()
                self.render()
                for widget in self.lista_widgets:
                    widget.update(lista_eventos)
                self.update_volumen(lista_eventos)
                
        else:
            self.hijo.update(lista_eventos)

    def update_volumen(self, lista_eventos):
        self.volumen = self.slider_volumen.value
        self.label_volumen.update(lista_eventos)
        self.label_volumen.set_text(f"{round(self.volumen * 100)}%")
        pygame.mixer.music.set_volume(self.volumen)
        


        
    # @staticmethod
    def btn_play_click(self, param):
        if self.flag_play:
           pygame.mixer.music.pause()
           self.boton_play._color_background = "Cyan"
           self.boton_play.set_text("Play")
        else:
           pygame.mixer.music.unpause()
           self.boton_play._color_background = "Red"
           self.boton_play.set_text("Pause")
        self.flag_play = not self.flag_play

    def btn_tabla_click(self, param):
        diccionario = [{"Jugador":"Gio","Score":5},{"Jugador":"Marcos","Score":7},{"Jugador":"Lucas","Score":3}]
        # nuevo_form = FormMenuScore(self._master,
        #                          250,25,500,550,
        #                           (220,0,220),
        #                           (255,255,255),
        #                           True,
        #                           "Recursos\Window.png",
        #                           diccionario,
        #                           100,10,10)

        nuevo_form = FormMenuScore(screen=self._master,
                                   x=250,y=25,
                                   w=500,h=550,
                                   color_background=(220,0,220)
                                   ,color_border=(255,255,255),
                                   active=True,
                                   path_image="Recursos\Window.png",
                                   scoreboard=diccionario,
                                   margen_x=10,margen_y=100,espacio=10)

        self.show_dialog(nuevo_form)
