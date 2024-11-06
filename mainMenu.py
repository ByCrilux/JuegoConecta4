from ArbolJuego import arbol
import tkinter as tk
import os

def j():
    jugar()

#ventana
FILAS, COLUMNAS = 7, 7
TAMANO_CELDA = 60
ventana = tk.Tk()
ventana.title("Conectar 4")
canvas = tk.Canvas(ventana, width=COLUMNAS * TAMANO_CELDA, height=FILAS * TAMANO_CELDA)#tablero
entrada = tk.Entry(ventana)#textbox
boton = tk.Button(ventana, text="tirar ficha", command=j)


#cargar
entrada.pack()
boton.pack()
canvas.pack()

#extras
jugador1 = " X "
jugador2 = " O "
tablero = [[" - " for _ in range(FILAS)] for _ in range(COLUMNAS)]
juego = arbol() #inicia al arbol
juego.que_jugador_en_turno(' O ') #define como primer turno a x
columna_seleccionada = -1


def dibujar_tablero():
    canvas.delete("all")
    for fila in range(FILAS):
        for col in range(COLUMNAS):
            x1 = col * TAMANO_CELDA
            y1 = fila * TAMANO_CELDA
            x2 = x1 + TAMANO_CELDA
            y2 = y1 + TAMANO_CELDA
            color = "white"
            if tablero[fila][col] == jugador1:
                color = "red"
            elif tablero[fila][col] == jugador2:
                color = "yellow"
            canvas.create_oval(x1, y1, x2, y2, fill=color, outline="blue")
            
    
def jugar():
    os.system("cls")
    v = True
    while v:

            juego.mostrar_tablero(tablero)
            dibujar_tablero()
            if juego.es_tablero_lleno(tablero): #si el tablero se llena es un empate
                print(f"empate")
                break

            #turno x
            if juego.jugador_en_turno == ' X ':
                valor = int(entrada.get())
                juego.poner_ficha_2(valor - 1, tablero)
                juego.set_tablero(tablero)
                if juego.verificar_si_hay_ganador(juego.jugador_en_turno):
                    print(f"jugador {juego.jugador_en_turno} gana")
                    break
                juego.que_jugador_en_turno(juego.jugador_en_turno) #<-cambia el turno al otro jugador
                

            #turno o
            if juego.jugador_en_turno == ' O ':
                arbolIA = arbol() #crea un nuevo arbol
                columaIA = arbolIA.elegir_mejor_columna(tablero)
                juego.poner_ficha_2(columaIA, tablero)
                juego.set_tablero(tablero)
                if juego.verificar_si_hay_ganador(juego.jugador_en_turno):
                    print(f"jugador {juego.jugador_en_turno} gana")
                    break
                juego.que_jugador_en_turno(juego.jugador_en_turno) #<-cambia el turno al otro jugador
                #os.system("cls")
            print(f'minimax eligió la columna: {columaIA + 1}')
            juego.mostrar_tablero(tablero)
            v = False

    dibujar_tablero()


if __name__ == "__main__":
    dibujar_tablero() #tablero inicial para meter un dato
    ventana.mainloop() 

 