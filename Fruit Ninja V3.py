from tkinter import *
import random
from tkinter import messagebox

root = Tk()


class Menu:
    def __init__(self):
        # make an instance of instructions
        self.instruction_instance = Instructions()

        # creating a frame for the menu buttons
        self.menu_frame = Frame(root)
        self.menu_frame.pack()

        # Button to start playing
        self.button_for_play_game = Button(self.menu_frame, text="Play Game", command=self.start_game)
        self.button_for_play_game.pack()

        # button that brings the instructions
        self.button_for_instructions = Button(self.menu_frame, text="How To Play", command=self.start_instructions)
        self.button_for_instructions.pack()

        # button to exit from the game, it will execute root.destroy()
        self.button_for_exit = Button(self.menu_frame, text="Exit", command=self.exit_game)
        self.button_for_exit.pack()

        self.game_instance = None

    # takes the menu off the root window when other things are needed to be packed on
    def destroy_menu_frame(self):
        self.menu_frame.destroy()

    # Pack the instruction frames on
    def start_instructions(self):
        self.instruction_instance.pack_instructions()

    # when the start_game button is pressed this is function is called
    def start_game(self):
        # get rid of the menu frame first
        self.destroy_menu_frame()
        self.game_instance = MyGame()
        root.bind('<space>', self.game_instance.press_to_start)

    #remake the menu
    def make_menu_again(self):
        global menu
        menu = Menu()

    #exit the game when the exit button is pressed
    def exit_game(self):
        root.destroy()


class Instructions:
    instructions = '''Hold left click to slice through the patterns
        Black squares are fruits, slice through them you will get points.
        Red circles are bombs, try avoiding them
        You can only miss maximum of 3 fruits
        Slice through as many fruits as possible to get a high score'''

    def __init__(self):
        self.instructions_frame = Frame(root)
        self.instructions_label = Label(self.instructions_frame, text=self.instructions, font=("Helvetica", 15))
        self.button_return_to_menu = Button(self.instructions_frame, text="press to return to menu",
                                            command=self.return_to_menu)
        self.instructions_label.pack()
        self.button_return_to_menu.pack()

    # when the return to menu button is pressed
    def return_to_menu(self):
        # delete the instruction frame, then make a menu again
        self.instructions_frame.destroy()
        menu.make_menu_again()

    def pack_instructions(self):
        menu.destroy_menu_frame()
        self.instructions_frame.pack()


class MyGame:
    max_number_patterns = 3

    def __init__(self):
        self.score = 0
        self.patterns_missed = 0

        self.game_frame = Frame(root)
        self.game_canvas = Canvas(self.game_frame, width=450, height=450)

        self.score_label = Label(self.game_frame, text=("Score: " + str(self.score)), font=("Helvetica", 30))
        self.score_label.grid(row=0, column=0, sticky=W)

        self.X_frames = Frame(self.game_frame)
        self.X_frames.grid(row=0, column=1, sticky=E)

        self.missed_label1 = Label(self.X_frames, text="X", font=("ms serif bold", 30), fg="grey")
        self.missed_label1.pack(side=RIGHT)

        self.missed_label2 = Label(self.X_frames, text="X", font=("ms serif bold", 30), fg="grey")
        self.missed_label2.pack(side=RIGHT)

        self.missed_label3 = Label(self.X_frames, text="X", font=("ms serif bold", 30), fg="grey")
        self.missed_label3.pack(side=RIGHT)

        # Packing on to the root window
        self.game_frame.pack()
        # self.game_frame.pack_propagate(False)
        self.game_canvas.grid(row=1, column=0, columnspan=2)

        # Update the window but Could be changed to root later when menu is added on
        self.game_frame.update()

        self.window_height = self.game_canvas.winfo_height()
        self.window_width = self.game_canvas.winfo_width()

        self.text_on_canvas = self.game_canvas.create_text(self.window_width / 2,
                                                           self.window_height / 2,
                                                           text="PRESS <SPACE> TO START GAME", font=('System', 20))
        # Making Drawing instance and binding
        self.drawing_instance = None

    def press_to_start(self, event):
        root.unbind('<space>')
        self.making_patterns()
        self.making_box_boundary_lines()
        self.game_canvas.delete(self.text_on_canvas)
        self.drawing_instance = Drawing(self.game_canvas)
        self.game_canvas.bind('<B1-Motion>', self.drawing_instance.b1_motion)
        self.game_canvas.bind('<ButtonRelease-1>', self.drawing_instance.delete_dots)

    def making_box_boundary_lines(self):

        self.game_canvas.create_line(0, self.window_height - 3, self.window_width - 3, self.window_height - 3)
        self.game_canvas.create_line(self.window_width - 3, 0, self.window_width - 3, self.window_height - 3)
        self.game_canvas.create_line(2, 0, 2, self.window_height - 2)

    def making_patterns(self):
        # Local variable how_many_patterns is a integer. To get how many patterns should pop up together
        if len(Pattern.list_of_patterns) <= self.max_number_patterns:
            how_many_patterns = (random.randint(1, 2))
            for number in range(how_many_patterns):
                a = Pattern(self.game_canvas, self.window_width, self.window_height)
                a.move_patterns()

    def finish_game(self):
        self.game_canvas.unbind('<B1-Motion>')
        print("Game has finished, your score is: " + str(self.score))
        self.drawing_instance.delete_dots(None)

        # self.game_canvas.delete("all")
        Pattern.list_of_patterns = []
        Pattern.list_of_bombs = []

        messagebox.showinfo("Game finished!", "Your score is: {} \nClick OK to go back to main menu"
                            .format(menu.game_instance.score))
        self.game_frame.destroy()
        menu.make_menu_again()


