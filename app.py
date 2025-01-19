import pygame

ANCHO, ALTURA = 600, 600 
FILAS, COLUMNAS = 4, 4
TAMAGNO_CUADRADO = ANCHO//COLUMNAS

#PYGAME = RGB 
ROJO = (255, 255, 255)
BLANCO = (33, 47, 60)
NEGRO = (20, 20, 20)
GRIS = (128, 128, 128)
AZUL = (59, 131, 189)

#parte de la imagen de la corona, coloca una corona en una de las fichas cuando se vuelve reina 
CORONA = pygame.transform.scale(pygame.image.load("corona.png"), (65, 65))



#PIEZAS_____________________

class Piezas:
    RELLENO = 15
    BORDE = 2 
    
    def __init__(self, fil, col, color):
        self.fil = fil
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()
        
    def copy(self):
        # Crear una nueva instancia de la pieza con los mismos atributos
        nueva_pieza = Piezas(self.fil, self.col, self.color)
        nueva_pieza.king = self.king  # También copias el estado de si es reina o no
        return nueva_pieza
        
    def calc_pos(self):
        self.x = TAMAGNO_CUADRADO * self.col + TAMAGNO_CUADRADO // 2
        self.y = TAMAGNO_CUADRADO * self.fil + TAMAGNO_CUADRADO // 2

            
    def make_king(self):
        self.king = True # la pieza se vuelve king una vez que llega al final 
        
    def check_king(self):
        if not self.king:  # Solo si la pieza aún no es reina
            if (self.color == 'blanco' and self.fil == 0) or (self.color == 'negro' and self.fil == 3):
                self.make_king()
                print(f"¡Pieza en ({self.fil}, {self.col}) se convierte en reina!")


        
        
    def draw(self, win):
        radio = TAMAGNO_CUADRADO // 2 - self.RELLENO
        pygame.draw.circle(win, GRIS, (self.x, self.y), radio + self.BORDE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radio)
        if self.king:
            win.blit(CORONA, (self.x - CORONA.get_width()//2, self.y - CORONA.get_height()//2))
                
    def move(self, fil, col):
        if 0 <= fil < FILAS and 0 <= col < COLUMNAS:
            self.fil = fil
            self.col = col
            self.calc_pos()
            self.check_king()
        else:
            print("Movimiento fuera de los límites del tablero")

            
    def __repr__(self): # por si se necesita un debug, depurar 
        return str(self.color) #representacion interna del objetivo. evita el <object at x>
        
               
#____________________________________________________________


#TABLERO/ CASILLAS
class Tablero:
    def __init__(self):
        self.tablero = []
        self.ROJO_left = self.BLANCO_left = 2
        self.ROJO_kings = self.BLANCO_kings = 0 
        self.crear_tablero()
        
    def copy(self):
        """
        Crear y devolver una copia profunda del tablero actual.
        """
        nuevo_tablero = Tablero()
        nuevo_tablero.tablero = [[casilla.copy() if casilla != 0 else 0 for casilla in fila] for fila in self.tablero]
        
        nuevo_tablero.ROJO_left = self.ROJO_left
        nuevo_tablero.BLANCO_left = self.BLANCO_left
        nuevo_tablero.ROJO_kings = self.ROJO_kings
        nuevo_tablero.BLANCO_kings = self.BLANCO_kings
        
        return nuevo_tablero
      
     
        
    def draw_cuadrados(self, win):
        win.fill(NEGRO)
        for fil in range(FILAS):
            for col in range(fil % 2, COLUMNAS, 2): #esto crea el patron del tablero
                pygame.draw.rect(win, ROJO, (fil*TAMAGNO_CUADRADO, col *TAMAGNO_CUADRADO, TAMAGNO_CUADRADO, TAMAGNO_CUADRADO))
                
    def print_tablero(self):
        for fila in self.tablero:
            print([str(pieza) if pieza != 0 else "0" for pieza in fila])

    
    def move(self, pieza, fil, col):
        """
        Mueve una pieza de un lugar a otro en el tablero y actualiza su estado.
        """
        # Verificar si la casilla destino está vacía
        if self.tablero[fil][col] != 0:
            print(f"Movimiento no permitido: La casilla ({fil}, {col}) ya está ocupada.")
            return

        # Verificar si la pieza existe en la casilla de origen
        if self.tablero[pieza.fil][pieza.col] != pieza:
            #print(f"Error: No se encuentra la pieza en la casilla de origen ({pieza.fil}, {pieza.col})")
            return

        # Vaciar la posición original de la pieza
        self.tablero[pieza.fil][pieza.col] = 0  # Esto limpia la posición original

        # Colocar la pieza en la nueva posición
        self.tablero[fil][col] = pieza  # Aquí colocamos la pieza en su nueva posición

        # Actualizar las coordenadas de la pieza
        pieza.move(fil, col)

        # Promoción a rey si corresponde
        if fil == FILAS - 1 or fil == 0:
            pieza.make_king()
            if pieza.color == BLANCO:
                self.BLANCO_kings += 1
            else:
                self.ROJO_kings += 1

        # Imprimir depuración después del movimiento
        print(f"Después del movimiento: Casilla origen ({pieza.fil}, {pieza.col}) está vacía, Casilla destino ({fil}, {col}) contiene {self.tablero[fil][col]}")

        # Depuración: imprime el estado del tablero
        print("Estado del tablero después del movimiento:")
        for fila in self.tablero:
            print(fila)

   
    
    def get_pieza(self, fil, col):
        return self.tablero[fil][col]
    
    
    def crear_tablero(self):
        for fil in range(FILAS):
            self.tablero.append([])
            for col in range(COLUMNAS):
                if col % 2 == ((fil + 1 ) % 2):
                    if fil < 1:
                        self.tablero[fil].append(Piezas(fil, col, BLANCO))
                    elif fil > 2:
                        self.tablero[fil].append(Piezas(fil, col, ROJO))
                    else:
                        self.tablero[fil].append(0)
                else:
                    self.tablero[fil].append(0)
                    
    
    
    
                    
                    
    def draw(self, win):
        self.draw_cuadrados(win)
        for fil in range (FILAS):
            for col in range(COLUMNAS):
                pieza = self.tablero[fil][col]
                if pieza != 0:
                    pieza.draw(win)
                    
                    
    def eliminar(self, piezas):
        for pieza in piezas:
            self.tablero[pieza.fil][pieza.col] = 0
            if pieza != 0:
                if pieza.color == ROJO:
                    self.ROJO_left -= 1
                else:self.BLANCO_left -= 1

                    
                    
    def ganador(self):
        if self.ROJO_left <= 0:
            return BLANCO
        elif self.BLANCO_left <= 0:
            return ROJO
        return None
    
    
    
    def get_movimientos_validos(self, pieza):
        movimientos = {}
        izq = pieza.col - 1
        der = pieza.col + 1
        fil = pieza.fil
        
        if pieza.color == ROJO or pieza.king:#verifico la direccion en la que se pueden mover las piezas
            movimientos.update(self.atravezar_izq(fil -1, max(fil-3, -1), -1, pieza.color, izq))
            movimientos.update(self.atravezar_der(fil -1, max(fil-3, -1), -1, pieza.color, der))
            #se actualizan los moviemientos con lo que se devuelva de ahi             
        
        if pieza.color == BLANCO or pieza.king:
            movimientos.update(self.atravezar_izq(fil +1, min(fil+3, FILAS), 1, pieza.color, izq))
            movimientos.update(self.atravezar_der(fil +1, min(fil+3, FILAS), 1, pieza.color, der))
            #se actualizan loa movimientos con los que se devuelva de ahi
        return movimientos 
    
    
    
    def atravezar_izq(self, start, stop, step, color, izq, skipped=None, visited=None):
        if visited is None:
            visited = set()  # Inicializar visited si es None
        
        movimientos = {}
        last = []
        
        for f in range(start, stop, step):
            if izq < 0 or izq >= COLUMNAS:
                break

            current = self.tablero[f][izq]
            
            # Si ya se visitó esta casilla, saltamos a la siguiente
            if (f, izq) in visited:
                continue
            
            if current == 0:  # Casilla vacía
                if skipped and not last:
                    break
                elif skipped:
                    movimientos[(f, izq)] = last + skipped
                else:
                    movimientos[(f, izq)] = last

                if last:
                    # Agregar la casilla actual al conjunto de visitados
                    visited.add((f, izq))

                    # Recursión para verificar saltos posteriores
                    movimientos.update(self.atravezar_izq(f + step, stop, step, color, izq - 1, skipped=last, visited=visited))
                    movimientos.update(self.atravezar_der(f + step, stop, step, color, izq + 1, skipped=last, visited=visited))
                break
            elif isinstance(current, Piezas) and current.color == color:  # No puedo saltar sobre piezas propias
                break
            else:
                last = [current]  # Se puede saltar sobre piezas del color contrario
                izq -= 1
        
        return movimientos if movimientos else {}
            
    

    def atravezar_der(self, start, stop, step, color, der, skipped=[], visited=None):
        if visited is None:
            visited = set()  # Inicializar visited si es None
        
        movimientos = {}
        last = []
        
        for f in range(start, stop, step):
            if der < 0 or der >= COLUMNAS:
                break

            current = self.tablero[f][der]
            
            # Si ya se visitó esta casilla, saltamos a la siguiente
            if (f, der) in visited:
                continue
            
            if current == 0:  # Casilla vacía
                if skipped and not last:
                    break
                elif skipped:
                    movimientos[(f, der)] = last + skipped
                else:
                    movimientos[(f, der)] = last

                if last:
                    # Agregar la casilla actual al conjunto de visitados
                    visited.add((f, der))

                    # Recursión para verificar saltos posteriores
                    movimientos.update(self.atravezar_izq(f + step, stop, step, color, der - 1, skipped=last, visited=visited))
                    movimientos.update(self.atravezar_der(f + step, stop, step, color, der + 1, skipped=last, visited=visited))
                break
            elif isinstance(current, Piezas) and current.color == color:  # No puedo saltar sobre piezas propias
                break
            else:
                last = [current]  # Se puede saltar sobre piezas del color contrario
                der += 1
        
        return movimientos if movimientos else {}


            
        
       
#___________________________________________________________

class AgenteIA:
    def __init__(self, tablero):
        self.tablero = tablero
        self.max_depth = 4  # Profundidad máxima de búsqueda en el árbol
        
    def obtener_mejor_movimiento(self):
        mejor_movimiento = None
        mejor_valor = -float('inf')
        movimientos_realizados = set()  # Para verificar movimientos realizados

        # Recorremos todas las piezas de la IA (BLANCO)
        for fil in range(FILAS):
            for col in range(COLUMNAS):
                pieza = self.tablero.get_pieza(fil, col)
                if pieza != 0 and pieza.color == BLANCO:  # Verificar que la pieza es de la IA
                    movimientos_validos = self.tablero.get_movimientos_validos(pieza)

                    for (nueva_fila, nueva_col), salto in movimientos_validos.items():
                        movimiento_actual = (fil, col, nueva_fila, nueva_col)
                        
                        # Ignorar si el movimiento ya fue realizado
                        if movimiento_actual in movimientos_realizados:
                            continue

                        # Registrar el movimiento como realizado
                        movimientos_realizados.add(movimiento_actual)

                        # Simular el movimiento
                        copia_tablero = self.tablero.copy()
                        copia_tablero.move(pieza, nueva_fila, nueva_col)

                        # Calcular el valor usando Minimax
                        valor = self.minimax(copia_tablero, 0, -float('inf'), float('inf'), False)

                        # Actualizar el mejor movimiento si el valor es mayor
                        if valor > mejor_valor:
                            mejor_valor = valor
                            mejor_movimiento = movimiento_actual

                        # Liberar memoria eliminando la referencia a la copia
                        del copia_tablero

        return mejor_movimiento


    def minimax(self, tablero, profundidad, alpha, beta, es_maximizador):
        # Si llegamos a la profundidad máxima o si el juego terminó, evaluamos el tablero
        ganador = tablero.ganador()
        if profundidad == self.max_depth or ganador != None:
            return self.evaluar_tablero(tablero)
        
        if es_maximizador:
            max_eval = -float('inf')
            for fil in range(FILAS):
                for col in range(COLUMNAS):
                    pieza = tablero.get_pieza(fil, col)
                    if pieza != 0 and pieza.color == BLANCO:  # Solo movimientos del jugador IA
                        movimientos_validos = tablero.get_movimientos_validos(pieza)
                        for (nueva_fila, nueva_col) in movimientos_validos:
                            copia_tablero = tablero.copy()
                            copia_tablero.move(pieza, nueva_fila, nueva_col)
                            eval_ = self.minimax(copia_tablero, profundidad + 1, alpha, beta, False)
                            max_eval = max(max_eval, eval_)
                            alpha = max(alpha, eval_)
                            if beta <= alpha:
                                break
            return max_eval
        else:
            min_eval = float('inf')
            for fil in range(FILAS):
                for col in range(COLUMNAS):
                    pieza = tablero.get_pieza(fil, col)
                    if pieza != 0 and pieza.color == ROJO:  # Movimientos del jugador humano
                        movimientos_validos = tablero.get_movimientos_validos(pieza)
                        for (nueva_fila, nueva_col) in movimientos_validos:
                            copia_tablero = tablero.copy()
                            copia_tablero.move(pieza, nueva_fila, nueva_col)
                            eval_ = self.minimax(copia_tablero, profundidad + 1, alpha, beta, True)
                            min_eval = min(min_eval, eval_)
                            beta = min(beta, eval_)
                            if beta <= alpha:
                                break
            return min_eval

    def evaluar_tablero(self, tablero):
        # Asigna un puntaje al estado del tablero. Esto puede basarse en la cantidad de piezas, reinas, etc.
        puntuacion = 0
        # Puntos por piezas y reinas
        puntuacion += tablero.BLANCO_left * 1  # Puedes asignar diferentes valores a las piezas y reinas
        puntuacion += tablero.BLANCO_kings * 5
        puntuacion -= tablero.ROJO_left * 1
        puntuacion -= tablero.ROJO_kings * 5
        
        return puntuacion




#manejo del juego______________________


class juego:
    def __init__(self, win):
        self._init()
        self.win = win
        self.agente_ia = AgenteIA(self.tablero)  # Crear instancia del agente IA

    def update(self):
        self.tablero.draw(self.win)
        self.draw_movimientos_validos(self.movimientos_validos)
        pygame.display.update()
        
    def _init(self):
        self.selected = None
        self.tablero = Tablero()
        self.turn = ROJO
        self.movimientos_validos = {}
        
    def ganador(self):
        return self.tablero.ganador()
    
    def reset(self):
        self._init()
        
    def select(self, fil, col):
        if self.selected:
            result = self._move(fil, col)  # Se mueve lo seleccionado
            if not result:
                self.selected = None
                self.select(fil, col)

        pieza = self.tablero.get_pieza(fil, col)
        if pieza != 0:
            # Si la pieza es del jugador actual (turno)
            if pieza.color == self.turn:
                self.selected = pieza
                self.movimientos_validos = self.tablero.get_movimientos_validos(pieza)
                return True
            else:
                # Si la pieza no es del jugador actual, no se selecciona
                print("No puedes seleccionar una pieza del oponente.")
                return False
        return False


        
    def _move(self, fil, col):
        pieza = self.tablero.get_pieza(fil, col)

        # Verifica si la posición seleccionada es válida
        if self.selected:
            # Si la casilla destino está vacía y es un movimiento permitido
            if pieza == 0 and (fil, col) in self.movimientos_validos:
                self.tablero.move(self.selected, fil, col)

                # Si hubo una captura, elimina la pieza capturada
                skipped = self.movimientos_validos.get((fil, col), None)
                if skipped:
                    self.tablero.eliminar(skipped)

                # Cambiar el turno después del movimiento
                self.change_turn()
                self.turno_agente_ia()  # IA juega después del jugador
                return True

            # Si la casilla destino está ocupada por una pieza enemiga
            elif pieza != 0 and pieza.color != self.turn:
                print("Movimiento no permitido: No puedes moverte a una casilla ocupada por una pieza enemiga.")
                return False

            # Si la casilla destino está ocupada por una pieza del mismo jugador
            elif pieza != 0 and pieza.color == self.turn:
                print("Movimiento no permitido: No puedes moverte a una casilla ocupada por tu propia pieza.")
                return False

        print("Movimiento inválido.")
        return False



    def draw_movimientos_validos(self, movimientos):
        for move in movimientos:
            fil, col = move
            pygame.draw.circle(self.win, AZUL, (col * TAMAGNO_CUADRADO + TAMAGNO_CUADRADO//2, fil * TAMAGNO_CUADRADO + TAMAGNO_CUADRADO//2), 15)
            
    def change_turn(self):
        self.movimientos_validos = {}
        if self.turn == ROJO:
            self.turn = BLANCO
        else:
            self.turn = ROJO

        # Después de cambiar de turno, mueve automáticamente la IA si es su turno
        if self.turn == BLANCO:  # Si el turno es de la IA
            self.turno_agente_ia()

    def turno_agente_ia(self):
        if self.turn == BLANCO:  # Asegurarse de que es el turno de la IA
            mejor_movimiento = self.agente_ia.obtener_mejor_movimiento()
            print("Mejor movimiento IA:", mejor_movimiento)  # Depuración

            # Verifica que haya un movimiento válido
            if mejor_movimiento:
                pieza_inicial = self.tablero.get_pieza(mejor_movimiento[0], mejor_movimiento[1])

                # Asegúrate de que la pieza inicial exista
                if pieza_inicial == 0:
                    print("Error: No hay pieza en la posición inicial.")
                    return

                # Verifica que el destino esté vacío o sea un movimiento válido
                destino = self.tablero.get_pieza(mejor_movimiento[2], mejor_movimiento[3])
                if destino != 0:
                    print("Error: La casilla destino ya está ocupada.")
                    return

                # Realiza el movimiento
                self.tablero.move(pieza_inicial, mejor_movimiento[2], mejor_movimiento[3])

                # Si hubo una captura, elimina la pieza capturada
                skipped = self.movimientos_validos.get((mejor_movimiento[2], mejor_movimiento[3]), None)
                if skipped:
                    self.tablero.eliminar(skipped)

                # Cambiar el turno al jugador
                self.change_turn()

                # Finalizar el turno de la IA
                return

            print("La IA no encontró un movimiento válido.")





            
            
#MAIN___________________________
FPS = 60 #declaracion de los fotogramas por segundo/ framse per second


WIN = pygame.display.set_mode((ANCHO, ALTURA))


pygame.display.set_caption('JUEGO DE DAMAS')


def get_fil_col_from_mouse(pos):
    x, y = pos 
    fil = y // TAMAGNO_CUADRADO
    col = x // TAMAGNO_CUADRADO
    return fil, col


def main():
    run = True
    clock = pygame.time.Clock()
    game = juego(WIN)
    
    
    while run:
        clock.tick(FPS)
        
        if game.ganador() != None:
            print(game.ganador())
            run = False
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                pos = pygame.mouse.get_pos()
                fil, col = get_fil_col_from_mouse(pos)
                game.select(fil, col)
        game.update()
    pygame.quit()
main()