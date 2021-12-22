import pygame
import sys
from tkinter import *
from tkinter.ttk import *
import os


'''
Variables
'''
# Initialize pygame
pygame.init()
screen_width = 900
screen_height = 900

gloc = []
tx = 64
ty = 64

root = Tk()
root.title('Physics Simulator')
root.iconbitmap('d:/projects/physicssim/images/physicssim.ico')
root.geometry("400x400")

variables = {}
calculation = ""
simulation = ""


'''
Objects
'''
class Level:
    # Setup ground
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
    # Setup player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.velx = 0
        self.vely = 0
        self.images = []

        img = pygame.image.load(os.path.join("images/player.png")).convert()
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()


    # Add gravity
    def gravity(self):
        global ty
        self.vely += float(variables["Acceleration"])

    # Add friction
    def friction(self):
        global ty
        self.velx += float(variables["Applied Force"]) / float(variables["Mass"])
        if self.velx > 0:
            self.velx += -1 * (float(variables["Coefficent of Friction"]) * float(variables["Gravity"]))

    # Update player pos
    def update(self):
        self.rect.x += self.velx
        self.rect.y += self.vely

        # Check screen bounds
        if self.rect.bottom > screen_height-ty:
            self.vely = 0
            self.rect.bottom = screen_height-ty
        
        if self.rect.top < 0:
            self.vely = 0
            self.rect.top = 0

        if self.rect.right > screen_width:
            self.velx = 0
            self.rect.right = screen_width
        
        if self.rect.left < 0:
            self.velx = 0
            self.rect.left = 0


class Platform(pygame.sprite.Sprite):
    # Setup platforms
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
    global root
    global simulation

    Label(root, text="Main Menu").pack()

    #Add list of items
    mainMenuOptions = [
        "Velocity Calculation",
        "Acceleration Calculation",
        "Force Calculation",
        "Work Calculation",
        "Gravity Simulation",
        "Friction Simulation"
        ]
    main_menu = makeListBox(mainMenuOptions, root)
    main_menu.pack(pady=15)

    #Add scrollbar
    scrollbar = Scrollbar(root)
    scrollbar.pack(side = RIGHT, fill = BOTH)
    main_menu.config(yscrollcommand = scrollbar.set)
    scrollbar.config(command = main_menu.yview)

    #Add select button
    select_button = Button(root, text = "Select", command = lambda: [variables.clear(), openSettings(main_menu.get(ANCHOR))])
    select_button.pack(pady=10)

    #Add simulate button
    simulate_button = Button(root, text="Simulate", command = lambda: eval(simulation + "()"))
    simulate_button.pack()

    root.mainloop()


def addValue(LB, name, list, value):
    # Add values to the listbox
    list[name] = value
    entry = name + ": " + list[name]

    LB.delete(ANCHOR)
    LB.insert(ANCHOR, entry)


def entryBox(LB, level, name, list):
    # Add an entrybox to a window
    canvas1 = Canvas(level, width = 200, height = 50)
    canvas1.pack(side="top")

    entry1 = Entry(level)
    canvas1.create_window(100, 25, window=entry1, tags="entry_box")


    # Add dropdown for units
    if name == "Acceleration" or name == "Gravity":
        units = [
            "m/s/s", 
            "km/hr/hr", 
            "miles/hr/hr"
        ]

    if name == "Mass":
        units = [
            "kg", 
            "g", 
            "lbs"
        ]
    
    if name == "Applied Force" or name == "Normal Force" or name == "Frictional Force":
        units = [
            "newtons"
            ]

    if name == "Coefficent of Friction":
        units = ["unitless"]

    variable = StringVar(level)
    variable.set(units[0]) # Default Value

    drop_down = OptionMenu(level, variable, units[0], *units)
    drop_down.pack()

    # Add submit button
    submit = Button(level, text="Submit", command= lambda: [addValue(LB, name, list, entry1.get()), canvas1.pack_forget(), 
                                                            submit.pack_forget(), drop_down.pack_forget()]) 
    canvas1.create_window(100, 25, window=submit)
    submit.pack(pady=1)  

    
