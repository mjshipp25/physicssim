import pygame
import sys
from tkinter import *
from tkinter.ttk import *
import os


'''
Variables
'''
# Initialize the pygame
pygame.init()
screen_width = 800 
screen_height = 600

gloc = []
tx = 64
ty = 64

root = Tk()
root.title('Physics Simulator')
root.iconbitmap('d:/projects/physicssim/images/physicssim.ico')
root.geometry("400x400")

variables = {}
calculation= ""


'''
Objects
'''
class Level:
    def ground(lvl, gloc, tx, ty):
        ground_list = pygame.sprite.Group()
        i = 0
        if lvl == 1:
            while i < len(gloc):
                ground = Platform(gloc[i], screen_height - ty, tx, ty, "platform.png")
                ground_list.add(ground)
                i += 1

        return ground_list


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.images = []

        img = pygame.image.load(os.path.join("images/player.png")).convert()
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()


    def update(self):
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey


    def gravity(self):
        global ty
        self.movey += int(variables["Acceleration"])
        if self.rect.y > screen_height and self.movey >= 0:
            self.movey = 0
            self.rect.y = screen_height-ty-ty


class Platform(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc, imgw, imgh, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("images", img)).convert()
        self.rect = self.image.get_rect()
        self.rect.y = yloc
        self.rect.x = xloc


'''
Functions
'''
def main():    
    Label(root, text="Main Menu").pack()

    #Add list of items
    mainMenuOptions = ["Force Calculation", "Velocity Calculation", "Angle Calculation", "Projectile Motion"]
    main_menu = makeListBox(mainMenuOptions, root)
    main_menu.pack(pady=15)

    #Add select button
    select_button = Button(root, text = "Select", command = lambda: openSettings(main_menu.get(ANCHOR)))
    select_button.pack(pady=10)

    simulate_button = Button(root, text="Simulate", command = lambda: simulate())
    simulate_button.pack()

    root.mainloop()


def addValue(LB, name, list, value):
    list[name] = value
    entry = name + ": " + list[name]
    LB.delete(ANCHOR)
    LB.insert(ANCHOR, entry)


def entryBox(LB, level, name, list):
    canvas1 = Canvas(level, width = 200, height = 50)
    canvas1.pack(side="top")

    entry1 = Entry(level)
    canvas1.create_window(100, 25, window=entry1, tags="entry_box")

    if (name == "Acceleration"):
        units = [
            "m/s^2", 
            "km/hr^2", 
            "miles/hr^2"
        ]

    if (name == "Mass"):
        units = [
            "kg", 
            "g", 
            "lbs"
        ]

    variable = StringVar(level)
    variable.set(units[0]) # Default Value

    drop_down = OptionMenu(level, variable, units[0], *units)
    drop_down.pack()

    submit = Button(level, text="Submit", command= lambda: [addValue(LB, name, list, entry1.get()), canvas1.pack_forget(), 
                                                            submit.pack_forget(), drop_down.pack_forget()]) 
    canvas1.create_window(100, 25, window=submit)
    submit.pack(pady=1)   


def forceCalculation(level):
    force = int(variables["Mass"]) * int(variables["Acceleration"])
    
    canvas1 = Canvas(level, width=100, height=25)
    canvas1.pack()

    label1 = Label(level, text = "Force = " + str(force) + " Newtons")
    canvas1.create_window(50, 12.5, window=label1)


def makeListBox(list, level):
    #Make Listbox
    my_listbox = Listbox(level)

    #Add options
    for item in list:
        my_listbox.insert(END, item)

    return my_listbox


def openSettings(function):
    global root
    settings = Toplevel(root)

    settings.title("Settings")
    settings.geometry("400x400")

    Label(settings, text = "Settings").pack()

    global calculation
    if (function == "Force Calculation"):
        global variables
        variables["Mass"] = ""
        variables["Acceleration"] = ""
        calculation = "Force"
    
    settings_LB = makeListBox(variables.keys(), settings)
    settings_LB.pack(fill = X)

    select_button = Button(settings, text="Select", command = lambda: entryBox(settings_LB, settings, settings_LB.get(ANCHOR), variables))
    select_button.pack(pady=10)

    calculate_button = Button(settings, text="Calculate", command = lambda: forceCalculation(settings))
    calculate_button.pack(pady=10)


def simulate():
    # Create the Screen
    global screen_width, screen_height
    screen = pygame.display.set_mode((screen_width, screen_height))
    screen.fill((255, 255, 255))
    pygame.display.flip()
    pygame.display.set_caption('Simulation')

    simulator_icon = pygame.image.load("images/physicssim-1.png")
    pygame.display.set_icon(simulator_icon)

    ''' 
    Setup
    '''
    fps = 60
    clock = pygame.time.Clock()

    box_width = 60
    box_heigth = 60

    player = Player()
    player.rect.x = screen_width/2 - box_width/2
    player.rect.y = 0
    player_list = pygame.sprite.Group()
    player_list.add(player)

    i = 0
    while i <= (screen_width/tx)+tx:
        gloc.append(i*tx)
        i+=1

    ground_list = Level.ground(1, gloc, tx, ty)

    '''
    Main Loop
    '''
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                try:
                    sys.exit()
                finally:
                    running = False

        player.gravity()
        player.update()

        player_list.draw(screen)
        ground_list.draw(screen)
        pygame.display.flip()
        clock.tick(fps)

        
if __name__ == '__main__':
    main()