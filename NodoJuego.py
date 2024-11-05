class nodo:
    
    def __init__(self, tablero):
        self.tablero = tablero
        self.listaHijos = []
        self.ini(self.cantidad_columas_no_llenas())
        self.estadoTablero = None #1 ganaIA ' O ', 0 empate, -1 ganahumano ' X '

    def ini(self, orden):
        for i in range(orden):
            self.listaHijos.append(None)

    def mostrar_estado_de_tablero(self):
        print("   " + "     ".join([str(i) for i in range(1, len(self.tablero[0]) + 1)]))
        for fila in self.tablero:
         print ("")
         print("| " + " | ".join(fila) + " |")
        print("") 

    def poner_ficha(self, columna, letra):
        if not self.es_columna_llena(columna):
            fila_a_caer = 0
            while fila_a_caer < 6: #mientras no este llena la columa
                if self.tablero [fila_a_caer + 1][columna] == ' - ':
                    fila_a_caer += 1
                else:
                    break
            self.tablero[fila_a_caer][columna] = letra
        else:
            print("-columna lleva, prueba otra-")
            print("")

    def es_columna_llena(self,  columna):
        "retorna verdadero o falso"
        if self.tablero[0][columna] != ' - ': #verificamos la fila 0 
            return True
        return False
    
    def obtener_fila_disponible(self, tablero, columna):
        for fila in range(len(tablero)-1, -1, -1):
            if tablero[fila][columna] == '-':
                return fila
        return None

    def verificar_si_hay_ganador(self, letra):
        filas = len(self.tablero)      # Número de filas en el tablero
        columnas = len(self.tablero[0])  # Número de columnas en el tablero

        # Verificar horizontalmente (filas)
        for fila in range(filas):
            for col in range(columnas - 3):
                if (self.tablero[fila][col] == letra and
                    self.tablero[fila][col + 1] == letra and
                    self.tablero[fila][col + 2] == letra and
                    self.tablero[fila][col + 3] == letra):
                    return True

        # Verificar verticalmente (columnas)
        for col in range(columnas):
            for fila in range(filas - 3):
                if (self.tablero[fila][col] == letra and
                    self.tablero[fila + 1][col] == letra and
                    self.tablero[fila + 2][col] == letra and
                    self.tablero[fila + 3][col] == letra):
                    return True

        # Verificar diagonal descendente (\)
        for fila in range(filas - 3):
            for col in range(columnas - 3):
                if (self.tablero[fila][col] == letra and
                    self.tablero[fila + 1][col + 1] == letra and
                    self.tablero[fila + 2][col + 2] == letra and
                    self.tablero[fila + 3][col + 3] == letra):
                    return True

        # Verificar diagonal ascendente (/)
        for fila in range(3, filas):
            for col in range(columnas - 3):
                if (self.tablero[fila][col] == letra and
                    self.tablero[fila - 1][col + 1] == letra and
                    self.tablero[fila - 2][col + 2] == letra and
                    self.tablero[fila - 3][col + 3] == letra):
                    return True

        # Si no hay ganador
        return False

    def cantidad_columas_no_llenas(self):
        contador = 0
        for columna in range(7):
            if not self.es_columna_llena(columna):
                contador += 1
        return contador
    
    def set_hijo(self, posicion, hijo):
        self.listaHijos[posicion] = hijo
    
    def get_hijo(self, posicion):
        return self.listaHijos[posicion]
    
    def get_tablero(self):
        return self.tablero
    
    def set_tablero(self, tablero):
        self.tablero = tablero

    def set_estadoDelTablero(self, estado:bool):
        self.estadoTablero = estado

    def get_estadoDelTablero(self):
        if self.estadoTablero == False:
            return False
        else:
            return True
    
    def siguiente_columna_vacia(self, tablero, columna_inicial):
        # Iterar desde la columna inicial hasta la última columna
        for i in range(columna_inicial, len(tablero[0])):  
            if not self.es_columna_llena(i):  # Verifica si la columna no está llena
                return i  # Retorna la columna vacía encontrada
            
        # Si no se encuentra una columna vacía, empieza desde el principio
        for i in range(0, columna_inicial):  # Busca desde el inicio hasta la columna inicial
            if not self.es_columna_llena(i):  # Verifica si la columna no está llena
                return i  # Retorna la columna vacía encontrada
        
        return -1  # Si todas las columnas están llenas, retorna -1



            

     