def gravitySimulation():
    # Simulates gravity
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
    global tx
    global ty

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
                running = False

        screen.fill((255, 255, 255))

        player.gravity()
        player.update()

        player_list.draw(screen)
        ground_list.draw(screen)
        pygame.display.flip()
        clock.tick(fps)


def frictionSimulation():
    # Simulate a horizontal frictional force simulation
    # Create the screen
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
    global tx
    global ty

    fps = 60
    clock = pygame.time.Clock()

    box_width = 60
    box_heigth = 60
    
    player = Player()
    player.rect.x = 0
    player.rect.y = screen_height-ty
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
                running = False

        screen.fill((255, 255, 255))

        player.friction()
        player.update()

        player_list.draw(screen)
        ground_list.draw(screen)
        pygame.display.flip()
        clock.tick(fps)


def makeListBox(list, level):
    #Make Listbox
    my_listbox = Listbox(level)

    #Add options
    for item in list:
        my_listbox.insert(END, item)

    return my_listbox


def openSettings(function):
    # Add toplevel settings window
    global calculation
    global root
    global simulation
    global variables

    # Calculates acceleration and displays answer
    def accelerationCalculation(level):
        #TO-DO
        return 0

    # Calculates force and displays answer
    def forceCalculation(level):
        force = float(variables["Mass"]) * float(variables["Acceleration"])
        
        canvas1 = Canvas(level, width=100, height=25)
        canvas1.pack()

        label1 = Label(level, text = "Force = " + str(force) + " Newtons")
        canvas1.create_window(50, 12.5, window=label1)

    # Calculates the frictional force and displays answer
    def frictionCalculation(level):
        if variables["Normal Force"] !=0:
            variables["Frictional Force"] = float(variables["Coefficent of Friction"]) * float(variables["Normal Force"])
        else:
            variables["Frictional Force"] = float(variables["Coefficent of Friction"]) * float(variables["Gravity"]) * float(variables["Mass"])

        canvas1 = Canvas(level, width=100, height=25)
        canvas1.pack()

        label1 = Label(level, text = "Frictional Force = " + str(variables["Frictional Force"]) + " Newtons")
        canvas1.create_window(50, 12.5, window=label1)

    # Calculates velocity and displays answer
    def velocityCalculation(level):
        # TO-DO
        return 0

    # Calculates work and displays answer
    def workCalculation(level):
        # TO-DO
        return 0

    # Initializes settings window
    settings = Toplevel(root)

    settings.title("Settings")
    settings.geometry("400x400")

    Label(settings, text = "Settings").pack()

    # Add input values for listbox
    if (function == "Force Calculation"):
        variables["Mass"] = 0
        variables["Acceleration"] = 0
        calculation = "forceCalculation"

    if function == "Gravity Simulation":
        variables["Acceleration"] = 0
        simulation = "gravitySimulation"

    if function == "Friction Simulation":
        variables["Applied Force"] = 0
        variables["Coefficent of Friction"] = 0  
        variables["Frictional Force"] = 0      
        variables["Gravity"] = 0
        variables["Mass"] = 0
        variables["Normal Force"] = 0
        calculation = "frictionCalculation"
        simulation = "frictionSimulation"
        
    
    # Add settings listbox
    settings_LB = makeListBox(variables.keys(), settings)
    settings_LB.pack(fill = X)

    # Add select button
    select_button = Button(settings, text="Select", command = lambda: entryBox(settings_LB, settings, settings_LB.get(ANCHOR), variables))
    select_button.pack(pady=10)

    # Add calculate button
    if calculation != "":
        scope = locals()
        calculate_button = Button(settings, text="Calculate", command = lambda: eval(calculation + "(settings)", scope))
        calculate_button.pack(pady=10)

       
if __name__ == '__main__':
    main()