class Drawing:
    line_colour = "black"

    def __init__(self, canvas):
        self.game_canvas = canvas

        self.list_of_dots = []
        self.list_of_lines = []

        self.drawn_dot = None
        self.drawn_line = None

        self.length_of_the_line = 40

    def b1_motion(self, event):

        self.drawn_dot = self.game_canvas.create_rectangle(event.x, event.y, event.x, event.y, fill=self.line_colour,
                                                           outline=self.line_colour)
        self.list_of_dots.append(self.drawn_dot)

        if len(self.list_of_dots) >= 2:
            self.drawn_line = self.game_canvas.create_line((self.game_canvas.coords(self.list_of_dots[-2])[0]),
                                                           (self.game_canvas.coords(self.list_of_dots[-2])[1]), event.x,
                                                           event.y)
            self.game_canvas.itemconfigure(self.drawn_line, fill=self.line_colour, width=5)
            self.list_of_lines.append(self.drawn_line)

            self.collision()

        while len(self.list_of_dots) > self.length_of_the_line:
            self.game_canvas.delete(self.list_of_dots[0])
            self.list_of_dots.pop(0)

        while len(self.list_of_lines) > self.length_of_the_line:
            self.game_canvas.delete(self.list_of_lines[0])
            self.list_of_lines.pop(0)

    def delete_dots(self, event):

        for dot in self.list_of_dots:
            self.game_canvas.delete(dot)
            self.list_of_dots = []

        for line in self.list_of_lines:
            self.game_canvas.delete(line)
            self.list_of_lines = []

        return None

    # Finding if there is any collision on the canvas when is the mouse is moved
    def collision(self):
        list_of_collided_items = self.game_canvas.find_overlapping(*self.get_coordinates())

        pattern_collided = list_of_collided_items[0]
        # Deleting objects

        if pattern_collided in Pattern.list_of_bombs:
            print("BOOM, you have sliced through a bomb")
            menu.game_instance.finish_game()



        elif pattern_collided in Pattern.list_of_patterns:
            Pattern.list_of_patterns.remove(pattern_collided)
            self.game_canvas.delete(list_of_collided_items[0])
            menu.game_instance.making_patterns()
            menu.game_instance.score += 1
            menu.game_instance.score_label.config(text=("Score: " + str(menu.game_instance.score)))

    def get_coordinates(self):

        return self.game_canvas.coords(self.drawn_line)


