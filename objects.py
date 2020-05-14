import turtle

class Ball():
    def __init__(self):
        self.turtleball = turtle.Turtle()      # Create a turtle object
        self.turtleball.speed(0)
        self.turtleball.shape('circle')        # Select a circle shape
        self.turtleball.color('red')           # Set the color to red
        self.turtleball.penup()
        self.x = 0
        self.y = 100
        self.turtleball.goto(self.x, self.y)
        self.turtleball.dx = 3   # ball's x-axis velocity
        self.turtleball.dy = -3  # ball's y-axis velocity
    def update_walls(self):
        # Ball-Walls collision
        if self.turtleball.xcor() > 290:    # If ball touch the right wall
            self.turtleball.setx(290)
            self.turtleball.dx *= -1        # Reverse the x-axis velocity
        if self.turtleball.xcor() < -290:   # If ball touch the left wall
            self.turtleball.setx(-290)
            self.turtleball.dx *= -1        # Reverse the x-axis velocity
        if self.turtleball.ycor() > 290:    # If ball touch the upper wall
            self.turtleball.sety(290)
            self.turtleball.dy *= -1        # Reverse the y-axis velocity
    def update_ground(self):
        # Ball-Ground collison   
        if self.turtleball.ycor() < -290:   # If ball touch the ground
            self.turtleball.goto(0, 100)    # Reset the ball position
            return True
        else:
            return False
    def get_position(self):
        return self.turtleball.xcor(),self.turtleball.ycor()
    def get_velocity(self):
        return self.turtleball.dx,self.turtleball.dy
    def reverse_speed(self,axis):
        if axis == "x":
            self.turtleball.dx *= -1
        if axis == "y":
            self.turtleball.dy *= -1
    def update_position(self):
        self.turtleball.setx(self.turtleball.xcor() + self.turtleball.dx)  # update the ball's x-location using velocity
        self.turtleball.sety(self.turtleball.ycor() + self.turtleball.dy)  # update the ball's y-location using velocity

class Paddle():
    def __init__(self):
        self.turtlepaddle = turtle.Turtle()    # Create a turtle object
        self.turtlepaddle.shape('square')      # Select a square shape
        self.turtlepaddle.speed(0)             
        self.turtlepaddle.shapesize(stretch_wid=1, stretch_len=5)   # Streach the length of square by 5 
        self.turtlepaddle.penup()
        self.turtlepaddle.color('white')       # Set the color to white
        self.turtlepaddle.goto(0, -275)        # Place the shape on bottom of the screen
    # Paddle Movement
    def paddle_right(self):
        x = self.turtlepaddle.xcor()        # Get the x position of paddle
        if x < 225:
            self.turtlepaddle.setx(x+20)    # increment the x position by 20
    def paddle_left(self):
        x = self.turtlepaddle.xcor()        # Get the x position of paddle
        if x > -225:
            self.turtlepaddle.setx(x-20)    # decrement the x position by 20
    def get_position(self):
        return self.turtlepaddle.xcor()

class Scorecard():
    def __init__(self):
        self.turtlescore = turtle.Turtle()   # Create a turtle object
        self.turtlescore.speed(0)
        self.turtlescore.color('white')      # Set the color to white
        self.turtlescore.hideturtle()        # Hide the shape of the object
        self.turtlescore.penup()
        self.turtlescore.goto(0, 250)        # Set scorecard to upper middle of the screen
        self.hit = 0
        self.miss = 0
    def update_score(self,hit,miss):
        self.hit += hit
        self.miss += miss
    def display_score(self):
        self.turtlescore.clear()
        self.turtlescore.write("Hit: {}   Missed: {}".format(self.hit, self.miss), align='center', font=('Courier', 24, 'normal'))

class Window():
    def __init__(self,paddle,ball,scorecard):
        # Screen
        self.screen = turtle.Screen()    # Create a screen
        self.screen.title('Paddle')      # Set the title to paddle
        self.screen.bgcolor('black')     # Set the color to black
        self.screen.tracer(0)
        self.screen.setup(width=600, height=600)   # Set the width and height to 600
        # Paddle
        self.turtlepaddle = paddle
        #ball
        self.turtleball = ball
        # Scorecard
        self.score = scorecard
        # Reward
        self.reward = 0.0
        # Number of tries
        self.done = 0
    def listen_screen(self):
        self.screen.listen()
    def onkey(self,key):
        if key == "Right":
            self.screen.onkey(self.turtlepaddle.paddle_right, 'Right')
        if key == "Left":
            self.screen.onkey(self.turtlepaddle.paddle_left, 'Left')
    def detect_collision(self):
        # Ball-Paddle collision
        ball_pos = self.turtleball.get_position()
        paddle_pos = self.turtlepaddle.get_position()
        if abs(ball_pos[1] + 250) < 2 and abs(paddle_pos - ball_pos[0]) < 55:
            self.turtleball.reverse_speed("y")
            self.reward += 3
            self.score.update_score(1,0)
    def update_screen(self):
        self.screen.update()
    def update_ball(self):
        self.turtleball.update_walls()
        has_reset = self.turtleball.update_ground()
        if has_reset:
            self.score.update_score(0,1)
            self.update_reward(-3)
            self.done += 1
        self.detect_collision()
        self.turtleball.update_position()
        self.score.display_score()
        return self.done
    def get_reward(self):
        return self.reward
    def update_reward(self,value):
        self.reward += value