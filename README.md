# Atari Paddle Reinforcement Learning

## Project :
The aim of this project is to create an artificial intelligence (AI) that will be able to learn and succeed in a game, the paddle.
The AI is created with a reinforcement learning algorithm.
The development has been made is two different steps :
- the paddle game
- the AI

## Some explanation about the Reinforcement Learning
This is a branch of Machine-Learning where an agent and an environment take place.
An environment is a simulation, a task. An agent is an intelligent algorithm that interacts in the environment to solve a problem (win a game for example).
At each time, the agent make an action in the environment, which give him back a state (a new position for example) and rewards the agent (depending on the action made).
The goal of the agent is to obtain the highest reward. It does it with two possible actions in the environment : explore or exploit. In the first case, it randomly chooses an action. In the second case, it uses past experiences to conclude on the best action to do.

## Development
### Paddle Game Coding
The Python library Turtle has been used to create this paddle game. It permits to easily create different objects and get their positions over time.
The created objects are :
- the paddle : it can only move along the horizontal axis. The user can interact with the game with the keyboard
- the ball : it can move in all the direction. It can collide with the walls or the paddle but it will change direction
- the score card : it display the number of hit (paddle-ball collision) and miss

The game follow the plan :
1. initialisation : the paddle and the ball are positioned to their init location
2. while the game is not over :
   1. the player choose an action : moving right, left or not moving at the paddle. Reward is updated
   2. the screen is updated with the move
   3. the ball is moved depending on its previous position and its velocity
   4. if the ball hits the wall, its velocity is changed on the correct axis
   5. if the ball hit the paddle, its velocity is changed on the correct axis and reward and score card are updated
   6. if the paddle miss the ball, the game is over and reward and score card are updated

### Reinforcement Learning algorithm implementation
As explained above, the agent receives space informations and should conclude on the next move. In other words, given a state, it will conclude on an action.
#### State
The state is a space information about elements in the game. In the paddle game, it means :
- the position of the paddle (along the x-axis)
- the position of the ball (along the x and y-axis)
- the velocity of the ball (along the x and y-axis)
Those informations are used by the agent to take a decision.
#### Reward
Rewards give the agent an idea about a good or a bad action. It seems logic that the agent should want to receive the best reward. In the paddle game, it means :
- if the paddle hit the ball, the reward is +3
- if the paddle miss the ball, the reward is -3
- if the paddle moves, the reward is -0.1.
The last reward has been designed to obtain the smoothest and accurate movement of the paddle.
#### Q-matrix
In order to let the agent select the best choice depeding on its situation, the idea is to attribute a score for each action before each move decision. This is the Q-matrix.
The matrix is filled after each action and game progress. The model (described below) is used to compute the score of each action for each next state. 
The previous actions are also saved, with the rewards. With these data, the value of the q-matrix corresponding to the action really played is updated with the following formula : `q_value = reward + gamma * max_row` with max_row = the maximum value of the given score, the maximum value of the model prediciton of the next state.
From that formula, it is important to understand that if `gamma` equal 0, the new q_value highlights the current action played. With a high `gamma`, the next action played will have more importance.
#### Model
The model designed is a Neural Network. It is fully connected neural network, with the following architecture :
- Dense layer (64), relu activation
- Dense layer (64), relu activation
- Dense layer (3), linear activation
Mean Square Error is used to compute loss and Adam optimizer is used.
### Algorithm
The full agorithm, with the AI, is :
- initialisation of the elements
- until a maximum of steps :
  1. explore or exploit : a random is picked. If it is lower than a threshold `epsilon`, a random action is selected (left, right or nothing). Otherwise, the model predict the action to do
  2. action is done and game plan is followed (as explained above)
  3. total reward is computed to let the user know if the agent performs nicely or not
  4. game results are saved : state, action, reward, next state, done (if the game is over or not)
  5. model is trained with data from the beginning of the game, with a limit batch size, using Q-matrix


## Run the program :

The program can be launched with the following command : `python paddle_game.py`.

It is also possible to run the game on its own, to let the user play with the keyboard. The command is : `python paddle_game_manual.py`.

Libraries are detailled in the file `requirements.txt`.
