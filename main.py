import pygame
from state import State
from cellTypes import Type
from direction import Direction
from cell import Cell
from color import Color
from algorithms import Algorithms



pygame.init()

# grid = [
#     [Cell(Type.EMPTY.value) for _ in range(6)] for _ in range(1)
# ]

# grid[0][0] = Cell(Type.PLAYER.value, Color.RED.value)
# grid[0][5] = Cell(Type.GOAL.value, Color.RED.value)


grid = [
    [Cell(Type.EMPTY.value) for _ in range(6)] for _ in range(10)
]

grid[0][0] = Cell(Type.WALL.value)
grid[0][2] = Cell(Type.WALL.value)
grid[0][3] = Cell(Type.WALL.value)
grid[1][3] = Cell(Type.WALL.value)
grid[2][3] = Cell(Type.WALL.value)
grid[2][0] = Cell(Type.WALL.value)
grid[2][1] = Cell(Type.WALL.value)
grid[3][4] = Cell(Type.WALL.value)
grid[3][5] = Cell(Type.WALL.value)
grid[4][0] = Cell(Type.WALL.value)
grid[6][0] = Cell(Type.WALL.value)
grid[6][1] = Cell(Type.WALL.value)
grid[6][2] = Cell(Type.WALL.value)
grid[7][2] = Cell(Type.WALL.value)
grid[8][2] = Cell(Type.WALL.value)
grid[9][2] = Cell(Type.WALL.value)
grid[6][4] = Cell(Type.WALL.value)
grid[6][5] = Cell(Type.WALL.value)
grid[9][3] = Cell(Type.WALL.value)
grid[9][5] = Cell(Type.WALL.value)
grid[5][2] = Cell(Type.WALL.value)
grid[0][1] = Cell(Type.GOAL.value, Color.RED.value)
grid[5][3] = Cell(Type.GOAL.value, Color.ORANGE.value)
grid[7][4] = Cell(Type.GOAL.value, Color.BLUE.value)
grid[9][4] = Cell(Type.GOAL.value, Color.GREEN.value)
grid[3][3] = Cell(Type.PLAYER.value, Color.RED.value)
grid[3][0] = Cell(Type.PLAYER.value, Color.BLUE.value)
grid[5][0] = Cell(Type.PLAYER.value, Color.ORANGE.value)
grid[5][5] = Cell(Type.PLAYER.value, Color.GREEN.value)



WIDTH, HEIGHT = len(grid[0] * 50), len(grid * 50)
CELL_SIZE = 50

player_color = Color.getColor(Color.ORANGE.value)

COLOR_EMPTY = (255, 255, 255)
COLOR_WALL = (0, 0, 0)
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
print("pathzzzzzzzzzzzzzzz")
path = []

class Button:
    def __init__(self, text, x, y, width, height, color=(200,200,200), hover_color=(100,100,100)):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color

    def draw(self, screen, mouse_pos):
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        text_surface = font.render(self.text, True, (0,0,0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click
    
bfs_button = Button("BFS", WIDTH/4, HEIGHT/20, WIDTH/2, HEIGHT/4)
dfs_button = Button("DFS", WIDTH/4, (7 * HEIGHT)/20, WIDTH/2, HEIGHT/4)
play_button = Button("Play", WIDTH/4, (13 * HEIGHT)/20, WIDTH/2, HEIGHT/4)

bfs = False
dfs = False
play = False

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
state_number = [0]
def handle_input(state, state_number):

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_UP]:
        state = state.move(state.grid, Direction.UP.value)

    elif keys[pygame.K_DOWN]:
        state = state.move(state.grid, Direction.DOWN.value)

    elif keys[pygame.K_LEFT]:
        state = state.move(state.grid, Direction.LEFT.value)

    elif keys[pygame.K_RIGHT]:
        state_number[0]  += 1
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

print(play)
running = True
while running:
    screen.fill((255, 255, 255))
    print(play)
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()[0]  # Left mouse button

    if not bfs and not dfs and not play:
        bfs_button.draw(screen, mouse_pos)
        dfs_button.draw(screen, mouse_pos)
        play_button.draw(screen, mouse_pos)


    # Check for button clicks
    if bfs_button.is_clicked(mouse_pos, mouse_click):
        path = Algorithms.generateUCSPath(state)
        bfs = True
        pygame.time.wait(200)  # Small delay for visual feedback

    if dfs_button.is_clicked(mouse_pos, mouse_click):
        path = Algorithms.recursiveDFS(state)
        bfs = True # Call DFS
        pygame.time.wait(200) 
        
    if play_button.is_clicked(mouse_pos, mouse_click):
        play = True # Call DFS
            


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

    if bfs or dfs:
        state = handle_input(state, state_number)
        print(state_number[0])
        draw_grid(path[state_number[0]].grid)
    if play :
        state = handle_input(state, state_number)
        print(state_number[0])
        draw_grid(state.grid)
            


    pygame.display.flip()
    clock.tick(10) 

# for state in path:
#     screen.fill((255, 255, 255))
#     for x in range(2000):
#         draw_grid(state.grid)


pygame.quit()
