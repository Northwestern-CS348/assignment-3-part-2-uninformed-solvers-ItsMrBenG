from solver import *
from queue import *


class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables().
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.
        Returns:
            True if the desired solution state is reached, False otherwise
        """
        start = self.currentState.state    
        win = self.victoryCondition    


        if (start == win):    
            return True   

        CURRENT = self.currentState      

        if self.gm.getMovables():  
            for movable in self.gm.getMovables():     

                self.gm.makeMove(movable)     

                child_state = GameState(self.gm.getGameState(), (CURRENT.depth + 1), movable)     
                CURRENT.children.append(child_state)     
                child_state.parent = CURRENT    

                self.gm.reverseMove(movable)     

            for child in CURRENT.children:   
                if child not in self.visited:   

                    self.visited[child] = True    
                    self.gm.makeMove(child.requiredMovable)   
                    self.currentState = child   

                    break

        else:

            self.gm.reverseMove(self.currentState.requiredMovable)


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
    q = Queue()
    move_counter = 0

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.
        Returns:
            True if the desired solution state is reached, False otherwise
        """
        visited = self.visited   
        CURRENT = self.currentState.state      
        VIC = self.victoryCondition   

        if CURRENT == VIC:    

            if (self.q != self.q.empty()):  

                while not self.q.empty():  

                    self.q.get()

            return True

        if (self.gm.getMovables()):
            for i in self.gm.getMovables():  

                self.gm.makeMove(i)
                c = GameState(self.gm.getGameState(), 0, i)   
                self.currentState.children.append(c)   
                c.parent = self.currentState
                self.gm.reverseMove(i)   

        for i in self.currentState.children:   
            if i not in visited:   

                self.q.put(i)   

        while not self.q.empty():   
   
            c = self.q.get()    

            if c not in visited:    

                CURRENT = self.currentState   
                vec1 = []   

                while (CURRENT.requiredMovable):  

                    vec1.append(CURRENT.requiredMovable)   
                    CURRENT = CURRENT.parent   

                CURRENT = c   
                vec2 = []   

                while CURRENT.requiredMovable:    

                    vec2.append(CURRENT.requiredMovable)   
                    CURRENT = CURRENT.parent  

                vec2 = reversed(vec2)   

                for k in vec1:    

                    self.gm.reverseMove(k)    

                for j in vec2:    

                    self.gm.makeMove(j)    

                visited[c] = True  

                self.currentState = c   
                self.move_counter = self.move_counter + 1   
                self.currentState.depth = self.move_counter   

                break  
  
        return False  








