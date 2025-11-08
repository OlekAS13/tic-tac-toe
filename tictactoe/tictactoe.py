import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((1000, 695))
pygame.display.set_caption("Tic Tac Toe  |  by OlekAS13")


monosansVerySmall = pygame.font.Font("monosans.ttf", 30)
monosansSmall = pygame.font.Font("monosans.ttf", 60)
monosansBig = pygame.font.Font("monosans.ttf", 100)

gameState = "menu"
player = " "
board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
won = False

# BACKGROUND elements

# tile  X O  128x128
#       O X
tile_size = 64
tile_w = tile_size * 2
tile_h = tile_size * 2
tile_surface = pygame.Surface((tile_w, tile_h))
tile_surface.fill("black")

# MAIN MENU elements

tttText = monosansBig.render("Tic Tac Toe", True, "white")
tttTextY = -100

# Create button text surfaces
playText = monosansSmall.render("Play", True, "white")
creditsText = monosansSmall.render("Credits", True, "white")

# Button positions and rectangles
creditsButtonY = 700
creditsButton = pygame.Rect(300, creditsButtonY, 450, 100)
creditsHovered = False
creditsTextActual = monosansVerySmall.render("Game developed by Aleksander Stachura\n\nThe Game is licenced under GNU GPL v3\n\nEnjoy the game!", True, "white")

playButtonY = 700
playButton = pygame.Rect(300, playButtonY, 450, 100)
playHovered = False

# MODE SELECTION elements
singleplayerText = monosansSmall.render("Singleplayer", True, "white")
multiplayerText = monosansSmall.render("Multiplayer", True, "white")
backText = monosansSmall.render("Back", True, "white")

singleplayerButtonY = 700
singleplayerButton = pygame.Rect(300, singleplayerButtonY, 450, 100)
singleplayerHovered = False

multiplayerButtonY = 700
multiplayerButton = pygame.Rect(300, multiplayerButtonY, 450, 100)
multiplayerHovered = False

backButtonY = 700
backButton = pygame.Rect(300, backButtonY, 450, 100)
backHovered = False

# CREDITS elements
creditsTextLines = [
    "Tic Tac Toe",
    "",
    "Developed by",
    "Aleksander Stachura",
    "",
    "Enjoy the game!",
    "",
    "Made with Python",
    "and Pygame"
]
creditsTextSurfaces = [monosansSmall.render(line, True, "white") for line in creditsTextLines]
creditsTextY = -600  # Start above screen

creditsBackButton = pygame.Rect(300, 700, 450, 100)  # Start off-screen like other buttons
creditsBackText = monosansSmall.render("Back", True, "white")
creditsBackHovered = False

# Button colors and scale
BUTTON_COLOR_NORMAL = (50, 50, 50)
BUTTON_COLOR_HOVER = (70, 70, 70)
BUTTON_SCALE_HOVER = 1.1

# GAME BOARD elements
BOARD_COLOR = BUTTON_COLOR_NORMAL
BOARD_LINE_WIDTH = 8

# Game pieces
X_piece = monosansBig.render("X", True, "white")
O_piece = monosansBig.render("O", True, "white")

# Quit button
quitText = monosansVerySmall.render("Quit", True, "white")
quitButton = pygame.Rect(850, 625, 100, 50)  # bottom-right corner
quitHovered = False
QUIT_BUTTON_COLOR = (30, 30, 30)

# Board dimensions
BOARD_SIZE = 450  # Size of the actual board
BOARD_MARGIN_TOP = 125  # Distance from top edge
BOARD_MARGIN_LEFT = (1000 - 450) // 2  # Center horizontally ((screen width - board size) / 2)
board_progress = 0.0  # Animation progress
winning_indices = None  # Store winning line indices

# Line coordinates (start positions, will be animated)
vertical_line1_length = 0
vertical_line2_length = 0
horizontal_line1_length = 0
horizontal_line2_length = 0

# Board tile buttons (invisible buttons for gameplay)
CELL_SIZE = BOARD_SIZE // 3  # Size of each cell including the line
board_buttons = []

