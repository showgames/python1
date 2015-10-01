from tkinter import *
import random
import time

#window,canvas
tk = Tk()
tk.title("GAME!!")
tk.resizable(0,0)
tk.wm_attributes("-topmost",1)
canvas = Canvas(tk, bg = 'black', width = 500, height = 400,
                bd = 0, highlightthickness = 0)

#Ball
class Ball:
    def __init__(self, canvas, paddle, score , level, color):
        self.canvas = canvas
        self.paddle = paddle
        self.score = score
        self.levelball = level
        self.id = canvas.create_oval(10,10,25,25,fill=color)
        self.canvas.move(self.id, 245, 100)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False
        self.speed = 3

    def hit_paddle(self,pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                self.x += self.paddle.x
                self.score.hit()
                return True
        return False

    def draw(self):
        self.canvas.move(self.id,self.x,self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = self.speed
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if self.hit_paddle(pos) == True:
            self.y = -self.speed
        if pos[0] <= 0:
            self.x = self.speed
        if pos[2] >= self.canvas_width:
            self.x = -self.speed
        if self.levelball.level == 2:
            self.canvas.itemconfig(self.id, fill = 'blue')
        if self.levelball.level == 3:
            self.canvas.itemconfig(self.id, fill = 'red')
        

#Paddle
class Paddle:
    def __init__(self,canvas,color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0,0,100,10,fill=color)
        self.canvas.move(self.id,200,300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.started = False
        self.game_start_text = self.canvas.create_text(250,200,text = 'Click For Start !',
                                                   font = ('Helvetica', 20),
                                                   fill = 'red', state = 'normal')
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<Button-1>', self.start_game)

    def draw(self):
        self.canvas.move(self.id,self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0

    def turn_left(self, evt):
        self.x = -5

    def turn_right(self,evt):
        self.x = 5

    def start_game(self,evt):
        self.canvas.itemconfig(self.game_start_text, state = 'hidden')
        time.sleep(0.5)
        self.started = True


#Score
class Score:
    def __init__(self,canvas,color):
        self.score = 0
        self.canvas = canvas
        self.id = self.canvas.create_text(400,380, text = ('SCORE : %d' %self.score),
                                          font = ('Helvetica', 20),fill = color)

    def hit(self):
        self.score += 1
        self.canvas.itemconfig(self.id, text=('SCORE : %d' %self.score))



#Level
class Level:
    def __init__(self, canvas,color):
        self.level = 1
        self.canvas = canvas
        self.id = self.canvas.create_text(100,380, text = ('LEVEL : %d' %self.level),
                                          font = ('Helvetica', 20),fill = color)

    def level_up(self, number):
        self.level = number
        self.canvas.itemconfig(self.id, text=('LEVEL : %d' %self.level))


#GameMaster       
class GameMaster:
    def set_game(self):
        canvas.pack()
        tk.update()
        self.game_over_text = canvas.create_text(250, 200,text = 'GAME OVER...',
                                                 font = ('Helvetica', 20),
                                                 fill = 'red',state = 'hidden')
        
    def set_object(self):
        self.levelgame = Level(canvas,'yellow')
        self.score = Score(canvas, 'yellow')
        self.paddle = Paddle(canvas, 'brown')
        self.ball = Ball(canvas, self.paddle, self.score, self.levelgame, 'yellow')

    
    def start_game(self):
        while True:
            if self.ball.hit_bottom == False and self.paddle.started == True:
               self.ball.draw()
               self.paddle.draw()
               if self.score.score >= 10 and self.score.score <= 15:
                   self.num = 2
                   self.levelgame.level_up(self.num)
                   self.ball.speed = 5
               elif self.score.score >= 20:
                   self.num = 3
                   self.levelgame.level_up(self.num)
                   self.ball.speed = 7
            if self.ball.hit_bottom == True:
               time.sleep(1)
               #canvas.itemconfig(self.game_over_text, state = 'normal')
               break
            tk.update_idletasks()
            tk.update()
            time.sleep(0.01)
        canvas.itemconfig(self.levelgame.id, state = 'hidden')
        #canvas.itemconfig(self.game_over_text, state = 'hidden')
        canvas.itemconfig(self.score.id, state = 'hidden')
        canvas.itemconfig(self.ball.id, state = 'hidden')
        canvas.itemconfig(self.paddle.id, state = 'hidden')
 


#START_GAME
game_master = GameMaster()
while True:
    game_master.set_game()
    game_master.set_object()
    game_master.start_game()






