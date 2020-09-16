from tkinter import *
import random
from time import sleep

class Segment:
    """ Single snake segment """
    def __init__(self, x, y):
        self.inst = c.create_rectangle(x, y, x+SIZE, y+SIZE, fill="white")

class Snake:
    """ Simple Snake class """
    def __init__(self, segments):
        self.segments = segments
        # possible moves
        self.mapping = {"Down": (0, 1), "Right": (1, 0),
                        "Up": (0, -1), "Left": (-1, 0)}
        # initial movement direction
        self.vector = self.mapping["Right"]

    def move(self):
        """ Moves the snake with the specified vector"""
        for index in range(len(self.segments)-1):
            segment = self.segments[index].inst
            x1, y1, x2, y2 = c.coords(self.segments[index+1].inst)
            c.coords(segment, x1, y1, x2, y2)

        x1, y1, x2, y2 = c.coords(self.segments[-2].inst)
        c.coords(self.segments[-1].inst,
                 x1+self.vector[0]*SIZE, y1+self.vector[1]*SIZE,
                 x2+self.vector[0]*SIZE, y2+self.vector[1]*SIZE)
    
    def handler_direction(self, d):
        x1, y1, x2, y2 = c.coords(self.segments[-1].inst)
        if d == 'x>':
            c.coords(self.segments[-1].inst, 0, y1, SIZE, y2)
        elif d == 'x<':
            c.coords(self.segments[-1].inst, WIDTH - SIZE, y1, WIDTH, y2)
        elif d == 'y>':
            c.coords(self.segments[-1].inst, x1, 0, x2, SIZE)
        else:
            c.coords(self.segments[-1].inst, x1, HEIGHT - SIZE, x2, HEIGHT)

    def add_segment(self):
        """ Adds segment to the snake """
        last_seg = c.coords(self.segments[0].inst)
        x = last_seg[0]
        y = last_seg[1]
        self.segments.insert(0, Segment(x, y))

    def change_direction(self, event):
        """ Changes direction of snake """
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]

    def reset_snake(self):
        for segment in self.segments:
            c.delete(segment.inst)


def set_state(item, state):
    c.itemconfigure(item, state=state)


def clicked(event):
    global boolean
    boolean = True
    c.itemconfigure(restart_text, state='hidden')
    c.itemconfigure(game_over_text, state='hidden')
    buttons()


def start_game():
    global s
    create_block()
    s = create_snake()
    # Reaction on keypress
    c.bind("<KeyPress>", s.change_direction)
    main()


def create_snake():
    # creating segments and snake
    segments = [Segment(SIZE, SIZE),
                Segment(SIZE*2, SIZE),
                Segment(SIZE*3, SIZE)]
    return Snake(segments)

def create_block():
    """ Creates an apple to be eaten """
    global BLOCK
    posx = SIZE * random.randint(1, (WIDTH-SIZE) / SIZE)
    posy = SIZE * random.randint(1, (HEIGHT-SIZE) / SIZE)
    BLOCK = c.create_oval(posx, posy, posx+SIZE, posy+SIZE, fill="red")

def easy_mode(k):
    global speed
    speed = 100
    set_state(choose_text, 'hidden')
    remove_buttons()
    start_game()

def medium_mode(k):
    global speed
    speed = 50
    set_state(choose_text, 'hidden')
    remove_buttons()
    start_game()

def hard_mode(k):
    global speed
    speed = 30
    set_state(choose_text, 'hidden')
    remove_buttons()
    start_game()

def buttons():
    global button1, button2, button3
    set_state(choose_text, 'normal')
    button1 = Button(root, text = 'easy', font = 'Arial 25 bold', width = '7', height = '1', bg = '#696969', fg = '#E0FFFF')
    button2 = Button(root, text = 'medium', font = 'Arial 25 bold', width = '7', height = '1', bg = '#696969', fg = '#E0FFFF')
    button3 = Button(root, text = 'hard', font = 'Arial 25 bold', width = '7', height = '1', bg = '#696969', fg = '#E0FFFF')
    button1.bind('<Button-1>', easy_mode)
    button2.bind('<Button-1>', medium_mode)
    button3.bind('<Button-1>', hard_mode)
    button1.place(x = WIDTH//4-50, y = HEIGHT//2, width = 140, height = 50)
    button2.place(x = WIDTH//2-50, y = HEIGHT//2, width = 140, height = 50)
    button3.place(x = WIDTH//4*3-50, y = HEIGHT//2, width = 140, height = 50)
    #button1.grid(row = 0, column = 0)
    #button2.grid(row = 0, column = 2)
    #button3.grid(row = 0, column = 4)

def remove_buttons():
    button_list = [button1, button2, button3]
    for name in button_list:
        name.destroy()

def animation_text(a, i):
    c.coords(a, 100 - i, 200)

def main():
    """ Handles game process """
    global boolean
    if boolean:
        s.move()
        head_coords = c.coords(s.segments[-1].inst)
        x1, y1, x2, y2 = head_coords
        # Check for collision with gamefield edges
        if x2 > WIDTH or x1 < 0 or y1 < 0 or y2 > HEIGHT:
            if x2 > WIDTH: d = 'x>'
            elif x1 < 0: d = 'x<'
            elif y2 > HEIGHT: d = 'y>'
            else: d = 'y<'
            s.handler_direction(d)
        # Eating apples
        elif head_coords == c.coords(BLOCK):
            s.add_segment()
            c.delete(BLOCK)
            create_block()
        # Self-eating
        else:
            for index in range(len(s.segments)-1):
                if head_coords == c.coords(s.segments[index].inst):
                    boolean = False
        root.after(speed, main)
    # Not boolean -> stop game and print message
    else:
        s.reset_snake()
        c.delete(BLOCK)
        set_state(restart_text, 'normal')
        set_state(game_over_text, 'normal')
        '''for i in range(10):   
            c.create_text(100 + i, 200, text = '-', font = "Arial 20", state = 'normal', fill = 'blue')
            sleep(0.1)'''

# Globals
WIDTH = 800
HEIGHT = 600
SIZE = 20
boolean = True
i = 0

# Setting up window
root = Tk()
root.title("SnakeGame")

c = Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
c.grid()
# catch keypressing
c.focus_set()
game_over_text = c.create_text(WIDTH/2, HEIGHT/3, text="Good Game", font='Arial 50', fill='yellow', state='hidden')
restart_text = c.create_text(WIDTH/2, HEIGHT-HEIGHT/2, text="ПЕРЕЗАПУСК", font='Arial 30', fill='white', state='hidden')
choose_text = c.create_text(WIDTH/2, HEIGHT/3, text = 'Выбор сложности', font = 'Arial 40', fill = '#F0E68C', state = 'hidden')
c.tag_bind(restart_text, "<Button-1>", clicked)
buttons()
root.mainloop()

