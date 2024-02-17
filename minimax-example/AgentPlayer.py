from AdversarialSearch import AdversarialSearch

class AgentPlayer:

    def __init__(self, marble, name, depth):
        self.name = "Agent_Player_" + name # Agent Name
        self.myMarble = marble # Agent Marble
        self.depth = depth
        # Create Adversarial Search Agent
        self.agent = AdversarialSearch(self.myMarble, self.depth)

    # Method to determine which move to make on the board (by calling search agent)
    def move(self, board, top):
        return self.agent.findOptimalMove(board, top)

    # Method to return the player's name
    def getName(self):
        return self.name

