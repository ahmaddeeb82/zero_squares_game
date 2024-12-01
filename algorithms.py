from state import State
from queue import Queue
import numpy as np
from direction import Direction
from collections import deque
from heapq import heappush, heappop
from cellTypes import Type

class Algorithms:
    
    @classmethod
    def bfs(cls, queue, visited_states):
        state = queue.get()
        add_state = True
        for visited_state in visited_states:
            # print(State.checkGridEquation(state.grid, visited_state.grid))
            if State.checkGridEquation(state.grid, visited_state.grid):
                add_state = False
                break
        # if(len(visited_states) > 50):
        #     return
        if(add_state):
            visited_states.append(state)
        print("end game")
        print(visited_states[-1].status)
        if visited_states[-1].status:
            return state
        state.getNextStates()
        for next_state in state.next_states:
            queue.put(next_state[0])
        return cls.bfs(queue,visited_states)
    
    # @classmethod
    # def generateBFSPath(cls,initial_state):
    #     bfs_queue = Queue(-1)
    #     bfs_queue.put(initial_state)
    #     visited_states = []
    #     path = []
    #     state = cls.bfs(bfs_queue,visited_states)
    #     while state is not None:
    #         path.append(state)
    #         state = state.prev_states
    #     return path
    
    @classmethod
    def generateBFSPath(cls,initial_state):
        visited = set()
        queue = deque([(initial_state, [])])
        while queue:
            current_state, path = queue.popleft()
            if current_state.status:
                return path + [current_state]
            state_key = tuple(tuple(cell.type for cell in row) for row in current_state.grid)
            if state_key in visited:
                continue
            visited.add(state_key)
            current_state.getNextStates()
            for next_state in current_state.next_states:
                if next_state[0] and not any(State.checkGridEquation(next_state[0].grid, state.grid) for state in path):
                    queue.append((next_state[0], path + [current_state]))
        return []
    
    @classmethod
    def generateDFSPath(cls,initial_state):
        visited = set()
        stack = [(initial_state, [])]
        while stack:
            current_state, path = stack.pop()
            if current_state.status:
                return path + [current_state]
            state_key = tuple(tuple(cell.type for cell in row) for row in current_state.grid)
            if state_key in visited:
                continue
            visited.add(state_key)
            current_state.getNextStates()
            for next_state in current_state.next_states:
                if next_state[0] and not any(State.checkGridEquation(next_state[0].grid, state.grid) for state in path):
                    stack.append((next_state[0], path + [current_state]))
        return []
    
    @classmethod
    def dfs(cls, stack, visited_states):
        state = stack.pop()
        add_state = True
        for visited_state in visited_states:
            if State.checkGridEquation(state.grid, visited_state.grid):
                add_state = False
                break
        if(add_state):
            visited_states.append(state)
        if visited_states[-1].status:
            return state
        state.getNextStates()
        for next_state in state.next_states:
            stack.append(next_state[0])
        return cls.dfs(stack,visited_states)
    
    @classmethod
    def recursiveDFS(cls,initial_state):
        stack = [initial_state]
        visited_states = []
        path = []
        state = cls.dfs(stack,visited_states)
        while state is not None:
            path.append(state)
            state = state.prev_states
        path.reverse()
        return path
    
    from heapq import heappush, heappop

    @classmethod
    def generateUCSPath(cls, initial_state):
        priority_queue = []
        heappush(priority_queue, (initial_state.cost, initial_state, []))
        visited = set()

        while priority_queue:
            current_cost, current_state, path = heappop(priority_queue)

            if current_state.status:
                return path + [current_state]

            state_key = tuple(tuple(cell.type for cell in row) for row in current_state.grid)
            if state_key in visited:
                continue
            visited.add(state_key)

            current_state.getNextStates()
            for next_state in current_state.next_states:
                if next_state[0]:
                    next_state_cost = next_state[0].cost

                    if not any(State.checkGridEquation(next_state[0].grid, state.grid) for state in path):
                        heappush(priority_queue, (next_state_cost, next_state[0], path + [current_state]))

        return []
        
    @classmethod
    def generateAStarPath(cls, initial_state):
        priority_queue = []
        heappush(priority_queue, (0, initial_state, [])) 
        visited = set()

        while priority_queue:
            current_f, current_state, path = heappop(priority_queue)

            if current_state.status:  
                return path + [current_state]

            state_key = tuple(tuple(cell.type for cell in row) for row in current_state.grid)
            if state_key in visited:
                continue
            visited.add(state_key)

            current_state.getNextStates()
            for next_state in current_state.next_states:
                if next_state[0]:
                    g_cost = len(path) + 1  
                    h_cost = cls.heuristic(next_state[0])  
                    f_cost = g_cost + h_cost  

                    if not any(State.checkGridEquation(next_state[0].grid, state.grid) for state in path):
                        heappush(priority_queue, (f_cost, next_state[0], path + [current_state]))

        return []

    @staticmethod
    def heuristic(state):
        player_positions = [
            (r, c)
            for r, row in enumerate(state.grid)
            for c, cell in enumerate(row)
            if cell.type == Type.PLAYER.value
        ]
        goal_positions = [
            (r, c)
            for r, row in enumerate(state.grid)
            for c, cell in enumerate(row)
            if cell.type == Type.GOAL.value
        ]

        total_distance = 0
        for player in player_positions:
            for goal in goal_positions:
                if state.grid[player[0]][player[1]].color == state.grid[goal[0]][goal[1]].color:
                    total_distance += abs(player[0] - goal[0]) + abs(player[1] - goal[1])

        return total_distance
