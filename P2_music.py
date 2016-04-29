import _tkinter
import random
from math import floor
from tkinter import *

# Clase que implementa la lógica y representación del juego
class Juego4enRaya:
    def f(self):
        return "potato"
    
    def __init__(self):
        self.reiniciar_juego()
                
    def reiniciar_juego(self):
        
        self.tama_tablero = 4
        # Tablero. 0 representa casilla vacía, 1 jugador 1 (círculos), 2 jugador 2 (cruces)
        self.casillas=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        
        #Calculamos las pos. vacías
        self.posiciones_vacias = []
        
        for i in range(self.tama_tablero):
            for j in range(self.tama_tablero):
                self.posiciones_vacias.append((i,j))
        
        # jugador actual (se sortea 1 o 2)
        random.seed()
        self.jugador_actual = random.randint(1,2)
        
        # Modo, jugador vs jugador o jugador vs ai
        # -1 juego parado
        # 0 modo normal 2 jugadores
        # 1 modo 1 jugador vs ai
        self.modo=-1
    
    def colocar_ficha(self, x, y):
        "Coloca una ficha del jugador actual en la casilla x,y"
        if( self.posiciones_vacias.count((x,y)) > 0 ):
            self.casillas[x][y] = self.jugador_actual
            self.posiciones_vacias.remove((x,y))
            self.siguiente_jugador()
            return True
        else:
            return False
    
    def siguiente_jugador(self):
        "Avanza al siguiente jugador"
        self.jugador_actual = (self.jugador_actual%2)+1
        
    def comprobar_libre(self):
        "Salida: True hay casillas libres, False no hay"
        if(len(self.posiciones_vacias) == 0):
            return False
        else:
            return True

    def comprobar_victoria(self):
        "Salida: 0 no hay ganador, 1 gana jugador 1, 2 gana jugador 2, 3 empate"
        ganador = 0
        
        diagonal1 = self.casillas[0][0]
        diagonal2 = self.casillas[0][self.tama_tablero-1]
        
        i=0
        while ( ganador == 0 and i<self.tama_tablero ):
            vertical = self.casillas[i][0]
            horizontal = self.casillas[0][i]
            
            for j in range(self.tama_tablero):
                #Verticales
                if(vertical != self.casillas[i][j]):
                    vertical = 0
                #Horizontales
                if(horizontal != self.casillas[j][i]):
                    horizontal = 0

            #Comprobamos las diagonales (solo las principales, ya que son las únicas posibles)
            #Diagonal 1
            if(diagonal1 != self.casillas[i][i]):
                diagonal1 = 0
                
            #Diagonal 2
            if(diagonal2 != self.casillas[i][self.tama_tablero-1-i]):
                diagonal2=0
            #Comprobamos si hay ganador por horizontales y verticales
            ganador = horizontal or vertical
            i+=1
            
        ganador = ganador or diagonal1 or diagonal2
                
        # Como solo puede darse el caso de que haya un ganador, pero sí puede darse
        # que un jugador gane por varios sitios, hacemos un or de los valores de comprobación
        if( (ganador == 0) and (not self.comprobar_libre()) ):
            ganador = 3
            
        return ganador
        
    def realizar_movimiento_ai(self):
        "Este método va a realizar un movimiento de la AI para el jugador actual"
        # Método similar al de comprobar la victoria
                
        x=-1
        y=-1
        
        # Primero comprobamos si podemos hacer un "Ofensa"
        cuenta_diagonal1=0
        cuenta_diagonal2=0      
        
        for i in range(self.tama_tablero):
            cuenta_vertical=0
            cuenta_horizontal=0
            for j in range(self.tama_tablero):
                if(self.casillas[i][j] == self.jugador_actual):
                    cuenta_horizontal+=1
                else:
                    #Si es otra ficha, va a hacer que la cuenta no llegue a 3,
                    #Si es un hueco, no la afecta
                    cuenta_horizontal-=self.casillas[i][j]
                if(self.casillas[j][i] == self.jugador_actual):
                    cuenta_vertical+=1
                else:
                    cuenta_vertical-=self.casillas[j][i]
            if(self.casillas[i][i] == self.jugador_actual):
                cuenta_diagonal1+=1
            else:
                cuenta_diagonal1-=self.casillas[i][i]
            if(self.casillas[i][self.tama_tablero-1-i] == self.jugador_actual):
                cuenta_diagonal2+=1
            else:
                cuenta_diagonal2-=self.casillas[i][self.tama_tablero-1-i]
            
            #Buscamos dónde hay que colocar la ficha
            if( cuenta_horizontal == 3 ):
                for k in range(self.tama_tablero):
                    if(self.casillas[i][k] == 0):
                        x=i
                        y=k
                        return x,y
            if( cuenta_vertical == 3 ):
                for k in range(self.tama_tablero):
                    if(self.casillas[k][i] == 0):
                        x=k
                        y=i
                        return x,y
                
        if ( cuenta_diagonal1 == 3 ):
            for k in range(self.tama_tablero):
                    if(self.casillas[k][k] == 0):
                        x=k
                        y=k
                        return x,y
                        
        if ( cuenta_diagonal2 == 3 ):
            for k in range(self.tama_tablero):
                    if(self.casillas[k][self.tama_tablero-1-k] == 0):
                        x=k
                        y=self.tama_tablero-1-k
                        return x,y
                        
        
        # Después, probamos a realizar una acción "Defensa"
        # Igual que lo anterior, pero con el jugador siguiente
        jugador_siguiente = (self.jugador_actual%2)+1
        
        cuenta_diagonal1=0
        cuenta_diagonal2=0      
        
        for i in range(self.tama_tablero):
            cuenta_vertical=0
            cuenta_horizontal=0
            for j in range(self.tama_tablero):
                if(self.casillas[i][j] == jugador_siguiente):
                    cuenta_horizontal+=1
                else:
                    cuenta_horizontal-=self.casillas[i][j]
                    
                if(self.casillas[j][i] == jugador_siguiente):
                    cuenta_vertical+=1
                else:
                    cuenta_vertical-=self.casillas[j][j]
                    
            if(self.casillas[i][i] == jugador_siguiente):
                cuenta_diagonal1+=1
            if(self.casillas[i][self.tama_tablero-1-i] == jugador_siguiente):
                cuenta_diagonal2+=1
            
            #Buscamos dónde hay que colocar la ficha
            if( cuenta_horizontal == 3 ):
                for k in range(self.tama_tablero):
                    if(self.casillas[i][k] == 0):
                        x=i
                        y=k
                        return x,y
            
            if( cuenta_vertical == 3 ):
                for k in range(self.tama_tablero):
                    if(self.casillas[k][i] == 0):
                        x=k
                        y=i
                        return x,y     
                
        if ( cuenta_diagonal1 == 3 ):
            for k in range(self.tama_tablero):
                    if(self.casillas[k][k] == 0):
                        x=k
                        y=k
                        return x,y
                        
        if ( cuenta_diagonal2 == 3 ):
            for k in range(self.tama_tablero):
                    if(self.casillas[k][self.tama_tablero-1-k] == 0):
                        x=k
                        y=self.tama_tablero-1-k
                        return x,y

        
        #Si no, vamos a realizar una acción "Neutral"
        # Elegimos una posición vacía al azar y la marcamos      
        posicion = random.randint(0,(len(self.posiciones_vacias)-1))
        x=self.posiciones_vacias[posicion][0]
        y=self.posiciones_vacias[posicion][1]
            
        # Devolvemos el movimiento realizado
        return x,y

    
