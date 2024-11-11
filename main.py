import pygame
from state import State
from cellTypes import Type
from direction import Direction
from cell import Cell
from color import Color



pygame.init()

grid = [
    [Cell(Type.EMPTY.value) for _ in range(5)] for _ in range(10)
]

grid[2][0] = Cell(Type.PLAYER.value, Color.RED.value)
grid[1][3] = Cell(Type.WALL.value)
grid[2][1] = Cell(Type.WALL.value)
grid[2][3] = Cell(Type.WALL.value)
grid[3][3] = Cell(Type.WALL.value)
grid[4][2] = Cell(Type.WALL.value)
grid[4][3] = Cell(Type.WALL.value)
grid[6][4] = Cell(Type.WALL.value)
grid[7][0] = Cell(Type.WALL.value)
grid[7][1] = Cell(Type.WALL.value)
grid[7][2] = Cell(Type.WALL.value)
grid[8][0] = Cell(Type.WALL.value)
grid[9][0] = Cell(Type.WALL.value)
grid[9][1] = Cell(Type.WALL.value)
grid[9][2] = Cell(Type.WALL.value)
grid[9][3] = Cell(Type.WALL.value)
grid[9][4] = Cell(Type.WALL.value)
grid[3][2] = Cell(Type.GOAL.value, Color.RED.value)
grid[1][2] = Cell(Type.PLAYER.value, Color.BLUE.value) 
grid[0][4] = Cell(Type.GOAL.value, Color.BLUE.value) 


WIDTH, HEIGHT = len(grid[0] * 50), len(grid * 50)
CELL_SIZE = 50

player_color = Color.getColor(Color.ORANGE.value)

COLOR_EMPTY = (255, 255, 255)
COLOR_WALL = (100, 100, 100)
COLOR_TEXT = (0, 0, 0)
COLOR_BUTTON = (200, 50, 50)
COLOR_BUTTON_HOVER = (255, 80, 80)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zero Squares Game")


font = pygame.font.Font(None, 36)


clock = pygame.time.Clock()

ROWS = len(grid)
COLS = len(grid[0]) if ROWS > 0 else 0


state = State(grid)

def draw_grid(grid):

    for row in range(min(ROWS, len(grid))):
        for col in range(min(COLS, len(grid[row]))):
            cell = grid[row][col]
            color = COLOR_EMPTY

            if cell.type == Type.WALL.value:
                color = COLOR_WALL
            elif cell.type == Type.PLAYER.value:
                color_rgb = Color.getColor(cell.color)
                color = (color_rgb['r'], color_rgb['g'], color_rgb['b'])
            elif cell.type == Type.GOAL.value:
                color_rgb = Color.getColor(cell.color)
                color = (color_rgb['r'], color_rgb['g'], color_rgb['b'])

            if cell.type != Type.GOAL.value:
                pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, COLOR_EMPTY, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            
            if cell.type == Type.GOAL.value or cell.type == Type.EMPTY.value:
                pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3) 
            elif cell.type == Type.PLAYER.value and cell.previous_color != None:
                previous_color_rgb = Color.getColor(cell.previous_color)
                previous_color = (previous_color_rgb['r'], previous_color_rgb['g'], previous_color_rgb['b'])
                pygame.draw.rect(screen, previous_color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3) 
            else:
                pygame.draw.rect(screen, (0, 0, 0), (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1) 

def handle_input(state):

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_UP]:
        state = state.move(state.grid, Direction.UP.value)

    elif keys[pygame.K_DOWN]:
        state = state.move(state.grid, Direction.DOWN.value)

    elif keys[pygame.K_LEFT]:
        state = state.move(state.grid, Direction.LEFT.value)

    elif keys[pygame.K_RIGHT]:
        state = state.move(state.grid, Direction.RIGHT.value)

    return state

def show_success_message():

    success_text = font.render("Success! All players reached their goals.", True, COLOR_TEXT)
    screen.blit(success_text, ((WIDTH - success_text.get_width()) // 2, HEIGHT // 2 - 50))


    button_text = font.render("Play Again", True, (255, 255, 255))
    button_rect = pygame.Rect((WIDTH // 2 - 75, HEIGHT // 2 + 20), (150, 50))


    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, COLOR_BUTTON_HOVER, button_rect)
    else:
        pygame.draw.rect(screen, COLOR_BUTTON, button_rect)

    screen.blit(button_text, (button_rect.x + (button_rect.width - button_text.get_width()) // 2, button_rect.y + (button_rect.height - button_text.get_height()) // 2))
    
    return button_rect

def reset_game():

    global state, grid
    grid = [
        [Cell(Type.EMPTY.value) for _ in range(6)] for _ in range(6)
    ]
    grid[0][1] = Cell(Type.PLAYER.value)
    grid[0][3] = Cell(Type.WALL.value)
    grid[0][4] = Cell(Type.GOAL.value)
    grid[1][1] = Cell(Type.PLAYER.value) 
    grid[1][4] = Cell(Type.GOAL.value)    
    state = State(grid)


running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if state.status:  
                if show_success_message().collidepoint(event.pos):
                    reset_game()  

    if state.status:
        show_success_message()  
    else:
       
        state = handle_input(state)
        draw_grid(state.grid)


    pygame.display.flip()
    clock.tick(10) 


pygame.quit()
