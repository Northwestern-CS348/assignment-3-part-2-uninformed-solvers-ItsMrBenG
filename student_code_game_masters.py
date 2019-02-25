from game_master import GameMaster
from read import *
from util import *


class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.
        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?d ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the ds on the peg. ds
        should be represented by integers, with the smallest d
        represented by 1, and the second smallest 2, etc.
        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest d onTop on top of the larger ones.
        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))
        Returns:
            A Tuple of Tuples that represent the game state
        """
        result = []
        for i in range(0, 3):
            p = []
            my_bindings = self.kb.kb_ask(parse_input("fact: (on ?x peg" + str(i + 1) + ")"))
            if my_bindings:
                for j in my_bindings:
                    p.append(int(j['?x'][-1]))
            p.sort()
            result.append(tuple(p))
        return tuple(result)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.
        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable d1 peg1 peg3)
        Args:
            movable_statement: A Statement object that contains one of the currently viable moves
        Returns:
            None
        """
        # Student code goes here
        disco = str(movable_statement.terms[0])      
        pegso = str(movable_statement.terms[1])      
        pegdi = str(movable_statement.terms[2])       

        check_disco = self.kb.kb_ask(parse_input("fact: (onTop " + disco + " ?y)"))  
        check_pegdi = self.kb.kb_ask(parse_input("fact: (top " + " ?x" + " " + pegdi + ")")) 
  
        if check_disco:   

            new = self.kb.kb_ask(parse_input("fact: (onTop " + disco + " ?y)"))[0]  
            self.kb.kb_retract(parse_input("fact: (onTop " + disco + " " + new['?y'] + ")")) 
            self.kb.kb_assert(parse_input("fact: (top " + new['?y'] + " " + pegso + ")"))     
    
        else:   

            self.kb.kb_assert(parse_input("fact: (empty " + pegso + ")"))    

        if check_pegdi:  

            old = self.kb.kb_ask(parse_input("fact: (top " + " ?x" + " " + pegdi + ")"))[0]  
            self.kb.kb_retract(parse_input("fact: (top " + old['?x'] + " " + pegdi + ")"))  
            self.kb.kb_assert(parse_input("fact: (onTop " + disco + " " + old['?x'] + ")"))     

        else:

            self.kb.kb_retract(parse_input("fact: (empty " + pegdi + ")"))    

        self.kb.kb_retract(parse_input("fact: (on " + disco + " " + pegso + ")"))  
        self.kb.kb_assert(parse_input("fact: (on " + disco + " " + pegdi + ")"))     
        self.kb.kb_retract(parse_input("fact: (top " + disco + " " + pegso + ")"))      
        self.kb.kb_assert(parse_input("fact: (top " + disco + " " + pegdi + ")"))   

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.
        Args:
            movable_statement: A Statement object that contains one of the previously viable moves
        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))


class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.
        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.
        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))
        Returns:
            A Tuple of Tuples that represent the game state
        """
        # Student code goes here

        t1 = []   
        t2 = []   
        t3 = []  
        result = [] 

        for i in range(1, 4):   

            z = self.kb.kb_ask(parse_input("fact: (loc ?tile pos" + str(i) + " pos1)"))    

            if (z):

                LOB = self.kb.kb_ask(parse_input("fact: (loc ?tile pos" + str(i) + " pos1)"))   
                tuple_bind = LOB[0]  
                tuple_str = tuple_bind['?tile']  

                if (tuple_str == "empty"):  

                    tuple_int = -1   

                elif (tuple_str != "empty"):  

                    tuple_int = int(tuple_str[-1])      

                t1.append(tuple_int)   

        for j in range(1, 4):    

            z = self.kb.kb_ask(parse_input("fact: (loc ?tile pos" + str(j) + " pos2)"))   

            if (z):   

                LOB = self.kb.kb_ask(parse_input("fact: (loc ?tile pos" + str(j) + " pos2)"))   
                tuple_bind = LOB[0]  
                tuple_str = tuple_bind['?tile']    

                if (tuple_str == "empty"):   

                    tuple_int = -1   

                elif (tuple_str != "empty"):    

                    tuple_int = int(tuple_str[-1])   

                t2.append(tuple_int)   

        for k in range(1, 4):   

            z = self.kb.kb_ask(parse_input("fact: (loc ?tile pos" + str(k) + " pos3)"))   

            if (z):   
  
                LOB = self.kb.kb_ask(parse_input("fact: (loc ?tile pos" + str(k) + " pos3)"))   
                tuple_bind = LOB[0]
                tuple_str = tuple_bind['?tile']  

                if (tuple_str == "empty"):   

                    tuple_int = -1  

                elif (tuple_str != "empty"):    

                    tuple_int = int(tuple_str[-1])   

                t3.append(tuple_int)  

        result.append(tuple(t1))
        result.append(tuple(t2))
        result.append(tuple(t3))
        return tuple(result)  

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.
        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)
        Args:
            movable_statement: A Statement object that contains one of the currently viable moves
        Returns:
            None
        """
        # Student code goes here

        p = parse_input("fact: (loc " + str(movable_statement.terms[0]) + " " + str(movable_statement.terms[1]) + " " + str(movable_statement.terms[2]) + ")")
        p1 = parse_input("fact: (loc  empty " + str(movable_statement.terms[3]) + " " + str(movable_statement.terms[4]) + ")")
        p2 = parse_input("fact: (loc " + str(movable_statement.terms[0]) + " " + str(movable_statement.terms[3]) + " " + str(movable_statement.terms[4]) + ")")
        p3 = parse_input("fact: (loc  empty " + str(movable_statement.terms[1]) + " " + str(movable_statement.terms[2]) + ")")

        self.kb.kb_retract(p)
        self.kb.kb_retract(p1)
        self.kb.kb_assert(p2)
        self.kb.kb_assert(p3)

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.
        Args:
            movable_statement: A Statement object that contains one of the previously viable moves
        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))


