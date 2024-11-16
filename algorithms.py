from state import State
from queue import Queue
import numpy as np
from direction import Direction
from collections import deque

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
    
    @classmethod
    def generateBFSPath(cls,initial_state):
        bfs_queue = Queue(-1)
        bfs_queue.put(initial_state)
        visited_states = []
        path = []
        state = cls.bfs(bfs_queue,visited_states)
        while state is not None:
            path.append(state)
            state = state.prev_states
        return path
    
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

    
    
        
        