# Para instalar pygame en linux http://b3nac.tumblr.com/post/87942476533/how-to-install-pygame-for-python-34-on-ubuntu
from pygame import mixer
# Para coger el path del archivo
import os
import sys


class Conecta4:
    def __init__(self):
        #Generamos un tablero nuevo
        self.juego = Juego4enRaya()
        self.ventana_principal = Tk()
        self.music_on=False
        # El archivo tiene que estar en la misma carpeta que el código, y ejecutarlo como archivo
        path = os.path.dirname(os.path.realpath(sys.argv[0]))
        path+="/BitQuest.mp3"
        self.load_music(path)
    
    def load_music(self, path):
        mixer.init()
        mixer.music.load(path)

    def toogle_music(self):
        #Cambia el estado de la música
        self.music_on = (not self.music_on)
        if(self.music_on):
            #Empezamos el play
            mixer.music.rewind()
            mixer.music.play(-1)
        else:
            #Paramos la musica
            mixer.music.stop()
            
    # Callbacks para los botones
    def nueva_partida_pulsado_single(self):
        self.juego.reiniciar_juego()
        # Limpiamos el tablero
        self.limpiar_tablero()
        self.juego.modo=1

    def nueva_partida_pulsado_multi(self):
        self.juego.reiniciar_juego()
        # Limpiamos el tablero
        self.limpiar_tablero()
        self.juego.modo=0
        
    def limpiar_tablero(self):
        self.tablero.delete("fichas")
        self.label_estado.config(text="Cuatro en Raya")


    def click_tablero(self, event):
        # Si el modo es -1, bloqueamos el juego
        if(self.juego.modo == -1):
            return
            
        col=(event.x//100)
        row=(event.y//100)

        # Guardamos el jugador actual
        jugador = self.juego.jugador_actual
        # Si la casilla está disponible, colocamos la ficha y continuamos el juego
        # si no, no se hace nada
        if(self.juego.colocar_ficha(row,col)):
            # Dibujamos una ficha correspondiente
            self.dibujar_ficha(row, col, jugador)
            
            #Comprobamos si hay ganador
            estado = self.juego.comprobar_victoria()
            
            if(estado != 0):
                #Modo -1 es juego acabado            
                self.juego.modo=-1
                #Cambiamos el label de estado
                if(estado == 1):
                    self.label_estado.config(text="¡Gana primer jugador!")
                elif(estado == 2):
                    self.label_estado.config(text="¡Gana segundo jugador!")                
                elif(estado == 3):
                    self.label_estado.config(text = "¡Es un empate!")
                    
            # Si estamos en modo vs ai hacemos un movimiento de ai en el tablero
            if (self.juego.modo == 1):
                jugador = self.juego.jugador_actual
                row,col = self.juego.realizar_movimiento_ai()
                
                if(self.juego.colocar_ficha(row,col)):
                    self.dibujar_ficha(row,col,jugador)
                else:
                    print("Error en el juego")
                    self.ventana_principal.destroy()
                
                # Comprobamos de nuevo si hay ganador
                estado = self.juego.comprobar_victoria()
                if(estado != 0):
                    #Modo -1 es juego acabado            
                    self.juego.modo=-1
                    #Cambiamos el label de estado
                    if(estado == 1):
                        self.label_estado.config(text="¡Gana primer jugador!")
                    elif(estado == 2):
                        self.label_estado.config(text="¡Gana segundo jugador!")                
                    elif(estado == 3):
                        self.label_estado.config(text = "¡Es un empate!")
                    
            
        #Comprobamos si hay ganador

        
        
    def jugar(self):
        # Esta es la función principal
        self.ventana_principal.geometry("400x500")
        self.ventana_principal.title("4 en Raya")

        self.dibujar_ui()
        self.ventana_principal.mainloop()   
        
    def dibujar_ficha(self, row, col, jugador):
        if(jugador == 1):
            self.tablero.create_oval(col*100+30,row*100+30,col*100+70,row*100+70, outline="purple", width=4, tags="fichas")
        elif(jugador == 2):
            self.tablero.create_line(col*100+30,row*100+70,col*100+70,row*100+30, fill="blue", width=4, tags="fichas")
            self.tablero.create_line(col*100+30,row*100+30,col*100+70,row*100+70, fill="blue", width=4, tags="fichas")

        
        
    def dibujar_ui(self):
        #Primero partimos el parent en tablero, estado y boton para reiniciar juego
    
        # Colocamos un frame abajo para los dos botones de inicio        
        frame_inferior = Frame( self.ventana_principal, bd = 0, highlightbackground="black")
        frame_inferior.pack(side=BOTTOM, fill=X)
        
        #Colocamos los botones de nueva partida en el frame inferior
        boton_nueva_partida_multi = Button( frame_inferior , text = "Clic aquí para comenzar",  highlightbackground="black", bd=0, height="3", command = self.nueva_partida_pulsado_multi, bg="PURPLE", fg="WHITE", activebackground="YELLOW",activeforeground="BLACK")
        boton_nueva_partida_single = Button( frame_inferior , text = "Clic aquí para comenzar vs ai",  highlightbackground="black", bd=0, height="3", command = self.nueva_partida_pulsado_single, bg="PURPLE", fg="WHITE", activebackground="YELLOW",activeforeground="BLACK")


        boton_nueva_partida_multi.pack( side = LEFT, fill=X, expand = True)
        boton_nueva_partida_single.pack( side = RIGHT, fill=X, expand = True)
        
        #Ahora el frame superior
        frame_superior = Frame( self.ventana_principal, bd = 0, highlightbackground="black")
        frame_superior.pack(side=BOTTOM, fill=X)

        #Ahora creamos el marco de estado del juego, que será parte de la clase para poder ser modificado después
        self.label_estado = Label(frame_superior, text="Cuatro en Raya" ,  highlightbackground="black", bd=0, height="2", fg="WHITE", bg="BLUE")
        self.label_estado.pack(side=LEFT, fill=BOTH, expand = True)

        boton_musica = Button( frame_superior , text = "Música",  highlightbackground="black", bd=0, height="2", command = self.toogle_music, bg="PURPLE", fg="WHITE", activebackground="YELLOW",activeforeground="BLACK")
        boton_musica.pack( side = RIGHT)
        
        self.nuevo_tablero()
        
    def nuevo_tablero(self):
        # Dibujamos finalmente el canvas con el tablero
        self.tablero = Canvas(self.ventana_principal, height=400, width=400)
        # Callback para la posición de los clicks
        self.tablero.bind("<Button-1>", self.click_tablero)    
        self.tablero.pack()
        
        
        
        
        for i in range(4):
            self.tablero.create_line(100 * i, 0, 100 * i, 400)
            self.tablero.create_line(0, 100 * i, 400, 100 * i)
        self.tablero.create_line(0, 400, 400, 400)



juego = Conecta4()

juego.jugar()





