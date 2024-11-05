import math
import random
from NodoJuego import nodo  # Supongo que tu clase nodo está bien definida

class arbol(nodo):
    def __init__(self):
        self.raiz = None
        self.jugador_en_turno = None
    
    def iniciar(self):
        self.raiz = nodo(7)  # Raíz inicial con 7 columnas
    
    def que_jugador_en_turno(self, jugador):
        self.jugador_en_turno = ' O ' if jugador == ' X ' else ' X '

    def poner_ficha_2(self, columnaEnviada, tablero):
        nuevoNodo = nodo(tablero) 
        nuevoNodo.set_tablero(tablero)
        nuevoNodo.poner_ficha(columnaEnviada, self.jugador_en_turno)
    
    def es_tablero_lleno(self, tablero):
        nodoActual = nodo(tablero)
        for i in range(7):
            if not nodoActual.es_columna_llena(i):
                return False
        return True
    
    def mov_validos(self, tablero):
        nodoActual = nodo(tablero)
        mv = []
        for i in range(7):
            if not nodoActual.es_columna_llena(i):
                mv.append(i)
        return mv


    def elegir_mejor_columna(self, tablero):
        nodoActual = nodo(tablero)
        self.raiz = nodoActual  # Definir la raíz del árbol
        mejor_columna = -1
        mejor_valor = -float('inf')

        for col in range(nodoActual.cantidad_columas_no_llenas()):
            if not nodoActual.es_columna_llena(col):
                # Crear hijo por cada jugada a realizar
                hijo = nodo([fila[:] for fila in nodoActual.get_tablero()])  # Copiar tablero
                hijo.poner_ficha(col, ' O ')  # IA juega en columna 'col'
                nodoActual.set_hijo(col, hijo)  # Añadir el nodo hijo
                resultado = self.minimax(hijo, 5, False, -math.inf, math.inf) #resultado [columna,valor]
                if resultado[1] > mejor_valor:
                    mejor_valor = resultado[1]
                    mejor_columna = col

        return mejor_columna
    
    def evaluar_tablero(self, tablero, ficha):
        puntuacion = 0
        columna_central = len(tablero[0]) // 2

        #toma mas prio el centro del tablero
        centro = [tablero[fila][len(tablero[0]) // 2] for fila in range(len(tablero))]
        centro_fichas = centro.count(ficha) 
        puntuacion += centro_fichas * 250  #aqui se da mas relevancia a las fichas del centro

        #valuar diferentes combinaciones de fichas consecutivas
        def evaluar_combinacion(combinacion, ficha):
            puntuacion = 0
            oponente =  ' X ' if ficha == ' O ' else ' O '

            if combinacion.count(ficha) == 4:  #4 en línea
                puntuacion += 1000
            elif combinacion.count(ficha) == 3 and combinacion.count(' - ') == 1:  #3 en línea con espacio
                puntuacion += 700
            elif combinacion.count(ficha) == 2 and combinacion.count(' - ') == 2:  #2 en línea con espacio
                puntuacion += 500
            elif combinacion.count(oponente) == 3 and combinacion.count(' - ') == 1:
                puntuacion -= 750  # Penalización por no bloquear al oponente

            return puntuacion

        # Evaluar líneas horizontales
        for fila in range(len(tablero)):
            for col in range(len(tablero[0]) - 3):
                combinacion = tablero[fila][col:col + 4]  # 4 fichas consecutivas
                puntuacion += evaluar_combinacion(combinacion, ficha)

        # Evaluar líneas verticales
        for col in range(len(tablero[0])):
            for fila in range(len(tablero) - 3):
                combinacion = [tablero[fila + i][col] for i in range(4)]  # 4 fichas consecutivas
                puntuacion += evaluar_combinacion(combinacion, ficha)

        # Evaluar diagonales (de izquierda a derecha)
        for fila in range(len(tablero) - 3):
            for col in range(len(tablero[0]) - 3):
                combinacion = [tablero[fila + i][col + i] for i in range(4)]  # 4 fichas consecutivas en diagonal
                puntuacion += evaluar_combinacion(combinacion, ficha)

        # Evaluar diagonales (de derecha a izquierda)
        for fila in range(len(tablero) - 3):
            for col in range(3, len(tablero[0])):
                combinacion = [tablero[fila + i][col - i] for i in range(4)]  # 4 fichas consecutivas en diagonal inversa
                puntuacion += evaluar_combinacion(combinacion, ficha)

        return puntuacion
    
    def minimax(self, nodoActual: nodo, profundidad, esMaximizador, alfa, beta):

        lista_movimientos_validos = self.mov_validos(nodoActual.get_tablero())  
        es_terminal = len(lista_movimientos_validos) == 0 or nodoActual.verificar_si_hay_ganador(' X ') or nodoActual.verificar_si_hay_ganador(' O ')

        if profundidad == 0 or es_terminal:
            if es_terminal:
                if nodoActual.verificar_si_hay_ganador(' O '):
                    return (None, 100000000000000)  # Gana la IA
                if nodoActual.verificar_si_hay_ganador(' X '):
                    return (None, -100000000000000)  # Gana el jugador humano
                if self.es_tablero_lleno(nodoActual.get_tablero()):
                    return (None, 0)  # Empate
            else:
                    return (None, self.evaluar_tablero(nodoActual.get_tablero(), ' O ') ) # Profundidad alcanzada

        if esMaximizador:
            maxEval = -float('inf')
            mejor_col = random.choice(lista_movimientos_validos)
            for col in range(nodoActual.cantidad_columas_no_llenas()):
                if not nodoActual.es_columna_llena(col):
                    if nodoActual.listaHijos[col] is None:
                        # Crear un hijo para la jugada
                        hijo = nodo([fila[:] for fila in nodoActual.get_tablero()])
                        hijo.poner_ficha(col, ' O ')
                        nodoActual.set_hijo(col, hijo)
                        eval = self.minimax(hijo, profundidad - 1, False, alfa, beta)[1]
                        if eval > maxEval:
                            maxEval = eval
                            mejor_col = col

                        maxEval = max(maxEval, eval)
                        alfa = max(alfa, maxEval)
                        if alfa >= beta:
                            break
            return mejor_col, maxEval
        else:
            minEval = float('inf')
            mejor_col = random.choice(lista_movimientos_validos)
            for col in range(nodoActual.cantidad_columas_no_llenas()):
                if not nodoActual.es_columna_llena(col):
                    if nodoActual.listaHijos[col] is None:
                        hijo = nodo([fila[:] for fila in nodoActual.get_tablero()])
                        hijo.poner_ficha(col, ' X ')
                        nodoActual.set_hijo(col, hijo)
                        eval = self.minimax(hijo, profundidad - 1, True, alfa, beta)[1]
                        if eval < minEval:
                            minEval = eval
                            mejor_col = col
                        minEval = min(minEval, eval)

                        beta = min(beta, minEval)
                        if alfa >= beta:
                            break
            return mejor_col, minEval
    
    def mostrar_tablero(self, tablero):
        nodoAux = nodo(tablero)
        return nodoAux.mostrar_estado_de_tablero()

    def es_abol_vacio(self):
        return self.raiz is None

    

        
