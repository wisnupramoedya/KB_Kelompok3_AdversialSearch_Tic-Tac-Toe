import pygame
import sys
import time

from tictactoe import TicTacToe

pygame.init()
size = width, height = 400, 600

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tic Tac Toe vs AI")

logo_file = "./assets/img/logo.png"
logo_image = pygame.image.load(logo_file)
logo_image = pygame.transform.scale(logo_image, (32, 32))
pygame.display.set_icon(logo_image)

bg_file = "./assets/img/bg_image.jpg"
bg_image = pygame.image.load(bg_file)
bg_image = pygame.transform.scale(bg_image, size)

font_file = "./assets/font/Catskin.otf"
mediumFont = pygame.font.Font(font_file, 35)
smallFont = pygame.font.Font(font_file, 25)
largeFont = pygame.font.Font(font_file, 80)
llargeFont = pygame.font.Font(font_file, 55)
moveFont = pygame.font.Font(font_file, 60)

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
        title = largeFont.render("Tic-Tac-Toe", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width/ 2), 180)
        screen.blit(title, titleRect)

        # Button X
        playXButton = pygame.Rect(5*(width / 8), (height / 2), width / 2.5, 50)
        playX = mediumFont.render("Play as X", True, black)
        playXRect = playX.get_rect()
        playXButton.center=((width / 2), 300)
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, white, playXButton,border_top_right_radius=20,
        border_bottom_right_radius=20,border_bottom_left_radius=20,
        border_top_left_radius=20)
        screen.blit(playX, playXRect)

        # Button O
        playOButton = pygame.Rect(5 * (width / 2), (height / 2), width /  2.5, 50)
        playO = mediumFont.render("Play as O", True, black)
        playORect = playO.get_rect()
        playOButton.center=((width / 2), 370)
        playORect.center = playOButton.center
        pygame.draw.rect(screen, white, playOButton,border_top_right_radius=20,
        border_bottom_right_radius=20,border_bottom_left_radius=20,
        border_top_left_radius=20)
        screen.blit(playO, playORect)

        #Exit Button
        exitButton = pygame.Rect(5 * (width / 2), (height / 2), width /  2.5, 50)
        exit = mediumFont.render("Exit", True, black)
        exitRect = exit.get_rect()
        exitButton.center=((width / 2), 440)
        exitRect.center = exitButton.center
        pygame.draw.rect(screen, white, exitButton,border_top_right_radius=20,
        border_bottom_right_radius=20,border_bottom_left_radius=20,
        border_top_left_radius=20)
        screen.blit(exit, exitRect)

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
            elif exitButton.collidepoint(mouse):
                time.sleep(0.2)
                pygame.quit()
    # tictactoe board
    else:
        # Game board
        tile_size = 80
        tile_origin = (width / 2 - (1.5 * tile_size),
                       height / 3 - (1.5 * tile_size))
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
                title = f"Game Over : Seri"
            else:
                player_winner = "AI" if not ai_turn else "You"
                title = f"Game Over : {player_winner} Win!"
        elif user == player:
            title = f" Current player: {user} "
            turn = mediumFont.render("Your Turn", True, white)
            titlesRect = turn.get_rect()
            titlesRect.center = ((width / 2), 420)
            screen.blit(turn, titlesRect)  
        else:
            title = f" Current player: {player} "
            turn = mediumFont.render("Wait for Your Turn", True, white)
            titlesRect = turn.get_rect()
            titlesRect.center = ((width / 2), 420)
            screen.blit(turn, titlesRect)        
        
        title = mediumFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 380)
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
            #play again
            againButton = pygame.Rect(5 * (width / 2), (height / 2), width /  2.5, 50)
            again = smallFont.render("Play Again", True, black)
            againRect = again.get_rect()
            againButton.center=((width / 2), 480)
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton,border_top_right_radius=20,
             border_bottom_right_radius=20,border_bottom_left_radius=20,
            border_top_left_radius=20)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    game_board.clear()
                    ai_turn = False
            #exit 
            exitButton = pygame.Rect(5 * (width / 2), (height / 2), width /  2.5, 50)
            exit = smallFont.render("Exit", True, black)
            exitRect = exit.get_rect()
            exitButton.center=((width / 2), 540)
            exitRect.center = exitButton.center
            pygame.draw.rect(screen, white, exitButton,border_top_right_radius=20,
            border_bottom_right_radius=20,border_bottom_left_radius=20,
            border_top_left_radius=20)
            screen.blit(exit, exitRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if exitButton.collidepoint(mouse):
                    time.sleep(0.2)
                    pygame.Quit()
                    
        else:
            againButton = pygame.Rect(5 * (width / 2), (height / 2), width /  2.5, 50)
            again = smallFont.render("Back to Menu", True, black)
            againRect = again.get_rect()
            againButton.center=((width / 2), 520)
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton,border_top_right_radius=20,
             border_bottom_right_radius=20,border_bottom_left_radius=20,
            border_top_left_radius=20)
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

