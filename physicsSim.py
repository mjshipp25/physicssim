from tkinter import *
from tkinter.ttk import *
import pygame
import sys


# Initialize the pygame
pygame.init()

root = Tk()
root.title('Physics Simulator')
root.iconbitmap('d:/projects/physicssim/physicssim.ico')
root.geometry("400x400")

variables = {}
calculation= ""


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


def simulate():
    # Create the Screen
    height = 600
    width = 800
    screen = pygame.display.set_mode((width, height))
    screen.fill((255, 255, 255))
    pygame.display.flip()
    pygame.display.set_caption('Simulation')

    simulator_icon = pygame.image.load("physicssim-1.png")
    pygame.display.set_icon(simulator_icon)

    # Game Loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.quit()

        # Draw box
        black = (0, 0, 0)
        box_width = 60
        box_heigth = 60
        pygame.draw.rect(screen, black, pygame.Rect(width/2 - box_width/2, 0, box_width, box_heigth))
        pygame.display.flip()



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


def makeListBox(list, level):
    #Make Listbox
    my_listbox = Listbox(level)

    #Add options
    for item in list:
        my_listbox.insert(END, item)

    return my_listbox


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


def addValue(LB, name, list, value):
    list[name] = value
    entry = name + ": " + list[name]
    LB.delete(ANCHOR)
    LB.insert(ANCHOR, entry)


def forceCalculation(level):
    force = int(variables["Mass"]) * int(variables["Acceleration"])
    
    canvas1 = Canvas(level, width=100, height=25)
    canvas1.pack()

    label1 = Label(level, text = "Force = " + str(force) + " Newtons")
    canvas1.create_window(50, 12.5, window=label1)


if __name__ == '__main__':
    main()