import pygame
import sys
import time

from tictactoe import TicTacToe

pygame.init()
size = width, height = 600, 400

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode(size)
bg_image = pygame.image.load("./assets/img/bg_image.jpg")
bg_image = pygame.transform.scale(bg_image, size)

mediumFont = pygame.font.Font("./assets/font/OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("./assets/font/OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("./assets/font/OpenSans-Regular.ttf", 60)

user = None
game_board = TicTacToe()
ai_turn = False



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.blit(bg_image, bg_image.get_rect())

    # Player memilih
    if user is None:
        # Title
        title = largeFont.render("Tic Tac Toe", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Button X
        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playX = mediumFont.render("Pemain X", True, black)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, white, playXButton)
        screen.blit(playX, playXRect)

        # Button O
        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        playO = mediumFont.render("Pemain O", True, black)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, white, playOButton)
        screen.blit(playO, playORect)

        # Cek jika button diklik
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = TicTacToe.X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = TicTacToe.O

    else:
        # Game board
        tile_size = 80
        tile_origin = (width / 2 - (1.5 * tile_size),
                       height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, white, rect, 3)
                if game_board.state[i][j] != TicTacToe.EMPTY:
                    move = moveFont.render(game_board.state[i][j], True, white)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = game_board.terminal(game_board.state)
        player = game_board.player(game_board.state)

        # Tunjukkan tittle
        if game_over:
            winner = game_board.winner(game_board.state)
            if winner is None:
                title = f"Game Over: Seri."
            else:
                title = f"Game Over: {winner} menang."
        elif user == player:
            title = f"Bermain sebagai {user}"
        else:
            title = f"AI berpikir..."
        title = largeFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        # Cek pergerakkan AI
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = game_board.alpha_beta_search()
                game_board.state = game_board.result(game_board.state, move)
                ai_turn = False
            else:
                ai_turn = True

        # Cek pergerakkan user
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if (game_board.state[i][j] == TicTacToe.EMPTY and tiles[i][j].collidepoint(mouse)):
                        game_board.state = game_board.result(game_board.state, (i, j))

        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Play Again", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    game_board.clear()
                    ai_turn = False
        else:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Kembali", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    game_board.clear()
                    ai_turn = False

    pygame.display.flip()
