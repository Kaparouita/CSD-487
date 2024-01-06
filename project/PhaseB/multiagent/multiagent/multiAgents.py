# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.
      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.
        getAction chooses among the best options according to the evaluation function.
        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
      """
      Design a better evaluation function here.
      The evaluation function takes in the current and proposed successor
      GameStates (pacman.py) and returns a number, where higher numbers are better.
      The code below extracts some useful information from the state, like the
      remaining food (newFood) and Pacman position after moving (newPos).
      newScaredTimes holds the number of moves that each ghost will remain
      scared because of Pacman having eaten a power pellet.
      Print out these variables to see what you're getting, then combine them
      to create a masterful evaluation function.
      """
      # Useful information you can extract from a GameState (pacman.py)
      successorGameState = currentGameState.generatePacmanSuccessor(action)
      newPos = successorGameState.getPacmanPosition()
      newFood = successorGameState.getFood()
      newGhostStates = successorGameState.getGhostStates()
      newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

      "*** YOUR CODE HERE ***"

      score = successorGameState.getScore()

      for ghostState in newGhostStates:
        ghostPos = ghostState.getPosition()
        scaredTime = ghostState.scaredTimer

        # Penalty for being close to ghost
        if scaredTime == 0 and util.manhattanDistance(newPos, ghostPos) < 2:
          return -float('inf')
        # Reward being close to scared ghost
        if scaredTime > 0 and util.manhattanDistance(newPos, ghostPos) < 2:
           return float('inf')

      foodDistances = [util.manhattanDistance(newPos, food) for food in newFood.asList()]
      if foodDistances:
        score += max(0, 100 - min(foodDistances))

      # Penalty for stopping
      if action == Directions.STOP:
        score -= 5

      return score
          

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one dix`splayed in the Pacman GUI.
      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.
      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.
      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.
          Here are some method calls that might be useful when implementing minimax.
          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1
          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action
          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        def minimax(agentIndex, depth, gameState):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)

            if agentIndex == 0:  # Maximize for Pacman
                return max(minimax(1, depth, gameState.generateSuccessor(agentIndex, action)) 
                           for action in gameState.getLegalActions(agentIndex))
            else:  # Minimize for ghosts
                nextAgent = agentIndex + 1
                if nextAgent == gameState.getNumAgents():
                    nextAgent, depth = 0, depth + 1

                return min(minimax(nextAgent, depth, gameState.generateSuccessor(agentIndex, action)) 
                           for action in gameState.getLegalActions(agentIndex))

        # Start with Pacman (agentIndex 0) at depth 0
        legalActions = gameState.getLegalActions(0)
        return max(legalActions, key=lambda x: minimax(1, 0, gameState.generateSuccessor(0, x)))


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def alphaBeta(agentIndex, depth, gameState, alpha, beta):
            # Check for terminal state
            if gameState.isWin() or gameState.isLose() or depth == self.depth * gameState.getNumAgents():
                return self.evaluationFunction(gameState)

            numAgents = gameState.getNumAgents()
            nextAgent = (agentIndex + 1) % numAgents
            if nextAgent == 0: nextDepth = depth + 1
            else: nextDepth = depth

            # Pacman
            if agentIndex == 0:
                value = -float('inf')
                for action in gameState.getLegalActions(agentIndex):
                    value = max(value, alphaBeta(nextAgent, nextDepth, gameState.generateSuccessor(agentIndex, action), alpha, beta))
                    if value > beta:
                        return value
                    alpha = max(alpha, value)
                return value

            # Ghosts
            else:
                value = float('inf')
                for action in gameState.getLegalActions(agentIndex):
                    value = min(value, alphaBeta(nextAgent, nextDepth, gameState.generateSuccessor(agentIndex, action), alpha, beta))
                    if value < alpha:
                        return value
                    beta = min(beta, value)
                return value

        # Init
        alpha, beta = -float('inf'), float('inf')
        bestAction = Directions.STOP
        bestScore = -float('inf')

        for action in gameState.getLegalActions(0):
            score = alphaBeta(1, 0, gameState.generateSuccessor(0, action), alpha, beta)
            if score > bestScore:
                bestScore = score
                bestAction = action
            alpha = max(alpha, bestScore)

        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
      """
        Your expectimax agent (question 4)
      """

      def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction
          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
          The expectimax function returns a tuple of (actions,
        """
        def expectimax(agentIndex, depth, gameState):
          # Check for terminal state
          if gameState.isWin() or gameState.isLose() or depth == self.depth * gameState.getNumAgents():
            return self.evaluationFunction(gameState)

          numAgents = gameState.getNumAgents()
          nextAgent = (agentIndex + 1) % numAgents
          nextDepth = depth + 1 if nextAgent == 0 else depth

          if agentIndex == 0:
            return max(expectimax(nextAgent, nextDepth, gameState.generateSuccessor(agentIndex, action))
                   for action in gameState.getLegalActions(agentIndex))

          else:
            actions = gameState.getLegalActions(agentIndex)
            if not actions:
              return self.evaluationFunction(gameState)
            total = sum(expectimax(nextAgent, nextDepth, gameState.generateSuccessor(agentIndex, action))
                  for action in actions)
            return float(total) / float(len(actions))

        legalActions = gameState.getLegalActions(0)
        return max(legalActions, key=lambda action: expectimax(0, 0, gameState.generateSuccessor(0, action)))


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).
      DESCRIPTION: <write something here so we know what you did>
      Evaluate state by  :
            * closest food
            * food left
            * capsules left
            * distance to ghost
    """
    "*** YOUR CODE HERE ***"

    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    capsules = currentGameState.getCapsules()

    score = currentGameState.getScore()

    foodDistances = [util.manhattanDistance(newPos, food) for food in newFood.asList()]
    if foodDistances:
        score -= min(foodDistances)

    for ghostState, scaredTime in zip(newGhostStates, newScaredTimes):
        ghostDistance = util.manhattanDistance(newPos, ghostState.getPosition())
        if scaredTime > 0:  # Ghost is scared
            score += max(10 - ghostDistance, 0)
        else:  # Ghost is not scared
            if ghostDistance < 2:
                score -= 100  

    if capsules:
        capsuleDistances = [util.manhattanDistance(newPos, capsule) for capsule in capsules]
        score -= 2 * min(capsuleDistances)

    return score

# Abbreviation
better = betterEvaluationFunction
