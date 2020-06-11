import turtle


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
        #manual
        self.screen.listen()
        self.screen.onkey(self.paddle_right, 'Right')
        self.screen.onkey(self.paddle_left, 'Left')
        #other
        self.reward = 0
        self.end = False

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
        self.end = False
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
        # Ball-Walls collision
        if self.ball.xcor() > 290:    # If ball touch the right wall
            self.ball.setx(290)
            self.ball.dx *= -1        # Reverse the x-axis velocity
        if self.ball.xcor() < -290:   # If ball touch the left wall
            self.ball.setx(-290)
            self.ball.dx *= -1        # Reverse the x-axis velocity
        if self.ball.ycor() > 290:    # If ball touch the upper wall
            self.ball.sety(290)
            self.ball.dy *= -1

    def miss_ball(self):
        # Ball-Ground collison   
        if self.ball.ycor() < -290:
            self.ball.goto(0, 100)
            self.reward -= 3
            self.miss += 1
            self.update_score()
            self.end = True

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



def main():
    paddle_game = Paddle_Game()
    paddle_game.restart()
    while True:
        paddle_game.run_frame()

if __name__ == "__main__":
    main()