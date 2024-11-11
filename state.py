from cellTypes import Type
from direction import Direction
from cell import Cell
class State:
    
    def __init__(self, grid, status = False, prev_states = None, next_states = []):
        self.grid = grid
        self.status = status
        self.prev_states = prev_states
        self.next_states = next_states
        
    def getDirectionalCell(self, row, column, direction,count = 1):
        new_row, new_col = row, column
        if direction == Direction.UP.value:
            new_row -= count
        elif direction == Direction.DOWN.value:
            new_row += count
        elif direction == Direction.LEFT.value:
            new_col -= count
        elif direction == Direction.RIGHT.value:
            new_col += count

        if 0 <= new_row < len(self.grid) and 0 <= new_col < len(self.grid[0]):
            return {'row': new_row, 'column': new_col}
        else:
            return None 
        
    def getPlayerCells(self,grid):
        player_cells = []
        for row_index, row in enumerate(self.grid):
            for col_index, cell in enumerate(row):
                if(cell.type == Type.PLAYER.value):
                    player_cells.append(
                        {
                            'cell': cell,
                            'row': row_index,
                            'column': col_index
                        }
                    )
        return player_cells

        
    def checkMove(self, row, column, grid, direction, count = 1):
        directional_cell_index = self.getDirectionalCell(row, column, direction, count)
        if directional_cell_index is None:
            return False
        checking_cell = grid[directional_cell_index['row']][directional_cell_index['column']]
        if checking_cell.type == Type.EMPTY.value or checking_cell.type == Type.GOAL.value or (checking_cell.type == Type.PLAYER.value and count > 1):
            return True
        return False
    
    def getPlayerCell(self, cell, grid):
        for index_row, row in enumerate(grid):
            for index_col, col in enumerate(row):
                if(col.type == cell.type and col.color == cell.color):
                    return {
                        'cell':col,
                        'row': index_row,
                        'column': index_col
                        }

        
    def checkAvailableMoves(self):
        available_moves = []
        player_cells = self.getPlayerCells(self.grid)
        for cell in player_cells:
            for direction in Direction.list():
                if(self.checkMove(cell['row'], cell['column'], self.grid, direction)):
                    available_moves.append(direction)
        return available_moves
    
    def move(self, grid, direction, count=0):
        availability = []
        running = True
        player_cells = self.getPlayerCells(grid)
        availability_row = [False for _ in range(len(player_cells))]
        while running:
            availability.append(availability_row[:])

            for index, cell in enumerate(player_cells):
                if len(availability) == 1:
                    availability[-1][index] = self.checkMove(cell['row'], cell['column'], grid, direction)
                elif len(availability) >= 2 and availability[-2][index]:
                    availability[-1][index] = self.checkMove(cell['row'], cell['column'], grid, direction, len(availability))
            
            if not any(availability[-1]):
                running = False

        print(availability)
        for index_row, row in enumerate(availability):
            for index_col, col in enumerate(row):
                print(col, index_row, index_col)
                print()
                if col:
                    grid_cell = self.getPlayerCell(player_cells[index_col]['cell'], grid)
                    directional_cell = self.getDirectionalCell(grid_cell['row'], grid_cell['column'], direction)
                    
                    if directional_cell is not None and self.checkMove(grid_cell['row'], grid_cell['column'], grid, direction):
                        # print(grid[grid_cell['row']][grid_cell['column']].type == Type.GOAL.value)
                        if(grid[directional_cell['row']][directional_cell['column']].type == Type.GOAL.value and grid[directional_cell['row']][directional_cell['column']].color == player_cells[index_col]['cell'].color):
                            grid[grid_cell['row']][grid_cell['column']], grid[directional_cell['row']][directional_cell['column']] = \
                                Cell(Type.EMPTY.value), Cell(Type.EMPTY.value)
                            self.status = True
                            break
                               
                        if(grid[directional_cell['row']][directional_cell['column']].type == Type.GOAL.value and grid[directional_cell['row']][directional_cell['column']].color != player_cells[index_col]['cell'].color):
                             grid[grid_cell['row']][grid_cell['column']].previous_color = grid[directional_cell['row']][directional_cell['column']].color
                             
                        grid[grid_cell['row']][grid_cell['column']], grid[directional_cell['row']][directional_cell['column']] = \
                            grid[directional_cell['row']][directional_cell['column']], grid[grid_cell['row']][grid_cell['column']]
                            
                        if(grid[directional_cell['row']][directional_cell['column']].previous_color is not None):
                            if(grid[grid_cell['row']][grid_cell['column']].color is None):
                                grid[grid_cell['row']][grid_cell['column']] = Cell(Type.GOAL.value,grid[directional_cell['row']][directional_cell['column']].previous_color)
                                grid[directional_cell['row']][directional_cell['column']].previous_color = None
                            else:
                                grid[grid_cell['row']][grid_cell['column']] = Cell(Type.EMPTY.value)
                        
                        player_cells[index_col] = {
                            'cell':grid[directional_cell['row']][directional_cell['column']],
                            'row': directional_cell['row'],
                            'column':directional_cell['column']
                        }
        
        return State(grid, False, self, [])
    
    def getNextStates(self):
        available_moves = self.checkAvailableMoves()
        for move in available_moves:
            self.next_states.append([self.move(self.grid, move), move])