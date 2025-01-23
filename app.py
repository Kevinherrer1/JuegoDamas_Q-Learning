import pygame
import random


# Inicializar Pygame
pygame.init()

# Constantes de la pantalla
WIDTH, HEIGHT = 400, 400
ROWS, COLS = 4, 4
SQUARE_SIZE = WIDTH // COLS

# Colores
LIGHT_COLOR = (205, 170, 125) 
DARK_COLOR = (120, 85, 55) 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Configuración de la ventana
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Damas 4x4")

# Tablero inicial dinámico
board = [[None for _ in range(COLS)] for _ in range(ROWS)]

# Inicializar las piezas dinámicamente
def init_pieces():
    for row in range(ROWS):
        for col in range(COLS):
            if row == 0 and col % 2 == 0:  # Primera fila (blancas) en columnas pares
                board[row][col] = "W"  # Blancas
            elif row == 3 and col % 2 != 0:  # Última fila (negras) en columnas impares
                board[row][col] = "B"  # Negras

# Dibujar el tablero
def draw_board(win):
    for row in range(ROWS):
        for col in range(COLS):
            color = DARK_COLOR if (row + col) % 2 == 0 else LIGHT_COLOR
            pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Dibujar las piezas
def draw_pieces(win):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece:
                x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                y = row * SQUARE_SIZE + SQUARE_SIZE // 2
                radius = SQUARE_SIZE // 3
                if piece == "W":
                    pygame.draw.circle(win, WHITE, (x, y), radius)
                    pygame.draw.circle(win, BLACK, (x, y), radius, 2)  # Borde negro
                elif piece == "B":
                    pygame.draw.circle(win, BLACK, (x, y), radius)
                elif piece == "QW":  # Reina blanca
                    pygame.draw.circle(win, WHITE, (x, y), radius)
                    pygame.draw.circle(win, (255, 215, 0), (x, y), radius, 4)  # Borde dorado
                elif piece == "QB":  # Reina negra
                    pygame.draw.circle(win, BLACK, (x, y), radius)
                    pygame.draw.circle(win, (255, 215, 0), (x, y), radius, 4)  # Borde dorado



# Obtener los movimientos válidos (con lógica de capturas)
def get_valid_moves(row, col):
    piece = board[row][col]
    moves = []
    
    if not piece:
        return moves

    directions = []  # Direcciones de movimiento
    
    # Direcciones según el tipo de pieza
    if piece == "B":  # Piezas negras
        directions = [(-1, -1), (-1, 1)]  # Movimientos hacia arriba
    elif piece == "W":  # Piezas blancas
        directions = [(1, -1), (1, 1)]  # Movimientos hacia abajo
    elif piece == "QB" or piece == "QW":  # Reinas (negras o blancas)
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Movimientos en todas las direcciones
    
    # Comprobamos los movimientos normales y las capturas
    for dr, dc in directions:
        r, c = row + dr, col + dc
        # Movimiento normal: casilla vacía
        if 0 <= r < ROWS and 0 <= c < COLS and not board[r][c]:
            moves.append((r, c))

        # Movimiento de captura
        capture_row, capture_col = row + 2 * dr, col + 2 * dc
        if (0 <= capture_row < ROWS and 0 <= capture_col < COLS and  # Verifica que la captura esté dentro del tablero
            board[r][c] and  # Hay una pieza en la casilla intermedia
            board[capture_row][capture_col] is None):  # La casilla de salto está vacía

            # Validar que no se capturen piezas propias
            if piece in ("W", "QW") and board[r][c] not in ("W", "QW"):  # Si es blanca, no puede capturar blancas
                moves.append((capture_row, capture_col))
            elif piece in ("B", "QB") and board[r][c] not in ("B", "QB"):  # Si es negra, no puede capturar negras
                moves.append((capture_row, capture_col))


    return moves

# Mover pieza con captura
def move_piece(selected_piece, target_row, target_col):
    row, col = selected_piece
    piece = board[row][col]
    board[row][col] = None  # Vaciar la casilla de la pieza seleccionada

    # Si la jugada es una captura, vaciar la casilla de la pieza capturada
    mid_row = (row + target_row) // 2  # Fila de la pieza capturada
    mid_col = (col + target_col) // 2  # Columna de la pieza capturada

    if abs(row - target_row) > 1:  # Verificar si la jugada fue una captura
        board[mid_row][mid_col] = None  # Vaciar la casilla de la pieza capturada

    board[target_row][target_col] = piece  # Colocar la pieza en la nueva casilla

    # Verificar si la pieza llegó al final y convertirla en reina
    if piece == "W" and target_row == 3:  # Si es blanca y llega a la fila 0
        board[target_row][target_col] = "QW"  # Convertir en reina blanca
    elif piece == "B" and target_row == 0:  # Si es negra y llega a la fila 3
        board[target_row][target_col] = "QB"  # Convertir en reina negra



