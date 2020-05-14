import turtle
from objects import Ball,Paddle,Scorecard,Window

class Game():
    def __init__(self):
        # Create objects
        self.paddle = Paddle()
        self.ball = Ball()
        self.scorecard = Scorecard()
        self.win = Window(self.paddle,self.ball,self.scorecard)
    def manual_run(self):
        # Keyboard Control
        self.win.listen_screen()
        self.win.onkey('Right')   # call paddle_right on right arrow key
        self.win.onkey('Left')
    def step(self,action):
        if action == 0:
            self.paddle.paddle_left()
            self.win.update_reward(-0.1)
        if action == 2:
            self.paddle.paddle_right()
            self.win.update_reward(-0.1)
        reward,state,done = self.run_frame()
        return reward,state,done
    def run_frame(self):
        self.win.update_screen()
        done = self.win.update_ball()
        reward = self.win.get_reward()
        state = [self.paddle.get_position(),self.ball.get_position(),self.ball.get_velocity()]
        return reward,state,done


manual = False

def main():
    game = Game()
    if manual:
        game.manual_run()
    info = game.run_frame()
    while True:
        print(info)
        if manual:
            info = game.run_frame()
        else:
            info = game.step(2)

if __name__ == "__main__":
    main()