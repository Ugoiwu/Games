from random import randint
import time
import os

alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

# Fonction pour supprimer la console
def cls():
    os.system('cls' if os.name=='nt' else 'clear')


def Game():
    cls()
    # Initialisation basique de la game
    inputSize = int(input("Quelle taille souhaitez vous pour cette partie de démineur ? (répondre par le chiffre indiqué)\n1: Débutant (9*9 - 10 mines)\n2: Intermédiaire (16*16 - 40 mines)\n3: Avancé (30*16 - 99 mines)\n4: Surhomme (50*50 - 500 mines)\n5: Extraterrestre (100*100 - 2000 mines)\n6: Personnalisé\n"))
    victory = False
    mines = []
    size = []

    match inputSize:
        case 1:
            size = [9,9,10]
        case 2:
            size = [16,16,40]
        case 3:
            size = [30,16,99]
        case 4:
            size = [50,50,500]
        case 5:
            size = [100,100,2000]
        case 6:
            size = list(map(int, input("Veuillez écrire dans l'ordre: la largeur, la hauteur, et le nombre de mines, séparé par des espaces: (ex: 9 9 10) ").split()))
        
    board = [["■" for _ in range(size[0])] for _ in range(size[1])]
    trueBoard = [[0 for _ in range(size[0])] for _ in range(size[1])]

    # Positionner les mines aléatoirement sur le trueBoard
    for i in range(size[2]):
        x, y = randint(0, size[0]-1), randint(0, size[1]-1)
        if [x, y] in mines: 
            x, y = randint(0, size[0]-1), randint(0, size[1]-1)
        else:
            mines.append([x, y])
            trueBoard[y][x] = "▲"

    # Pour les cases sans mines, déterminer le nombre de mines aux alentours
    for mine in mines:
        y,x = mine
        if trueBoard[x][y] != "▲":
            continue
        else:
            for k, l in zip([1,1,1,0,0,0,-1,-1,-1], [-1,0,1,-1,0,1,-1,0,1]):
                try:
                    if -1 in [x+k, y+l]:
                        continue
                    if trueBoard[x+k][y+l] >= 0:
                        trueBoard[x+k][y+l] += 1
                except:
                    pass

    # Fonction pour afficher le tableau
    def afficherBoard(board: list, mines: list):

        a = len(str(len(board[0])))
        x = ""
        for i in range(len(board[0])):
            z = int(str(i/26)[0])
            x = x + f"{z} "

        print(f"{' ': <{a+3}} {x} Mines restantes:")

        x = ""
        for i in range(len(board[0])):
            i+=1
            if i/25 > 1:
                i -= int(str(i/26)[0]) * 26
            x += f"{alpha[i-1]} "
            
        print(f"{' ': <{a+3}} {x} - {mines}")
        print("─"*(((3+len(board[0]))*2)-1))

        for index, i in enumerate(board):
            index+=1
            print(f"{index : <{a}} | ", *i)

    # Fonction pour choisir une case
    def chooseCase():
        while True:
            try:
                letter, nbr = input("Veuillez indiquer la lettre, et ensuite le nombre: (ex: A0 1) ").split()
                break
            except:
                pass
        letter = list(letter)
        letter[0] = letter[0].upper()
        letterIndex =  alpha.index(letter[0]) + 26*int(letter[1])
        return int(nbr)-1,letterIndex
    
    # Fonction pour compter le nombre de mines
    def countMines(mines: list, board: list):
        nbrMines = len(mines)
        for i in board:
            nbrMines -= i.count("¤")
        return nbrMines


    # Fonction pour remplir les cases alentours si on tombe sur une case contenant 0
    def fill(coord: list, board: list, trueBoard: list, typeFill: int):
        y, x = coord

        if trueBoard[y][x] == 0 and board[y][x] != 0:
            board[y][x] = 0
            for i,j in zip([-1, 1, 0, 0], [0, 0, -1, 1]):
                if -1 in [y+i, x+j] or y+i > size[1]-1 or x+j > size[0]-1:
                    continue
                elif typeFill == 0:
                    if trueBoard[y+i][x+j] >= 1:
                        board[y+i][x+j] = trueBoard[y+i][x+j]
                    fill([y+i, x+j], board, trueBoard, typeFill)

    start = time.time()
    while not victory:
        cls()

        # Compter le nombre de mines
        nbrMines = countMines(mines, board)

        afficherBoard(board, nbrMines)

        # Décider de l'action à faire
        actionOk = False

        while not actionOk:
            while True:
                try:
                    action = int(input("Que voulez vous faire ?\n- 1: Révéler une case\n- 2: (Dé)Marquer une mine\n. "))
                    break
                except:
                    pass

            # Réaliser l'action choisie
            y,x = chooseCase()
            if action == 1:
                if board[y][x] == "¤":
                    print("Vous ne pouvez pas révéler une case marquée.")
                    continue
                if trueBoard[y][x] == 0:
                    fill([y, x], board, trueBoard, 0)
                else:
                    board[y][x] = trueBoard[y][x]
                actionOk = True
            else:
                if board[y][x] == "¤":
                    board[y][x] = "■"
                    actionOk = True
                else:
                    if board[y][x] != "■":
                        print("Vous ne pouvez pas marquer une case révélée.")
                        continue
                    board[y][x] = "¤"
                    actionOk = True

        nbrMines = countMines(mines, board)
        afficherBoard(board, nbrMines)

        # Vérifier condition défaite
        if board[y][x] == "▲":
            print("Perdu ! Tu es tombé sur une mine !")
            break
        
        # Vérifier condition victoire
        nbrUnrevealed = 0
        for i in board:
            nbrUnrevealed += i.count("■")

        if nbrUnrevealed == 0:
            tempBoard = board
            tempBreak = False
            for i in range(size[1]-1):
                for j in range(size[0]-1):
                    if tempBoard[i][j] == "¤":
                        tempBoard[i][j] = "▲"
                    if tempBoard[i][j] != trueBoard[i][j]:
                        tempBreak = True
                        break
                if tempBreak:
                    break
            if not tempBreak:
                print("Vous avez gagné !!!")
                break

        input("Appuyer pour passer au prochain tour...")
    end = time.time()
    print(f"Tu as fini la partie en {str(end-start)[0:3]} secondes.")

    restart = input("Veux tu recommencer ? O pour oui, N pour non: ").upper()
    cls()
    if restart == "O":
        Game()

Game()