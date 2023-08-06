import pygame
import glob
from random import randint
from BIRD_pygame import BIRD


# Load each image from a file source as a surface object, and double its original size
BASE_IMG = pygame.transform.scale2x(pygame.image.load("./images/base.png"))
PIPE_IMG = pygame.transform.scale2x(pygame.image.load("./images/pipe.png"))
BG_IMG = pygame.transform.scale2x(pygame.image.load("./images/bg.png"))

# Moving distance along x-axis per frame for Base and Pipes
BG_VEL = 5


class BASE:
    """
    Class for the moving floor in the game
    """

    # Get the surface object of the base floor image
    IMG = BASE_IMG
    # Get the width (in pixels) of the base floor image
    WIDTH = IMG.get_width()


    def __init__(self, y: int):
        """
        Initialize the object of BASE with a given y position.
        Parameters:
        - y: position on y-axis (int)
        return: None
        """

        # Set the y pos for the top left corner of both base floor images
        self.y = y
        # Set the starting x pos for the top left corner of the first base floor image
        self.x1 = 0
        # Set the starting x pos for the top left corner of the second base floor image
        self.x2 = self.WIDTH


    def move(self):
        """
        Method to update the x position of both base images for animation
        """

        # The floor images move to the left by a distance of BG_VEL
        self.x1 -= BG_VEL
        self.x2 -= BG_VEL

        # Check if the first base image has moved completely off the screen to the left
        # If so, reset its position to the right of the second base image to create a seamless loop
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        # Check if the second base image has moved completely off the screen to the left
        # If so, reset its position to the right of the next base image to create a seamless loop
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH


    def draw(self, win):
        """
        Method to draw the base floor images on the game window to create a continuous floor effect.
        Parameters:
        - win: pygame window or surface
        return: None
        """
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))



class PIPE:
    """
    Class for the moving pipes with random heights
    """

    # Flip the pipe image upside down to represent the top pipe
    TOP_IMG = pygame.transform.flip(surface = PIPE_IMG, flip_x = False, flip_y = True)
    # Define the bottom pipe image
    BOTTOM_IMG = PIPE_IMG
    # Set the gap between top and bottom pipes
    GAP = 200
    # Get the original height (in pixels) of the pipe image
    HEIGHT = TOP_IMG.get_height()
    # Get the width (in pixels) of the pipe image
    WIDTH = TOP_IMG.get_width()


    def __init__(self, x: int):
        """
        Initialize the object of PIPE with a given x position.
        Parameters:
        - x: position on x-axis (int)
        return: None
        """

        self.x = x
        # Set the height for the top pipe using a random value between 50 and 450
        self.top_height = randint(50, 450)
        # Calculate the y pos for the top left corner of the top and bottom pipes
        self.top_y = - (self.HEIGHT - self.top_height)
        self.bottom_y = self.top_height + self.GAP
        # Initialize the 'passed' attribute to False, used to track if the bird has passed the pipe
        self.passed = False


    def move(self):
        """
        Method to update the x position of the pipe for animation
        """
        # The pipe moves to the left by a distance of BG_VEL
        self.x -= BG_VEL


    def collide(self, bird):
        """
        Method to detect Pixel Perfect Collision between the bird and pipes.
        Pixel Perfect Collision: Collision is recognised only when non-transparent pixel inside an image matrix collides with one inside another image matrix.

        Parameters:
        - bird: an object of BIRD
        return: Bool
        """

        # Get the masks for bird, top pipe and bottom pipe
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.TOP_IMG)
        bottom_mask = pygame.mask.from_surface(self.BOTTOM_IMG)

        # Use mask.overlap() method to detect Pixel Perfect Collision
        # mask.overlap(other, offset) -> (x, y)
        # mask.overlap(other, offset) -> None
        # The overlap() method returns the first point of intersection encountered between this mask and other.

        # Calculate the top_offset and bottom_offset that will be used as arguments in overlap() function
        top_offset = (self.x - bird.x, self.top_y - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom_y - round(bird.y))
        # Detect the collision point between the bird and top pipe
        t_point = bird_mask.overlap(top_mask, top_offset)
        # Detect the collision point between the bird and bottom pipe
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)

        if t_point or b_point:
            # Return True if there is a collision between the bird and either the top or bottom pipe
            return True
        else:
            # Return False if there is no collision
            return False


    def draw(self, win):
        """
        Method to draw the top and bottom pipe images on the game window.
        Parameters:
        - win: pygame window or surface
        return: None
        """
        win.blit(self.TOP_IMG, (self.x, self.top_y))
        win.blit(self.BOTTOM_IMG, (self.x, self.bottom_y))




def test_BASE_PIPE():
    """
    Function for testing BASE and PIPE classes
    """

    # Create objects of BIRD, PIPE and BASE class
    bird = BIRD(230, 350)
    base = BASE(700)
    pipes = [PIPE(700)]
    
    # Create pygame window object
    win = pygame.display.set_mode((530, 780))

    # Initialize the pygame font module
    pygame.font.init()
    # Set the system font for the game
    text_font = pygame.font.SysFont("comicsans", 40)

    # Create pygame clock object to manage the game's frame rate
    clock = pygame.time.Clock()
    # Initialize the player's score to 0
    score = 0

    run = True
    while run:
        # Set the game to run at most 30 frames per second
        clock.tick(30)
        # Draw background image onto the pygame window
        win.blit(BG_IMG, (0, 0))
        # Draw the moving base floor image onto the pygame window
        base.move()
        base.draw(win)
        # Draw the bird onto the pygame window
        bird.draw(win)

        # Initialize an empty list to store pipes that need to be removed
        pipes_to_remove = []
        # Initialize a boolean variable to track whether a new pipe needs to be added
        add_pipe = False
        # Loop through all the pipes in the 'pipes' list
        for pipe in pipes:
            # Draw the moving pipes onto the pygame window
            pipe.move()
            pipe.draw(win)
            # Check if the pipe has moved completely off the screen to the left
            # If so, add it to the 'pipes_to_remove' list for deletion
            if pipe.x + pipe.WIDTH < 0:
                pipes_to_remove.append(pipe)
            # Check if the pipe has just been flown through by the bird
            # If so, mark it as "passed", and set 'add_pipe' to True to indicate that a new pipe needs to be added to the 'pipes' list
            if (pipe.passed == False) and (pipe.x + pipe.WIDTH < bird.x):
                pipe.passed = True
                add_pipe = True

        # Update the list of pipes and the player's score
        if add_pipe:
            # Increment the player's score by 1 for successfully passing a pipe
            score += 1
            # Add a new pipe to the 'pipes' list that will be placed at a position of 550 pixels on the right side of the window
            pipes.append(PIPE(550))

        # Check if there are any pipes in the 'pipes_to_remove' list that need to be deleted
        if len(pipes_to_remove) > 0:
            # Loop through the pipes in 'pipes_to_remove' and remove them from the 'pipes' list
            for p in pipes_to_remove:
                pipes.remove(p)

        # Draw current score onto the pygame window
        score_text = text_font.render("Score: " + str(score),
                                      True,                 # antialisa = True: Characters will have smooth edges
                                      (255, 255, 255))      # white text color
        win.blit(score_text, (530 - 15 - score_text.get_width(), 15))

        # Display the pygame surface on user's monitor
        pygame.display.update()

        # Break the loop if button "X" is clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    # Quit the game
    pygame.quit()
    # Close the application
    quit()




# Testing BASE and PIPE classes
#test_BASE_PIPE()
