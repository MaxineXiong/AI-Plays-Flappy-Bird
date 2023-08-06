# Pygame is library for the development of multimedia applications like video games using Python
import pygame
import glob

# Load each image from a file source as a surface object, and double its original size
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(image)) for image in glob.glob("./images/bird*.png")]
BG_IMG = pygame.transform.scale2x(pygame.image.load("./images/bg.png"))


class BIRD:
    """
    Class for a flappy bird
    """

    # Load each bird image from a file source as a surface object, and double their original size
    IMGS = BIRD_IMGS
    # Maximum rotation degrees of a bird
    MAX_ROTATION = 25
    # By which degrees a bird is rotated in one tick/frame
    ROT_VEL = 20
    # Set the duration (in frames) for which a wing flapping state lasts
    ANIMATION_TIME = 5
    # Set acceleration value for calculating displacement
    ACCELERATION = 3


    def __init__(self, x: int, y: int):
        """
        Initialize the object BIRD.
        Parameters:
        - x: starting position on x-axis (int)
        - y: starting position on y-axis (int)
        return: None
        """
        # Set the starting (x, y) coordinate for the top left corner of the bird image
        self.x = x
        self.y = y
        self.height = self.y
        # Start with a rotation degree of 0
        self.tilt = 0
        # Initialize tick_count at 0 for a jumping-falling session
        self.tick_count = 0
        # Initialize velocity for calculating displacement
        self.vel = 0
        # Set starting image of the bird
        self.img = self.IMGS[0]
        # Initialize img_count at 0 for a wings flapping session: ↖ ↼ ↙ ↼
        self.img_count = 0


    def jump(self):
        """
        Make the bird jump
        return: None
        """
        # Whenever the bird starts to move upwards, set velocity to be -10.5
        self.vel = -10.5
        # Reset tick_count back to 0 everytime the bird jumps
        self.tick_count = 0
        # Reset the original height
        self.height = self.y


    def move(self):
        """
        Make the bird move
        return: None
        """
        # Incrementing tick_count
        self.tick_count += 1

        """
        Displacement: moving distance along y axis
        Displacement = [initial velocity] * [time] + 0.5 * [acceleration] * ([time]**2)
        """
        displacement = self.vel * self.tick_count + 0.5 * self.ACCELERATION * (self.tick_count**2)

        # If the bird is about to move down by more than 16 pixels, make the displacement remain at 16
        if displacement >= 16:
            displacement = 16
        # If the bird is about to move up, move up the bird a bit more by 2 more pixels
        if displacement < 0:
            displacement -= 2

        # Update y position of bird
        self.y += displacement

        if self.y < self.height + 50:
            # Do not tilt the bird's nose down until it drops more than 50 pixels below its original height
            # if self.tilt < self.MAX_ROTATION:
            self.tilt = self.MAX_ROTATION
        else:
            # Start tilting down the bird once it's dropped more than 50 pixels below the original height
            if self.tilt > -90:
                # Tilting down the bird by ROT_VEL degrees in each frame/tick until the degrees of rotation become lower than -90
                self.tilt -= self.ROT_VEL


    def draw(self, win):
        """
        Draw the bird flapping wings on the pygame window
        Parameters:
        - win: pygame window or surface
        return: None
        """
        # Incrementing img_count
        self.img_count += 1
        # Updating the bird image to show different wing flapping states
        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        # Start a new wings flapping session
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 1

        # Make the bird at a fixed wing flapping state if it's tilted more than 80 degrees downwards
        if self.tilt < -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        # Rotate the bird image on pygame window
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        # Get the rectangle of the rotated image
        rotated_image_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)
        # Draw the rotated image onto the pygame window
        win.blit(source = rotated_image, dest = rotated_image_rect.topleft)


    def get_mask(self):
        """
        Get the 2D bitmask from the surface object of the bird's current image for fast detection of Pixel Perfect Collision
        return: mask object
        """
        return pygame.mask.from_surface(self.img)




def test_BIRD_class():
    """
    Function for quickly testing the BIRD class
    """
    # Create an object of BIRD class
    bird = BIRD(200, 200)
    # Create pygame window object
    win = pygame.display.set_mode((500, 780))
    clock = pygame.time.Clock()

    run = True
    while run:
        # Set the game to run at most 30 frames per second
        clock.tick(30)
        # Draw background image onto the pygame window
        win.blit(BG_IMG, (0, 0))
        # Make the bird move
        bird.move()
        # Draw the bird onto the pygame window
        bird.draw(win)
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




# Testing BIRD class
#test_BIRD_class()
