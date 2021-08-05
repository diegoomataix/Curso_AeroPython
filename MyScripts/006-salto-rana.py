#_____________________________________________________________________________#
def main():
    # Creamos el tablero de juego
    board = init()                      # Initialise board
    target = board[::-1]                # From : to : in -1 steps

    # Vamos pasando turnos hasta que no podamos continuar
    while can_move_something(board):    # Function for each turn    
        # Pintamos el tablero
        show(board)                     # Function to show the board
        # Pedimos por teclado una ficha para mover
        pos = int(input('Select a token to move (by its position): '))
        # Nos aseguramos de que esa ficha puede mover
        if not can_move(board, pos):    # Function to determine if the token can be moved
            print('The token cannot move!')
            continue
        # Y la movemos
        board = move(board, pos)        # Function to acc move the token

    # Comprobamos si ha ganado
    if board == target:
        print('ENHORABUENA!')
    else:
        print('Pringao!')
#_____________________________________________________________________________#
# init() function
# La creación del tablero no es demasiado compleja. Tan sólo hay que crear 
# una lista con 7 números enteros, en el que el 0 representa el hueco vacío, 
# el 1 las fichas rojas, y el -1 las fichas azules. Puede parecer que la 
# elección del valor para las fichas azules es un poco caprichoso, pero no 
# lo es en absoluto, ya que de paso nos permite saber la dirección en la 
# que avanzan, lo que nos ahorrará un poco de trabajo
def init():
    return [1] * 3 + [0] + [-1] * 3
#_____________________________________________________________________________#
def show(board):
    print(board)
#_____________________________________________________________________________#
# Función sólo debe recorrer la lista, y preguntar si alguien puede moverse
def can_move_something(board):
    for i in range(len(board)):
        if can_move(board, i):
            return True
    return False
#_____________________________________________________________________________#
# Esta función sólo debe intercambiar los valores de la posición elegida y del hueco.
def move(board, token):
    hole = get_hole(board)
    board[token], board[hole] = board[hole], board[token]
    return board
#_____________________________________________________________________________#
def get_hole(board):
    for i,token in enumerate(board):
        if not token:
            return i
#_____________________________________________________________________________#
def can_move(board, token):
    # Excluimos por supuesto fichas fuera del tablero
    if not -1 < token < len(board):
        return False
    # Y excluimos tambien el hueco
    if not board[token]:
        return False
    # Vamos a ver donde esta el hueco
    hole = get_hole(board)
    # Si el hueco es contiguo, y esta en el lado correcto, entonces sabemos positivamente que podemos mover
    if token + board[token] == hole:
        return True
    # Si no es el caso, la ficha esta obligada a saltar
    if (token + 2 * board[token] == hole) and (board[token + board[token]] != board[token]):    #!=: not equal to
        return True
    # Si la ficha no puede avanzar o saltar, entonces no se puede mover
    return False
#_____________________________________________________________________________#

main()