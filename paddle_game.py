import turtle
import numpy as np
import pandas as pd
import random

from keras import Sequential
from keras.layers import Dense
from keras.optimizers import adam


class Paddle_Game():
    def __init__(self):
        #screen
        self.screen = turtle.Screen()
        self.screen.title('Paddle')
        self.screen.bgcolor('black')
        self.screen.tracer(0)
        self.screen.setup(width=600, height=600)
        #ball
        self.ball = turtle.Turtle()
        self.ball.speed(0)
        self.ball.shape('circle')
        self.ball.color('red')
        self.ball.penup()
        self.ball.goto(0,100)
        self.ball.dx = -3
        self.ball.dy = -3
        #paddle
        self.paddle = turtle.Turtle()
        self.paddle.shape('square')
        self.paddle.speed(0)             
        self.paddle.shapesize(stretch_wid=1, stretch_len=5)
        self.paddle.penup()
        self.paddle.color('white')
        self.paddle.goto(0, -275)
        #score
        self.score = turtle.Turtle()
        self.score.speed(0)
        self.score.color('white')
        self.score.hideturtle()
        self.score.penup()
        self.score.goto(0, 250)
        self.hit = 0
        self.miss = 0
        self.score.write("Hit: {}   Missed: {}".format(self.hit, self.miss), align='center', font=('Courier', 24, 'normal'))
        #other
        self.reward = 0
        self.end = 0

    def paddle_right(self):
        x = self.paddle.xcor()
        if x < 225:
            self.paddle.setx(x+20)
    def paddle_left(self):
        x = self.paddle.xcor()
        if x > -225:
            self.paddle.setx(x-20)

    def restart(self):
        self.paddle.goto(0, -275)
        self.ball.goto(0,100)
        return self.get_state()

    def do_action(self, action):
        self.reward = 0
        self.end = 0
        if action == 0:
            self.paddle_left()
            self.reward -= 0.1
        if action == 1:
            self.reward += 0
        if action == 2:
            self.paddle_right()
            self.reward -= 0.1
        reward,state,end = self.run_frame()
        return reward,state,end

    def wall_collision(self):
        if self.ball.xcor() > 290:    # Right wall
            self.ball.setx(290)
            self.ball.dx *= -1
        if self.ball.xcor() < -290:   # Left wall
            self.ball.setx(-290)
            self.ball.dx *= -1
        if self.ball.ycor() > 290:    # Upper wall
            self.ball.sety(290)
            self.ball.dy *= -1

    def miss_ball(self):
        # Ball-Ground collison   
        if self.ball.ycor() < -290:
            self.ball.goto(0, 100)
            self.reward -= 3
            self.miss += 1
            self.update_score()
            self.end = 1

    def touched(self):
        # Ball-Paddle collision
        if abs(self.ball.ycor() + 250) < 2 and abs(self.paddle.xcor() - self.ball.xcor()) < 55:
            self.ball.dy *= -1
            self.hit += 1
            self.update_score()
            self.reward += 3

    def move_ball(self):
        self.ball.setx(self.ball.xcor() + self.ball.dx)
        self.ball.sety(self.ball.ycor() + self.ball.dy)

    def update_score(self):
        self.score.clear()
        self.score.write("Hit: {}   Missed: {}".format(self.hit, self.miss), align='center', font=('Courier', 24, 'normal'))

    def run_frame(self):
        self.screen.update()
        self.move_ball()
        self.wall_collision()
        self.touched()
        self.miss_ball()
        return self.reward,self.get_state(),self.end
    
    def get_state(self):
        return [self.paddle.xcor()*0.01, self.ball.xcor()*0.01, self.ball.ycor()*0.01, self.ball.dx, self.ball.dy]


def create_model():
    model = Sequential()
    model.add(Dense(64, activation="relu",input_shape=(5,)))
    model.add(Dense(64, activation="relu"))
    model.add(Dense(3, activation="linear"))
    model.compile(loss='mse', optimizer=adam(lr=0.01))
    return model


def train_model(model,data):
    #prepare data : fill NA
    data.fillna(0, inplace=True)

    if data.shape[0] > batch_size:
        #random rows and limit batch size otherwise too slow : experience replay
        data = data.sample(batch_size)

        #construct q-matrix -- q_value
        df_qvalues = model.predict(data[["next_statepx","next_statebx","next_stateby","next_statebdx","next_statebdy"]])
        q_value = (data["reward"] + gamma * (1-data["done"]) * np.amax(df_qvalues, axis=1)).tolist()

        #update q-value matrix : value on which action has been made
        action_list = data["action"].to_list()
        for i in range(len(action_list)):
            df_qvalues[i,int(action_list[i])] = q_value[i]

        Y = df_qvalues
        cols = ["statepx","statebx","stateby","statebdx","statebdy"]
        X = data[cols].to_numpy()
        model.fit(X,Y,epochs=1,verbose=0)
    return model


def main():
    paddle_game = Paddle_Game()

    model = create_model()

    df_event = pd.DataFrame(columns=["statepx","statebx","stateby","statebdx","statebdy","action","reward","next_statepx","next_statebx","next_stateby","next_statebdx","next_statebdy","done"])
    df_event['reward'] = df_event['reward'].astype(int)
    for g in range(game_part):
        state = paddle_game.restart()
        tot_reward = 0
        for action in range(max_actions):
            if random.uniform(0, 1) < epsilon:
                #random action
                action = random.randrange(3)
            else:
                action = np.argmax(model.predict(pd.DataFrame(np.reshape(state,[1,5]))))
            reward,next_state,done = paddle_game.do_action(action)
            tot_reward += reward
            new_row = state+[action]+[reward]+next_state+[done]
            df_event = df_event.append(new_row)
            state = next_state
            model = train_model(model,df_event)
            if done:
                break
        print("Game {} : Score {}".format(g,tot_reward))

epsilon = 0.2
game_part = 20
max_actions = 1000
batch_size = 64
gamma = 0.8

if __name__ == "__main__":
    main()