# Create 9 buttons in a 3x3 grid
for row in range(3):
    for col in range(3):
        x = BOARD_MARGIN_LEFT + col * CELL_SIZE  # Start of cell
        y = BOARD_MARGIN_TOP + row * CELL_SIZE
        # Adjust position by line width when after first column/row
        x += (BOARD_LINE_WIDTH // 2) if col > 0 else 0
        y += (BOARD_LINE_WIDTH // 2) if row > 0 else 0
        # Adjust size by line width for edge cells, adding 1px to stretch
        width = CELL_SIZE - (BOARD_LINE_WIDTH if col > 0 else BOARD_LINE_WIDTH // 2) + 1
        height = CELL_SIZE - (BOARD_LINE_WIDTH if row > 0 else BOARD_LINE_WIDTH // 2) + 1
        button = pygame.Rect(x, y, width, height)
        board_buttons.append(button)

# filling tile with X and O
for y in range(2):
    for x in range(2):
        letter = "X" if (x + y) % 2 == 0 else "O"
        text = monosansSmall.render(letter, True, [30, 30, 30])
        # center text in tile
        tx = x * tile_size + (tile_size - text.get_width()) // 2
        ty = y * tile_size + (tile_size - text.get_height()) // 2
        tile_surface.blit(text, (tx, ty))

offset_x = 0
offset_y = 0
scroll_speed = 1

clock = pygame.time.Clock()

def drawGameState():
    """Draw the current game state including background and UI elements."""
    global offset_x, offset_y, playButton, creditsButton, singleplayerButton, multiplayerButton, backButton
    
    screen.fill("black")

    # Draw background for menu, mode selection, and credits states
    if gameState in ["menu", "choose mode", "credits"]:
        # Update background scroll
        offset_x = (offset_x + scroll_speed) % tile_w
        offset_y = (offset_y + scroll_speed) % tile_h

        # Draw tiled background
        sw, sh = screen.get_width(), screen.get_height()
        start_x = -tile_w
        start_y = -tile_h
        end_x = sw + tile_w
        end_y = sh + tile_h

        y = start_y
        while y < end_y:
            x = start_x
            while x < end_x:
                screen.blit(tile_surface, (x - offset_x, y - offset_y))
                x += tile_w
            y += tile_h

        if gameState == "menu":
            # Update main menu button positions and maintain center alignment
            screen_center_x = screen.get_width() / 2
            button_width = 450  # Width of our buttons
            button_x = screen_center_x - button_width / 2

            playButton.x = button_x
            playButton.y = playButtonY
            creditsButton.x = button_x
            creditsButton.y = creditsButtonY

            # Draw main menu UI elements
            screen.blit(tttText, (screen.get_width() / 2 - tttText.get_width() / 2, tttTextY))

            # Draw play button with hover effect
            if playHovered:
                hoverRect = pygame.Rect(playButton.x - (playButton.width * (BUTTON_SCALE_HOVER - 1)) / 2,
                                    playButton.y - (playButton.height * (BUTTON_SCALE_HOVER - 1)) / 2,
                                    playButton.width * BUTTON_SCALE_HOVER,
                                    playButton.height * BUTTON_SCALE_HOVER)
                pygame.draw.rect(screen, BUTTON_COLOR_HOVER, hoverRect, border_radius=10)
                playTextRect = playText.get_rect(center=hoverRect.center)
                screen.blit(playText, playTextRect)
            else:
                pygame.draw.rect(screen, BUTTON_COLOR_NORMAL, playButton, border_radius=10)
                playTextRect = playText.get_rect(center=playButton.center)
                screen.blit(playText, playTextRect)

            # Draw credits button with hover effect
            if creditsHovered:
                hoverRect = pygame.Rect(creditsButton.x - (creditsButton.width * (BUTTON_SCALE_HOVER - 1)) / 2,
                                    creditsButton.y - (creditsButton.height * (BUTTON_SCALE_HOVER - 1)) / 2,
                                    creditsButton.width * BUTTON_SCALE_HOVER,
                                    creditsButton.height * BUTTON_SCALE_HOVER)
                pygame.draw.rect(screen, BUTTON_COLOR_HOVER, hoverRect, border_radius=10)
                creditsTextRect = creditsText.get_rect(center=hoverRect.center)
                screen.blit(creditsText, creditsTextRect)
            else:
                pygame.draw.rect(screen, BUTTON_COLOR_NORMAL, creditsButton, border_radius=10)
                creditsTextRect = creditsText.get_rect(center=creditsButton.center)
                screen.blit(creditsText, creditsTextRect)

        elif gameState == "choose mode":
            # Update mode selection button positions and maintain center alignment
            screen_center_x = screen.get_width() / 2
            button_width = 450  # Width of our buttons
            button_x = screen_center_x - button_width / 2

            singleplayerButton.x = button_x
            singleplayerButton.y = singleplayerButtonY
            multiplayerButton.x = button_x
            multiplayerButton.y = multiplayerButtonY
            backButton.x = button_x
            backButton.y = backButtonY

            # Draw title
            screen.blit(tttText, (screen.get_width() / 2 - tttText.get_width() / 2, tttTextY))

            # Draw mode selection buttons
            if singleplayerHovered:
                hoverRect = pygame.Rect(singleplayerButton.x - (singleplayerButton.width * (BUTTON_SCALE_HOVER - 1)) / 2,
                                    singleplayerButton.y - (singleplayerButton.height * (BUTTON_SCALE_HOVER - 1)) / 2,
                                    singleplayerButton.width * BUTTON_SCALE_HOVER,
                                    singleplayerButton.height * BUTTON_SCALE_HOVER)
                pygame.draw.rect(screen, BUTTON_COLOR_HOVER, hoverRect, border_radius=10)
                textRect = singleplayerText.get_rect(center=hoverRect.center)
                screen.blit(singleplayerText, textRect)
            else:
                pygame.draw.rect(screen, BUTTON_COLOR_NORMAL, singleplayerButton, border_radius=10)
                textRect = singleplayerText.get_rect(center=singleplayerButton.center)
                screen.blit(singleplayerText, textRect)

            if multiplayerHovered:
                hoverRect = pygame.Rect(multiplayerButton.x - (multiplayerButton.width * (BUTTON_SCALE_HOVER - 1)) / 2,
                                    multiplayerButton.y - (multiplayerButton.height * (BUTTON_SCALE_HOVER - 1)) / 2,
                                    multiplayerButton.width * BUTTON_SCALE_HOVER,
                                    multiplayerButton.height * BUTTON_SCALE_HOVER)
                pygame.draw.rect(screen, BUTTON_COLOR_HOVER, hoverRect, border_radius=10)
                textRect = multiplayerText.get_rect(center=hoverRect.center)
                screen.blit(multiplayerText, textRect)
            else:
                pygame.draw.rect(screen, BUTTON_COLOR_NORMAL, multiplayerButton, border_radius=10)
                textRect = multiplayerText.get_rect(center=multiplayerButton.center)
                screen.blit(multiplayerText, textRect)

            if backHovered:
                hoverRect = pygame.Rect(backButton.x - (backButton.width * (BUTTON_SCALE_HOVER - 1)) / 2,
                                    backButton.y - (backButton.height * (BUTTON_SCALE_HOVER - 1)) / 2,
                                    backButton.width * BUTTON_SCALE_HOVER,
                                    backButton.height * BUTTON_SCALE_HOVER)
                pygame.draw.rect(screen, BUTTON_COLOR_HOVER, hoverRect, border_radius=10)
                textRect = backText.get_rect(center=hoverRect.center)
                screen.blit(backText, textRect)
            else:
                pygame.draw.rect(screen, BUTTON_COLOR_NORMAL, backButton, border_radius=10)
                textRect = backText.get_rect(center=backButton.center)
                screen.blit(backText, textRect)

        elif gameState == "credits":
            # Update credits back button position
            screen_center_x = screen.get_width() / 2
            button_width = 450
            button_x = screen_center_x - button_width / 2
            creditsBackButton.x = button_x

            # Draw credits text
            line_spacing = 60
            for i, textSurface in enumerate(creditsTextSurfaces):
                y_pos = creditsTextY + (i * line_spacing)
                x_pos = screen.get_width() / 2 - textSurface.get_width() / 2
                screen.blit(textSurface, (x_pos, y_pos))

            # Draw back button with hover effect
            if creditsBackHovered:
                hoverRect = pygame.Rect(creditsBackButton.x - (creditsBackButton.width * (BUTTON_SCALE_HOVER - 1)) / 2,
                                    creditsBackButton.y - (creditsBackButton.height * (BUTTON_SCALE_HOVER - 1)) / 2,
                                    creditsBackButton.width * BUTTON_SCALE_HOVER,
                                    creditsBackButton.height * BUTTON_SCALE_HOVER)
                pygame.draw.rect(screen, BUTTON_COLOR_HOVER, hoverRect, border_radius=10)
                textRect = creditsBackText.get_rect(center=hoverRect.center)
                screen.blit(creditsBackText, textRect)
            else:
                pygame.draw.rect(screen, BUTTON_COLOR_NORMAL, creditsBackButton, border_radius=10)
                textRect = creditsBackText.get_rect(center=creditsBackButton.center)
                screen.blit(creditsBackText, textRect)

    

    elif gameState == "play":
        # Draw the game board
        board_x = BOARD_MARGIN_LEFT
        board_y = BOARD_MARGIN_TOP

        # Draw vertical lines (aligned with tiles)
        pygame.draw.line(screen, BOARD_COLOR, 
                        (board_x + BOARD_SIZE//3, board_y),
                        (board_x + BOARD_SIZE//3, board_y + vertical_line1_length - 4),
                        BOARD_LINE_WIDTH)
        pygame.draw.line(screen, BOARD_COLOR,
                        (board_x + 2*BOARD_SIZE//3, board_y),
                        (board_x + 2*BOARD_SIZE//3, board_y + vertical_line2_length - 4),
                        BOARD_LINE_WIDTH)

        # Draw horizontal lines (aligned with tiles)
        pygame.draw.line(screen, BOARD_COLOR,
                        (board_x, board_y + BOARD_SIZE//3),
                        (board_x + horizontal_line1_length - 4, board_y + BOARD_SIZE//3),
                        BOARD_LINE_WIDTH)
        pygame.draw.line(screen, BOARD_COLOR,
                        (board_x, board_y + 2*BOARD_SIZE//3),
                        (board_x + horizontal_line2_length - 4, board_y + 2*BOARD_SIZE//3),
                        BOARD_LINE_WIDTH)
        
        # Draw board buttons and winning line highlight
        for i, button in enumerate(board_buttons):
            if winning_indices and i in winning_indices:
                pygame.draw.rect(screen, BUTTON_COLOR_HOVER, button, 0)  # Fill winning tiles
        
        # Draw X's and O's
        for i, button in enumerate(board_buttons):
            if board[i] == "X":
                text_rect = X_piece.get_rect(center=button.center)
                screen.blit(X_piece, text_rect)
            elif board[i] == "O":
                text_rect = O_piece.get_rect(center=button.center)
                screen.blit(O_piece, text_rect)
                        
        # Draw quit button
        if quitHovered:
            hoverRect = pygame.Rect(quitButton.x - (quitButton.width * (BUTTON_SCALE_HOVER - 1)) / 2,
                                quitButton.y - (quitButton.height * (BUTTON_SCALE_HOVER - 1)) / 2,
                                quitButton.width * BUTTON_SCALE_HOVER,
                                quitButton.height * BUTTON_SCALE_HOVER)
            pygame.draw.rect(screen, QUIT_BUTTON_COLOR, hoverRect, border_radius=5)
            quitTextRect = quitText.get_rect(center=hoverRect.center)
            screen.blit(quitText, quitTextRect)
        else:
            pygame.draw.rect(screen, QUIT_BUTTON_COLOR, quitButton, border_radius=5)
            quitTextRect = quitText.get_rect(center=quitButton.center)
            screen.blit(quitText, quitTextRect)

        
        if gamemode == "multiplayer":
            if not won:
                if player == "X":
                    xMoveText = monosansSmall.render("X Move", True, "white")
                    screen.blit(xMoveText, (10, 10))
                elif player == "O":
                    oMoveText = monosansSmall.render("O Move", True, "white")
                    screen.blit(oMoveText, (775, 10))
            elif won:
                if result != "tie":
                    wonText = monosansBig.render(f"{result} won", True, "white")
                    screen.blit(wonText, (350, 0))
                else:
                    tieText = monosansBig.render("Tie", True, "white")
                    screen.blit(tieText, (430, 0))
            


    pygame.display.flip()
    clock.tick(60)

def updateButtonHoverStates(mousePos):
    """Update button hover states based on mouse position."""
    global playHovered, creditsHovered, singleplayerHovered, multiplayerHovered, backHovered, quitHovered, creditsBackHovered
    
    if gameState == "menu":
        playHovered = playButton.collidepoint(mousePos)
        creditsHovered = creditsButton.collidepoint(mousePos)
    elif gameState == "choose mode":
        singleplayerHovered = singleplayerButton.collidepoint(mousePos)
        multiplayerHovered = multiplayerButton.collidepoint(mousePos)
        backHovered = backButton.collidepoint(mousePos)
    elif gameState == "play":
        quitHovered = quitButton.collidepoint(mousePos)
    elif gameState == "credits":
        creditsBackHovered = creditsBackButton.collidepoint(mousePos)

def showMainMenu():
    """Animate all menu elements appearing simultaneously."""
    global gameState, tttTextY, creditsButtonY, playButtonY, creditsButton, playButton, tttText

    gameState = "menu"

    tttText = monosansBig.render("Tic Tac Toe", True, "white")  # Reset title text

    # Starting positions
    title_start = -100
    credits_start = 700
    play_start = 700

    # Target positions
    title_target = 100
    credits_target = 450
    play_target = 300

    # Set initial positions
    tttTextY = title_start
    creditsButtonY = credits_start
    playButtonY = play_start

    # Animation control
    progress = 0.0  # Start at 0 for ease-out effect
    speed = 0.02   # Slightly faster than before for better feel

    # Animate until everything reaches its target
    while progress < 1:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update progress (going 0 → 1)
        progress = min(1.0, progress + speed)
        
        # Quadratic ease-out: start fast, end slow
        # When progress is small, ease_factor changes quickly
        # When progress is near 1, ease_factor changes slowly
        ease_factor = -(progress * (progress - 2))  # This gives true ease-out

        # Update all elements simultaneously using eased progress
        tttTextY = title_start + (title_target - title_start) * ease_factor
        creditsButtonY = credits_start + (credits_target - credits_start) * ease_factor
        playButtonY = play_start + (play_target - play_start) * ease_factor

        # Draw the current frame
        drawGameState()

    # Ensure everything is exactly at their targets
    tttTextY = title_target
    creditsButtonY = credits_target
    playButtonY = play_target

def showModeSelection():
    """Animate mode selection menu appearing."""
    global gameState, tttTextY, singleplayerButtonY, multiplayerButtonY, backButtonY, tttText

    gameState = "choose mode"

    # Change title text
    tttText = monosansBig.render("Choose mode", True, "white")

    # Starting positions
    title_start = -100
    singleplayer_start = 700
    multiplayer_start = 700
    back_start = 700

    # Target positions
    title_target = 100
    singleplayer_target = 300
    multiplayer_target = 420
    back_target = 580

    # Set initial positions
    tttTextY = title_start
    singleplayerButtonY = singleplayer_start
    multiplayerButtonY = multiplayer_start
    backButtonY = back_start

    # Animation control
    progress = 0.0
    speed = 0.02

    # Animate until everything reaches its target
    while progress < 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        progress = min(1.0, progress + speed)
        ease_factor = -(progress * (progress - 2))

        tttTextY = title_start + (title_target - title_start) * ease_factor
        singleplayerButtonY = singleplayer_start + (singleplayer_target - singleplayer_start) * ease_factor
        multiplayerButtonY = multiplayer_start + (multiplayer_target - multiplayer_start) * ease_factor
        backButtonY = back_start + (back_target - back_start) * ease_factor

        drawGameState()

    # Ensure everything is exactly at their targets
    tttTextY = title_target
    singleplayerButtonY = singleplayer_target
    multiplayerButtonY = multiplayer_target
    backButtonY = back_target

def showGameBoard():
    """Animate the game board lines rolling out."""
    global board_progress, vertical_line1_length, vertical_line2_length, horizontal_line1_length, horizontal_line2_length

    progress = 0.0
    speed = 0.02

    while progress < 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        progress = min(1.0, progress + speed)
        # Use the same easing as buttons for consistency
        ease_factor = -(progress * (progress - 2))

        # Animate line lengths
        vertical_line1_length = BOARD_SIZE * ease_factor
        vertical_line2_length = BOARD_SIZE * ease_factor
        horizontal_line1_length = BOARD_SIZE * ease_factor
        horizontal_line2_length = BOARD_SIZE * ease_factor

        drawGameState()

    # Ensure lines are exactly at their final lengths
    vertical_line1_length = BOARD_SIZE
    vertical_line2_length = BOARD_SIZE
    horizontal_line1_length = BOARD_SIZE
    horizontal_line2_length = BOARD_SIZE

def showCredits():
    """Animate credits screen appearing."""
    global gameState, creditsTextY, creditsBackButton

    gameState = "credits"

    # Starting positions
    text_start = -600
    back_start = 700

    # Target positions
    text_target = 0
    back_target = 570

    # Set initial positions
    creditsTextY = text_start
    creditsBackButton.y = back_start

    # Animation control
    progress = 0.0
    speed = 0.02

    while progress < 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        progress = min(1.0, progress + speed)
        ease_factor = -(progress * (progress - 2))

        creditsTextY = text_start + (text_target - text_start) * ease_factor
        creditsBackButton.y = back_start + (back_target - back_start) * ease_factor

        drawGameState()

    # Ensure everything is at their targets
    creditsTextY = text_target
    creditsBackButton.y = back_target

def checkWin(board):
    """Check if there is a winner on the board.
    Returns: (winner, winning_line) where:
    - winner is None if no winner, 'X' if X wins, 'O' if O wins, 'tie' if board is full
    - winning_line is a list of indices that form the winning line, or None if no winner"""
    
    # Check rows
    for i in range(0, 9, 3):  # Check each row (0, 3, 6)
        if board[i] != " " and board[i] == board[i+1] == board[i+2]:
            return board[i], [i, i+1, i+2]
    
    # Check columns
    for i in range(3):  # Check each column (0, 1, 2)
        if board[i] != " " and board[i] == board[i+3] == board[i+6]:
            return board[i], [i, i+3, i+6]
    
    # Check diagonals
    if board[0] != " " and board[0] == board[4] == board[8]:  # Top-left to bottom-right
        return board[0], [0, 4, 8]
    if board[2] != " " and board[2] == board[4] == board[6]:  # Top-right to bottom-left
        return board[2], [2, 4, 6]
    
    # Check for tie (board is full)
    if " " not in board:  # No empty spaces left
        return "tie", None
    
    # No winner yet
    return None, None

def hideGameBoard():
    """Animate the game board lines rolling back in."""
    global vertical_line1_length, vertical_line2_length, horizontal_line1_length, horizontal_line2_length

    progress = 0.0
    speed = 0.02

    # Starting positions (current full length)
    start_length = BOARD_SIZE

    while progress < 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        progress = min(1.0, progress + speed)
        # Use quadratic ease-in for retracting animation
        ease_factor = progress * progress

        # Animate lines retracting
        vertical_line1_length = start_length * (1 - ease_factor)
        vertical_line2_length = start_length * (1 - ease_factor)
        horizontal_line1_length = start_length * (1 - ease_factor)
        horizontal_line2_length = start_length * (1 - ease_factor)

        drawGameState()

    # Ensure lines are exactly at their initial lengths
    vertical_line1_length = 0
    vertical_line2_length = 0
    horizontal_line1_length = 0
    horizontal_line2_length = 0

def hideModeSelection():
    """Animate mode selection menu disappearing."""
    global gameState, tttTextY, singleplayerButtonY, multiplayerButtonY, backButtonY

    # Starting positions are current positions
    title_start = tttTextY
    singleplayer_start = singleplayerButtonY
    multiplayer_start = multiplayerButtonY
    back_start = backButtonY

    # Target positions (off screen)
    title_target = -100
    singleplayer_target = 700
    multiplayer_target = 700
    back_target = 700

    # Animation control
    progress = 0.0
    speed = 0.02

    while progress < 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        progress = min(1.0, progress + speed)
        ease_factor = progress * progress

        tttTextY = title_start + (title_target - title_start) * ease_factor
        singleplayerButtonY = singleplayer_start + (singleplayer_target - singleplayer_start) * ease_factor
        multiplayerButtonY = multiplayer_start + (multiplayer_target - multiplayer_start) * ease_factor
        backButtonY = back_start + (back_target - back_start) * ease_factor

        drawGameState()

    # Ensure everything is exactly at their targets
    tttTextY = title_target
    singleplayerButtonY = singleplayer_target
    multiplayerButtonY = multiplayer_target
    backButtonY = back_target

def hideCredits():
    """Animate credits screen disappearing."""
    global gameState, creditsTextY, creditsBackButton

    # Starting positions
    text_start = creditsTextY
    back_start = creditsBackButton.y

    # Target positions
    text_target = -600
    back_target = 700

    # Animation control
    progress = 0.0
    speed = 0.02

    while progress < 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        progress = min(1.0, progress + speed)
        ease_factor = progress * progress

        creditsTextY = text_start + (text_target - text_start) * ease_factor
        creditsBackButton.y = back_start + (back_target - back_start) * ease_factor

        drawGameState()

    # Ensure everything is at their targets
    creditsTextY = text_target
    creditsBackButton.y = back_target

def hideMainMenu():
    """Animate all menu elements disappearing simultaneously."""
    global gameState, tttTextY, creditsButtonY, playButtonY, creditsButton, playButton

    # Starting positions are current positions
    title_start = tttTextY
    credits_start = creditsButtonY
    play_start = playButtonY

    # Target positions (off screen)
    title_target = -100
    credits_target = 700
    play_target = 700

    # Animation control
    progress = 0.0  # Start at 0 for ease-in effect
    speed = 0.02   # Match show menu speed for consistency

    # Animate until everything reaches its target
    while progress < 1:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update progress (going 0 → 1 for ease-in)
        progress = min(1.0, progress + speed)
        
        # Quadratic ease-in: start slow, end fast
        # When progress is small, ease_factor changes slowly
        # When progress is near 1, ease_factor changes quickly
        ease_factor = progress * progress  # True quadratic ease-in

        # Update all elements simultaneously using eased progress
        tttTextY = title_start + (title_target - title_start) * ease_factor
        creditsButtonY = credits_start + (credits_target - credits_start) * ease_factor
        playButtonY = play_start + (play_target - play_start) * ease_factor

        # Draw the current frame
        drawGameState()

    # Ensure everything is exactly at their targets
    tttTextY = title_target
    creditsButtonY = credits_target
    playButtonY = play_target

# Show menu when game starts
showMainMenu()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEMOTION and gameState in ["menu", "choose mode", "play", "credits"]:
            updateButtonHoverStates(event.pos)
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # In menu state, check for button clicks
            if gameState == "menu":
                # Check play button click
                if playButton.collidepoint(mouse_x, mouse_y):
                    hideMainMenu()
                    showModeSelection()
                    
                # Check credits button click
                elif creditsButton.collidepoint(mouse_x, mouse_y):
                    hideMainMenu()
                    showCredits()
            
            # In choose mode state, handle mode selection buttons
            elif gameState == "choose mode":
                if singleplayerButton.collidepoint(mouse_x, mouse_y):
                    hideModeSelection()
                    gameState = "play"
                    gamemode = "singleplayer"
                    showGameBoard()
                    
                elif multiplayerButton.collidepoint(mouse_x, mouse_y):
                    hideModeSelection()
                    gameState = "play"
                    gamemode = "multiplayer"
                    showGameBoard()
                    player = random.choice(["X", "O"])
                    board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]

                elif backButton.collidepoint(mouse_x, mouse_y):
                    hideModeSelection()
                    showMainMenu()
            
            # In play state, handle board and quit button clicks
            elif gameState == "play":
                # Check for clicks on board tiles
                for i, button in enumerate(board_buttons):
                    if button.collidepoint(mouse_x, mouse_y):
                        # Here you'll add the logic for handling moves
                        # The tile index i corresponds to:
                        # 0 1 2
                        # 3 4 5
                        # 6 7 8

                        if board[i] == " " and not won:
                            # Make move
                            board[i] = player
                            
                            # Check for win or tie
                            result, win_line = checkWin(board)
                            if result is not None:
                                if result == "tie":
                                    print("It's a tie!")  # Replace with proper game over handling
                                    won = True
                                else:
                                    print(f"Player {result} wins!")  # Replace with proper win handling
                                    won = True
                                    #global winning_indices
                                    winning_indices = win_line

                            else:
                                # Switch players if game isn't over
                                player = "O" if player == "X" else "X"
                
                # Handle quit button
                if quitButton.collidepoint(mouse_x, mouse_y):
                    hideGameBoard()
                    showMainMenu()
                    player = " "
                    board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
                    won = False
                    #global winning_indices
                    winning_indices = None

            # In credits state, handle back button
            elif gameState == "credits":
                if creditsBackButton.collidepoint(mouse_x, mouse_y):
                    hideCredits()
                    showMainMenu()

    # Draw the current game state (handles all rendering)
    drawGameState()
