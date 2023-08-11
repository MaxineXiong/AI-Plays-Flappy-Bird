# AI Plays Flappy Bird
[![GitHub](https://badgen.net/badge/icon/GitHub?icon=github&color=black&label)](https://github.com/MaxineXiong)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Made with Python](https://img.shields.io/badge/Python->=3.6-blue?logo=python&logoColor=white)](https://www.python.org)
[![Pygame - >=2.0](https://img.shields.io/badge/Pygame->=2.0-ADFF2F)](https://www.pygame.org/docs/)

<br/>

## **Project Description**

The **AI Plays Flappy Bird with NEAT** project is an implementation of the **[NeuroEvolution of Augmenting Topologies (NEAT)](https://neat-python.readthedocs.io/en/latest/neat_overview.html)** algorithm in Python, which evolves a population of virtual birds through successive generations based on their performance in a Flappy Bird-like game. The classic 2D game, [***Flappy Bird***](https://flappybird.io/), was once renowned for its high level of challenge and addictiveness among players. Players are required to control a yellow bird in the game, maneuvering it through columns of green pipes without collision. Successfully passing through columns earns players score points, motivating them to achieve higher scores.

In this project, the NEAT algorithm orchestrates the **evolution** and **evaluation** of a bird population through **successive generations** until the fitness threshold is met. Each bird is controlled by a **genome (genotype)** that encapsulates critical genetic information, including the architecture, connection weights, and other parameters of a neural network. The algorithm releases this population of genetically diverse birds into the game environment to **evaluate their fitness**. A **feedforward neural network (phenotype)** is created for each bird at the beginning of the game using its genome as a blueprint. Each network then continues to process input data and generates output predictions as the associated bird progresses in the game. 

The algorithm employs the **fitness score** to assess a genome's performance. When a bird successfully passes a pipe, it earns extra fitness points. As a result, higher fitness scores indicate better genome performance. During the evaluation process, birds that collide with the ceiling, floor, or pipes are promptly eliminated from the game, **as illustrated in the GIF image below**. Once all birds in a generation have been eliminated, the algorithm prunes the underperforming genomes and potentially **mutates** or **breeds** the best-performing genomes to create a new generation of evolved birds, which will also undergo the fitness evaluation within the game environment as the previous generation does.

<p align="center">
  <img src="./images/demo.gif" height=580 />
</p>

The process of **evolution and evaluation** may iterate across multiple generations **until the fitness threshold is met or exceeded**. The ultimate winner genome, demonstrating exceptional gameplay, is saved as a pickle file. This file can be reloaded to relive the game, showcasing the impressive capabilities of the evolved AI.

_**Press and hold the CTRL key while clicking the badge icon below to see AI playing the Flappy Bird-like game with the winner genome** (It is recommended to open the Replit IDE on a <ins>desktop monitor</ins> for better viewing experience)_:

[![Run on Repl.it](https://replit.com/badge/github/MaxineXiong/AI-Plays-Flappy-Bird.git)](https://replit.com/@MaxineXiong/AI-Plays-Flappy-Bird?v=1)

<br/>


## **Features**

- Utilizes the NEAT algorithm to evolve a population of birds through successive generations.
- Each bird is controlled by a genome that encodes genetic information about the neural network’s architecture, connection weights, and parameters.
- At the start of every new round of the game, a feed-forward neural network (phenotype) is created for each bird using its genome (genotype) as blueprint.
- Fitness evaluation is based on how far a bird progresses in the game.
- Automatic mutation or/and breeding of disparate neural network topologies to create the next generation of birds with more complex network architecture.
- The ultimate best-performing genome is saved as a pickle file for later use.
- Real-time visualization of evolving bird gameplay.

<br/>

## **Repository Structure**

The repository is structured as follows:

```
AI-Plays-Flappy-Bird-with-NEAT/
├── Main.py
├── BIRD_pygame.py
├── BASE_PIPE_pygame.py
├── config-feedforward.txt
├── winner.pkl
├── images/
│   └── *.png
├── requirements.txt
├── README.md
└── LICENSE
```

- **Main.py**: the core Python program that implements NEAT to evolve and evaluate a population of birds in a game environment through successive generations until the fitness threshold is met. Users can replay the game with the saved winner genome.
- **BIRD_pygame.py**: This Python script declares the `BIRD` class, which is instantiated for each genome in the **Main.py** program. The class defines the behaviour of the bird, dictating how it moves and jumps within the game environment.
- **BASE_PIPE_pygame.py**: This Python script declares the classes `BASE` and `PIPE` that both are instantiated in the **Main.py** as components of the game simulation. The `BASE` class defines the behaviour of the base floor moving in the game, while the `PIPE` class models how the green pipe move within the game and determines if a bird collides with the pipe column, crucial for evaluating the birds' fitness.
- **config-feedforward.txt**: This configuration file plays a vital role in fine-tuning the genetic NEAT algorithm and customizing the experiment's parameters. It provides a comprehensive set of specifications, including those specific to the `DefaultStagnation`, `DefaultReproduction`, `DefaultSpeciesSet`, and `DefaultGenome` classes. By modifying these parameters, users can tailor the evolution process and experiment settings to their requirements.
- **winner.pkl**: As the output of executing the **Main.py** program, this pickle file stores the robust genome of the winning bird that has surpassed the fitness threshold. This file enables users to load and relive the remarkable gaming experience achieved by the evolved artificial intelligence.
- **images/**: This folder houses all the images used in the game, such as three bird images, a background image, a pipe image, and a base floor image. These images together contribute to the game's visual appeal and create an engaging environment.
- **requirements.txt**: This file lists the necessary dependencies and packages required to run the program. It provides a convenient way to install all the dependencies.
- **README.md**: The README file for the project. It provides a comprehensive overview of the project's objectives, functionalities, structure, and usage instructions.
- **LICENSE**: The license file for the project.

<br/>

## **Usage**

1. Install the required dependencies using `pip`:
    
    ```
    pip install -r requirements.txt
    ```
    
2. Run the **Main.py** script to start evolving the population of birds and observe their progress:
    
    ```
    python Main.py
    ```
    
3. The best-performing genome will be saved as **winner.pkl** as the final output. You can load this genome using the  `play_with_best_bird()` method of the `NeatApp` class, as defined in the **Main.py**, to watch the AI-controlled bird play the game, or further fine-tune the evolution process.

<br/>

## **Contribution**

Contributions to this project are welcome! Feel free to open issues or submit pull requests to suggest improvements, fix bugs, or add new features.

<br/>

## **License**

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

<br/>

## **Acknowledgement**

This project was inspired by the ***Flappy Bird*** game and the **NEAT algorithm**. Special thanks to [**Kenneth O. Stanley**](https://scholar.google.se/citations?user=6Q6oO1MAAAAJ&hl=en), the original developer of NEAT algorithm, and the creators of the [**neat-python**](https://github.com/CodeReclaimers/neat-python.git) library, for providing the method and tools to implement this project.

<br/>

**Disclaimer**: This project is for learning and entertainment purpose only. It is not affiliated with the original ***Flappy Bird*** game or its creators.