class Pattern:
    list_of_patterns = []
    list_of_bombs = []

    pattern_width = 40

    pattern_color = "black"
    bomb_colour = "red"

    def __init__(self, canvas, window_width, window_height):
        self.game_canvas = canvas

        # Generating a random number to show if the pattern is going to be a bomb
        # 10% Chance of getting a bomb
        if random.randint(0, 100) < 13:
            self.boolean_of_bomb = True
        else:
            self.boolean_of_bomb = False
        # boolean, if true this pattern is going to be a bomb
        self.window_width = window_width
        self.window_height = window_height

        self.width = self.pattern_width

        self.x = random.randrange(self.window_width - self.width)
        self.y = self.window_height

        self.x_velocity = random.uniform(-0.7, 0.7)

        self.y_velocity = -5

        # The acceleration(gravity value) changes as y velocity changes
        # Increasing 729 will make the distance go up
        self.y_acceleration = round(float((self.y_velocity ** 2) / (self.window_height * 0.73 * 2), ), 4)

        self.pattern_created = self.create_pattern()
        self.list_of_patterns.append(self.pattern_created)

    def create_pattern(self):

        if self.boolean_of_bomb is True:
            pattern_bomb = self.game_canvas.create_oval(self.x, self.y, self.x + self.width, self.y + self.width,
                                                        fill=self.bomb_colour)
            self.list_of_bombs.append(pattern_bomb)

            return pattern_bomb

        else:
            pattern_rectangle = self.game_canvas.create_rectangle(self.x, self.y, self.x + self.width,
                                                                  self.y + self.width, fill=self.pattern_color)
            return pattern_rectangle

    def move_patterns(self):
        # If the pattern has been deleted, making the coordinates list empty
        if len(self.list_of_patterns) == 0 or len(self.get_coordinates()) == 0:
            return

        # 6+0.05, eventually yv will become positive, so the pattern will start to drop
        self.y_velocity += self.y_acceleration

        if self.get_coordinates()[0] + self.x_velocity <= 1:
            self.x_velocity = abs(self.x_velocity)

        # checking if pattern reaches the bottom of the frame
        elif self.get_coordinates()[2] + self.x_velocity >= self.window_width:

            self.x_velocity = -abs(self.x_velocity)

        # checking if pattern reaches the top of the frame
        if self.get_coordinates()[1] + self.y_velocity <= 0:
            self.y_velocity = abs(self.y_velocity)

        # checking if pattern reaches the bottom of the frame , with positive velocity(falling down)
        elif self.get_coordinates()[3] + self.y_velocity >= self.window_height + self.width and self.y_velocity > 0:

            # check if this a bomb, if not bomb, then missed + 1
            if self.boolean_of_bomb is False:
                menu.game_instance.patterns_missed += 1
                # if the player missed 1 fruit,changing the label to show that the player has missed one
                if menu.game_instance.patterns_missed == 1:
                    menu.game_instance.missed_label3.configure(fg="red")
                # if the player missed 2 fruits,changing the label to show that the player has missed two
                elif menu.game_instance.patterns_missed == 2:
                    menu.game_instance.missed_label2.configure(fg="red")

                # if the player missed 3 fruits
                elif menu.game_instance.patterns_missed == 3:
                    # changing the label to show that the player has missed 3
                    menu.game_instance.missed_label1.configure(fg="red")
                    print("You missed 3 fruits")

                    # The game has finished when the player missed 3, so call finish_game in game
                    menu.game_instance.finish_game()

                    # returns out of the move() function and stops the pattern from moving
                    return

            # calling the removing function to remove the pattern from the canvas and the list
            # as it has fallen out of the window
            self.removing_pattern_from_canvas()

            # self.y_velocity = -abs(self.y_velocity)

        self.game_canvas.move(self.pattern_created, self.x_velocity, self.y_velocity)

        # Call move function itself again after 10milli seconds to move it
        root.after(10, self.move_patterns)

    # Get coordinates of the pattern
    def get_coordinates(self):
        return self.game_canvas.coords(self.pattern_created)

    def removing_pattern_from_canvas(self):
        self.list_of_patterns.remove(self.pattern_created)
        if self.boolean_of_bomb is True:
            self.list_of_bombs.remove(self.pattern_created)
        self.game_canvas.delete(self.pattern_created)
        menu.game_instance.making_patterns()


menu = Menu()

# root.resizable(False,False)

root.mainloop()