# Dibujar movimientos válidos
def draw_valid_moves(win, moves):
    for row, col in moves:
        x = col * SQUARE_SIZE + SQUARE_SIZE // 2
        y = row * SQUARE_SIZE + SQUARE_SIZE // 2
        pygame.draw.circle(win, BLUE, (x, y), 10)



# Movimiento de la máquina
def machine_turn():
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] in ("B", "QB"):
                valid_moves = get_valid_moves(row, col)
                if valid_moves:
                    target = random.choice(valid_moves)
                    move_piece((row, col), *target)
                    return



def human_turn(event, selected_piece, valid_moves, turn):
    # Lógica de interacción del jugador humano
    if event.type == pygame.MOUSEBUTTONDOWN:
        x, y = pygame.mouse.get_pos()
        row, col = y // SQUARE_SIZE, x // SQUARE_SIZE

        if selected_piece:
            # Si selecciona una posición válida, mover la pieza
            if (row, col) in valid_moves:
                move_piece(selected_piece, row, col)
                selected_piece = None
                valid_moves = []
                turn = "MÁQUINA"  # Cambiar el turno
            else:
                # Deseleccionar
                selected_piece = None
                valid_moves = []
        elif board[row][col] in ("W", "QW"):
            # Seleccionar una pieza
            selected_piece = (row, col)
            valid_moves = get_valid_moves(row, col)

    return selected_piece, valid_moves, turn



def check_winner():
    # Contar las piezas restantes de cada jugador
    human_pieces = sum(row.count("W") + row.count("QW") for row in board)
    machine_pieces = sum(row.count("B") + row.count("QB") for row in board)

    if human_pieces == 0:
        return "MÁQUINA"
    elif machine_pieces == 0:
        return "HUMANO"

    # Verificar si ambos jugadores tienen movimientos válidos
    human_moves = any(get_valid_moves(row, col) for row in range(ROWS) for col in range(COLS) if board[row][col] in ("W", "QW"))
    machine_moves = any(get_valid_moves(row, col) for row in range(ROWS) for col in range(COLS) if board[row][col] in ("B", "QB"))

    if not human_moves and not machine_moves:
        return "EMPATE"
    elif not human_moves:
        return "MÁQUINA"
    elif not machine_moves:
        return "HUMANO"

    return None  # El juego continúa

def draw_winner(win, winner):
    font = pygame.font.SysFont("arial", 48)  # Fuente y tamaño del texto
    if winner == "EMPATE":
        text = font.render("¡EMPATE!", True, (255, 255, 255))
    else:
        text = font.render(f"¡El ganador es: {winner}!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Centrar el texto
    pygame.draw.rect(win, (0, 0, 0), text_rect.inflate(20, 20))  # Fondo negro para el texto
    win.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(3000)  # Esperar 3 segundos antes de cerrar


# Juego principal
def main():
    run = True
    clock = pygame.time.Clock()

    init_pieces()

    selected_piece = None
    valid_moves = []
    turn = "HUMANO"  # Turno inicial
    move_counter = 0 #contador de movimientos
    

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if turn == "HUMANO":
                # Llamar a la función para el turno del humano
                selected_piece, valid_moves, turn = human_turn(event, selected_piece, valid_moves, turn)
                

        # Turno de la máquina
        if turn == "MÁQUINA":
            machine_turn()
            turn = "HUMANO"
            move_counter += 1
            
        #Verificar si hay un ganador
        winner = check_winner()
        if winner:
            draw_board(WIN)
            draw_pieces(WIN)
            draw_winner(WIN, winner)
            run = False
            
        if move_counter == 64:
            draw_board(WIN)
            draw_pieces(WIN)
            draw_winner(WIN, "EMPATE")
            run = False
            

        # Dibujar todo
        draw_board(WIN)
        draw_pieces(WIN)
        if valid_moves:
            draw_valid_moves(WIN, valid_moves)

        
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()