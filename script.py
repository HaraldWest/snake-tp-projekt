import time
from colorama import Fore, Back, Style, init
from tkinter import *
import random

GAME_WIDTH = 500
GAME_HEIGHT = 500
SPEED = 120         #spelhastighet
SPACE_SIZE = 50     #storlek på varje rutmönster
BODY_PARTS = 3      #ormens "start" storlek
SNAKE_COLOR = "#00FF00"     #ormens färg
FOOD_COLOR = "#FF0000"      #matens färg
BACKGROUND_COLOR = "#000000"        #bakgrundsfärg för fönstret
BOARD_COLORS = ["#000000", "#08149c"]       #färger för rutnätet

restart_button = None       #knappen för att starta om spelet

#klassen för ormen
class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []       #koordinaterna för ormens kroppsdelar
        self.squares = []           #dem grafiska rutorna för ormens kroppsdelart

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])     #initiala koordinater för ormens kroppsdelar

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)     #skapar ormens kroppsdelar i fönstret


#klassen för maten
class Food:

    def __init__(self):

        x = random.randint(0, int((GAME_WIDTH / SPACE_SIZE)-1)) * SPACE_SIZE
        y = random.randint(0, int((GAME_HEIGHT / SPACE_SIZE) - 1)) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

#funktion för nästa drag i spelet
def next_turn(snake, food):

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))     #lägger till nya koordinater för huvuvdet på ormen

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)        #ritar ormen i fönstrer

    snake.squares.insert(0, square)     #lägg till ormens huvud i grafiken

    if x == food.coordinates[0] and y == food.coordinates[1]:       #om ormen äter maten

        global score

        score += 1      #om ormen äter maten ökas scoren med 1

        label.config(text="Score:{}".format(score))     #uppdatera poängtexten

        canvas.delete("food")       #ta bort maten från fönstret

        food = Food()          #skapa ny mat

    else:

        del snake.coordinates[-1]       #ta bort den sista kroppsdelens koordinater

        canvas.delete(snake.squares[-1])        #ta bort den sista kroppsdelens grafiska representation

        del snake.squares[-1]       #ta bort den sista kroppsdelens grafiska representation

    if check_collisions(snake):     
        game_over()     #om ormen kolliderar med sig själv eller en kant så är spelet över

    else:
        window.after(SPEED, next_turn, snake, food)     #annars fortsätter spelet med nästa drag


#funktion för att ändra riktning för ormen
def change_direction(new_direction):

    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


#funktion för att kontrollera kollisioner
def check_collisions(snake):

    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


#funktion för att hantera spelets slut
def game_over():
    global restart_button
    canvas.delete(ALL)      #tar bort allt från fönstret
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/3,
                       font=('consolas',70), text="GAME OVER", fill="red", tag="gameover")      #visar "Game Over" texten
    if score < 10:                                                                  
        canvas.create_text(canvas.winfo_width()/2 , canvas.winfo_height()/3 * 2,
                       font=('consolas',20), text="You f*cking suck at the game!", fill="yellow", tag="gameover")       #visar ett meddelande om spelarens presentation
        
    
    if game_over:
        restart_button = Button(window, text="Restart", font=('consolas', 20), command=restart_game)        #visar en knapp för att starta om spelet
        restart_button.place(x=canvas.winfo_width()/3, y=canvas.winfo_height()/3 + 150)


    
#funtion för att skapa rutnätet
def CreateSquareCanvas():
    for i in range(0, GAME_WIDTH, SPACE_SIZE):
        for j in range(0, GAME_HEIGHT, SPACE_SIZE):
            color = BOARD_COLORS[(i // SPACE_SIZE + j // SPACE_SIZE) % 2]
            canvas.create_rectangle(i, j, i + SPACE_SIZE, j + SPACE_SIZE, fill=color)


#funktionen för att starta om spelet
def restart_game():
    global score, direction
    score = 0               #återställer poängen
    direction = 'down'      #återställer riktningen på ormen
    label.config(text="Score:{}".format(score))     #uppdaterar poängtexten
    canvas.delete(ALL)      #tar bort allt från fönstret
    CreateSquareCanvas()    #skapar rutnätet igen
    snake = Snake()         #skapar en ny orm
    food = Food()           #skapar ny mat
    next_turn(snake, food)  #startar spelet igen
    print("should destroy")


    if restart_button != None:
        print("destroying..")
        restart_button.destroy()


#skapa huvudfönstret
window = Tk()
window.title("Snake game")
window.resizable(False, False)      #gör fönsret oföränderligt

score = 0       #variabeln som håller ordning på poängen
direction = 'down'      #rikting för ormen

label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()


#huvudfunktionen för spelet
def main():
    label.config(text="Score:{}".format(score))     #uppdaterar poängtexten
    window_width = window.winfo_width()             #fönstrets bredd
    window_height = window.winfo_height()           #fönsrets höjd
    screen_width = window.winfo_screenwidth()       #skärmens bredd
    screen_height = window.winfo_screenheight()     #skärmens höjd

    x = int((screen_width/2) - (window_width/2))
    y = int((screen_height/2) - (window_height/2))

    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    window.bind('<Left>', lambda event: change_direction('left'))       #bindning för vänsterpil
    window.bind('<Right>', lambda event: change_direction('right'))     #bindning för högerpil
    window.bind('<Up>', lambda event: change_direction('up'))           #bindning för uppåtpil
    window.bind('<Down>', lambda event: change_direction('down'))       #bindning för nedåtpil

    snake = Snake()     #skapa en orm
    food = Food()       #skapa maten

    next_turn(snake, food)  #skapa spelet

    window.mainloop()       #starta huvudloopen för fönsret

countdown_time = 3      #tid för nedräkning innan spelet startar

#funktionen för nedräkningen
def countdown(seconds):
    canvas.delete(ALL)
    while seconds > 0:
        canvas.delete(ALL)
        canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas',70), text=f"{seconds}", fill="red", tag="countdown")
        window.update()
        print (Back.BLACK + Fore.WHITE + f"{seconds} Seconds Remaining", end="\r")
        time.sleep(1)
        seconds -= 1        #minskar nedräkningsitden
    CreateSquareCanvas()
    main()                  #starta huvudfunktionen för spelet
window.update()
countdown(countdown_time)       #starta nedräkningen