from BIRD_pygame import BIRD
from BASE_PIPE_pygame import BASE, PIPE
import pygame
import neat
import pickle
import os


"""
Genetic algorithm: NEAT (NeuroEvolution of Augmenting Topologies)
- inspired by natural selection
- a process of generations continually learning and getting better (evolved) until eventually they can get as good as they can (become unbeatable)
- 1) create a population: each population consists of eg. 100 birds. Each bird has a neutral network controlling it
  2) we test each neutral network and evaluate their fitness
  3) When all birds in a generation die, get rid of the other poorly-performing birds, mutate and breed (i.e. cross over disparate topologies) the best-performing birds in the last population to create a new population -> more nodes and connection genes will be added to bird's neural network and the architecture will get more complex

- Important Attributes of neural network:
  1) Inputs (3 neurons): bird.y, distance between bird.y and top_pipe, distance between bird.y and bottom_pipe
  2) output (1 neuron): Jump?
  3) Activation function = tanh (output value will be between -1 and 1)
  4) population size each generation: 100 (adjustable)
  5) fitness function: how we assess the birds' performance (i.e. how we score the birds)
  6) max generation: 30
"""


class NeatApp:
    """
    Class for the NEAT app that implements the NEAT algorithm
    to train and evolve a population of birds in a Flappy Bird-like game.
    """

    # Set the width and height of pygame window
    WIN_WIDTH = 530
    WIN_HEIGHT = 780
    # Set the game to run at most 30 frames per second
    FRAMES_PER_SECOND = 30
    # The fitness function eval_genomes() will be called for up to 30 generations
    MAX_GENS = 30



    def __init__(self, config_path):
        """
        Initialize the 'NeatApp' object with a given path to the configuration file.
        """

        self.config_path = config_path
        # Load the required NEAT config from the config file
        self.config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, self.config_path)
        # Create a population object that implements the core evolution algorithm:
        # 1. Evaluate the fitness of all genomes
        # 2. Check to see if the termination criterion is satisfied; exit if it is
        # 3. Generate the next generation from the current generation
        # 4. Partition the new generation into species based on genetic similarity
        # 5. Go to 1
        self.p = neat.Population(self.config)

        # Initialize the generation count to 0
        self.gen_count = 0
        # Initialize the player's score to 0
        self.score = 0



    def run(self):
        """
        Method to run the NEAT algorithm and evolve the birds through successive generations.
        """

        # Show statistics in terminal
        self.p.add_reporter(neat.StdOutReporter(True))  # show_species_details = True
        self.p.add_reporter(neat.StatisticsReporter())

        # Run the fitness function eval_genomes() for up to MAX_GENS generations
        winner = self.p.run(self.eval_genomes, self.MAX_GENS)

        # Show stats for the winner genome in the terminal
        print('\nBest genome:\n{!s}'.format(winner))

        # Save the winner genome to a pkl file
        with open('winner.pkl', 'wb') as f:
            pickle.dump(winner, f)



    def eval_genomes(self, genomes, config):
        """
        The fitness function that simulates the current population of birds attempting to fly through the pipes,
        and evaluates the fitness of each genome (bird) in the population based on how far they progress in the game.
        """

        # Increment gen_count by 1 everytime the eval_genomes() function is called
        self.gen_count += 1
        # Reset the player's score back to 0 everytime the eval_genomes() function is run with a new generation
        self.score = 0

        # Create the three lists to store genomes, neural networks, and bird objects for each genome in the current generation
        self.gns = []
        self.nets = []
        self.birds = []
        for g_id, g in genomes:
            # Initialise the fitness score of each genome to 0
            g.fitness = 0
            # Add each updated genome to the 'gns' list
            self.gns.append(g)

            # Create a feed-forward neural network for each genome
            net = neat.nn.FeedForwardNetwork.create(g, config)
            # Add each neural network to the 'nets' list
            self.nets.append(net)

            # Create and store the bird object for each genome, all starting at the same position on the pygame window
            self.birds.append(BIRD(230, 350))


        # Initialise a new round of the game
        self.init_game()


        run = True
        while run:
            # Set the maximum frames per second at which the game is run
            self.clock.tick(self.FRAMES_PER_SECOND)

            # Check if there are still birds alive in the current generation
            if len(self.birds) > 0:
                # Take the first pipe as the upcoming pipe
                upcoming_pipe_id = 0
                # If the birds are between two pipes...
                if (len(self.pipes) > 1) and ( (self.pipes[0].x + self.pipes[0].WIDTH) < self.birds[0].x ):
                    # ...take the second pipe as the upcoming pipe
                    upcoming_pipe_id = 1
                # Get the pipe object that the birds are flying towards or passing through
                upcoming_pipe = self.pipes[upcoming_pipe_id]

                # Iterate through each bird's genome, neural network, and bird object
                for i in range(len(self.birds)):
                    # Increment the fitness score of each genome by 0.1 per frame
                    self.gns[i].fitness += 0.1

                    # Make each bird move
                    self.birds[i].move()

                    # Determine whether the bird should jump or not to avoid hitting the upcoming pipe
                    self.bird_jump(self.nets[i], self.birds[i], upcoming_pipe)

                # Eliminate the birds that have collided with either the pipes, ceiling, or base floor
                self.remove_colliding_birds()


                # Make all the pipes move and update the 'pipes' list accordingly
                self.update_pipes()


                # Make the base floor move
                self.base.move()


                # Get the number of birds alive
                self.num_lives = len(self.birds)


                # Draw all elements onto the pygame window
                self.draw_all()


            else:
                # If all birds are extinct, break the loop.
                # The population object "p" will recall the eval_genomes() function to run with the next generation
                run = False


            # If the button "X" is clicked
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Quit the game
                    pygame.quit()
                    # Quit the program
                    quit()



    def init_game(self):
        """
        Method to initialise the game environment and objects required to start a new round of game
        """
        # Create pygame window object
        self.win = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))

        # Initialise the pygame font module
        pygame.font.init()
        # Set the system font for the game
        self.text_font = pygame.font.SysFont("comicsans", 40)

        # Create pygame clock object to manage the game's frame rate
        self.clock = pygame.time.Clock()

        # Initialise the 'base' object and 'pipes' list
        self.base = BASE(700)
        self.pipes = [PIPE(700)]



    def bird_jump(self, net, bird, upcoming_pipe):
        """
        Method to determine whether a bird should jump or not based on the output value of its neural network
        """
        # Feed the three inputs into the target bird's neural network to get an output value that falls within a range of -1 to 1
        output = net.activate( (
                                 bird.y,
                                 abs(bird.y - upcoming_pipe.top_height),
                                 abs(bird.y + bird.img.get_height() - upcoming_pipe.bottom_y)
                                ) )[0]
        if output > 0.5:
            # Make the bird jump if the output value is higher than 0.5
            bird.jump()



    def remove_colliding_birds(self):
        """
        Method to identify and eliminate the birds that have collided with obstacles in the game,
        such as pipes, ceiling, or base floor.
        """

        # Eliminate the birds that have collided with any of the pipes
        for pipe in self.pipes:
            # Capture the birds that have collided with either the top or bottom pipe
            birds_to_remove = []
            for bird in self.birds:
                if pipe.collide(bird):
                    birds_to_remove.append(bird)
            # Remove all the colliding birds from the game
            self.eliminate_birds(birds_to_remove)

        # Eliminate the birds that have collided with either the ceiling or floor
        # Capture the colliding birds
        birds_to_remove = []
        for bird in self.birds:
            if (bird.y <= 0) or ((bird.y + bird.img.get_height()) >= self.base.y):
                birds_to_remove.append(bird)
        # Remove all the colliding birds from the game
        self.eliminate_birds(birds_to_remove)



    def eliminate_birds(self, birds_to_remove):
        """
        Method to remove the genomes, neural netowrks, and bird objects of the target birds from the three lists
        """
        # Check if there are any birds to remove
        if len(birds_to_remove) > 0:
            # Iterate through each bird to remove
            for b in birds_to_remove:
                # Get the index of the current bird in the 'birds' list
                b_id = self.birds.index(b)
                # Remove the genome, neural network, and bird object associated with the current bird from the three lists
                self.gns.pop(b_id)
                self.nets.pop(b_id)
                self.birds.pop(b_id)



    def update_pipes(self):
        """
        Method that makes the pipes move and updates pipes in the game
        """

        # Initialise the boolean variable as False, which will track whether a new pipe needs to be added
        add_pipe = False
        # Initialise the list variable as an empty list, which will store pipes that need to be removed
        pipes_to_remove = []

        # Check if there are still birds alive in the current generation
        if len(self.birds) > 0:
            # Iterate through each pipe in the 'pipes' list
            for pipe in self.pipes:
                # Check if the current pipe has just been flown through by the birds
                if (pipe.passed == False) and (pipe.x + pipe.WIDTH < self.birds[0].x):
                    # If so, mark it as "passed", and set 'add_pipe' to True to indicate that a new pipe needs to be added to the 'pipes' list
                    pipe.passed = True
                    add_pipe = True

                # Make the current pipe move
                # Check if the current pipe has moved completely off the screen to the left
                if pipe.x + pipe.WIDTH < 0:
                    # If so, move the pipe first, then add it to the 'pipes_to_remove' list for deletion
                    pipe.move()
                    pipes_to_remove.append(pipe)
                else:
                    # Otherwise, simply move the pipe
                    pipe.move()

        # Update the list of pipes, genome fitness scores, and the player's score
        # Check if a bird has just successfully passsed through a pipe
        if add_pipe:
            # If so, increment the player's score by 1
            self.score += 1
            # Add a new pipe to the 'pipes' list that will be placed at a position of 550 pixels on the right side of the window
            self.pipes.append(PIPE(550))
            # Reward each genome with 5 more fitness score points
            for g in self.gns:
                g.fitness += 5

        # Check if there are any pipes in the 'pipes_to_remove' list that need to be deleted
        if len(pipes_to_remove) > 0:
            # If so, loop through each pipe in 'pipes_to_remove' and remove them from the 'pipes' list
            for p in pipes_to_remove:
                self.pipes.remove(p)



    def draw_all(self):
        """
        Method to draw all game elements, including birds, pipes, base floor, and indicator texts, onto the pygame window
        """

        # Load the background image from a file source as a surface object, and double its original size
        bg_img = pygame.transform.scale2x(pygame.image.load("./images/bg.png"))
        # Draw background image onto the pygame window
        self.win.blit(bg_img, (0, 0))

        # Draw each pipe onto the pygame window
        for pipe in self.pipes:
            pipe.draw(self.win)

        # Draw the base floor onto the pygame window
        self.base.draw(self.win)

        # Draw each bird onto the pygame window
        for bird in self.birds:
            bird.draw(self.win)

        # Display the current score as text on the pygame window
        score_text = self.text_font.render("Score: " + str(self.score),
                                            True,                 # antialisa = True: Characters will have smooth edges
                                            (255, 255, 255))      # white text color
        self.win.blit(score_text, (self.WIN_WIDTH - 15 - score_text.get_width(), 15))

        # Display the generation count as text on the pygame window.
        gen_text = self.text_font.render("Gens: " + str(self.gen_count),
                                          True,
                                          (255, 255, 255))
        self.win.blit(gen_text, (15, 15))

        # Display the number of birds alive as text on the pygame window
        alive_text = self.text_font.render("Alive: " + str(self.num_lives),
                                            True,
                                            (255, 255, 255))
        self.win.blit(alive_text, (15, 15 + gen_text.get_height() + 10))

        # Display the pygame surface on user's monitor
        pygame.display.update()



    def play_with_best_bird(self, genome_path):
        """
        Method to load the winner genome from a saved pickle file, and play the game using the best bird (genome)
        """
        # Unpickle the saved winner genome
        with open(genome_path, 'rb') as f:
            genome = pickle.load(f)

        # Convert loaded genome into required data structure
        genomes = [(1, genome)]

        # Call the eval_genomes() method with only the loaded genome
        self.eval_genomes(genomes, self.config)






# Check if the script is being run directly as the main program
if __name__ == '__main__':
    # Create an instance of the 'NeatApp' class with the specified configuration file path
    app = NeatApp('./config-feedforward.txt')

    # Run successive generations to train and evolve 100 birds at a time, and save the winner genome in the end
    #app.run()

    # Play the game with only the winner bird
    genome_path = 'winner.pkl'
    if os.path.exists(genome_path):
        # If the file path exists, load the winner genome, and play the game using the best bird only
        app.play_with_best_bird(genome_path)
