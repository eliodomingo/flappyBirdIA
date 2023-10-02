import pygame
import neat
import time
import os
import random
pygame.font.init()

from bird import Bird
from pipe import Pipe
from base import Base

# Taille écran
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 800

# Nombre de générations
GENERATIONS = 0

pygame.display.set_caption("Flappy Bird")

# Importer background image
BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(
    os.path.join("images", "bg.png")
))

# Affichage font
STAT_FONT = pygame.font.SysFont("georgia", 50)

# Dessiner l'ensemble de nos objets
def draw_window(window, birds, pipes, base, score, generations):
    window.blit(BACKGROUND_IMAGE, (0, 0))

    for pipe in pipes:
        pipe.draw(window)

    text = STAT_FONT.render("Score : " + str(score), 1, (255, 255, 255))
    window.blit(text, (WINDOW_WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT.render("Gen : " + str(generations), 1, (255, 255, 255))
    window.blit(text, (10, 10))

    base.draw(window)

    for bird in birds:
        bird.draw(window)

    pygame.display.update()



def main(genomes, config):
    global GENERATIONS
    GENERATIONS += 1

    nets = []
    ge = []
    birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    base = Base(730)
    pipes = [Pipe(600)]
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    
    score = 0

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()

        add_pipe = False
        remove = []

        for pipe in pipes:
            for x, bird in enumerate(birds):   
                # Collision
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                # L'oiseau a passé un tuyau
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            # Tuyau sort complétement de l'image, on doit le supprimer
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                remove.append(pipe)

            pipe.move()

        # On ajoute un nv tuyau dès que l'oiseau a passé un tuyau
        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600))

        # Supprimer les tuyaux à supprimer
        for r in remove:
            pipes.remove(r)

        for x, bird in enumerate(birds):
            # On touche le sol
            if bird.y + bird.image.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        base.move()
        draw_window(window, birds, pipes, base, score, GENERATIONS)


def run(config_path):
    # Charger la configauration NEAT
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)
    # Créer la population
    population = neat.Population(config)

    # Afficher des informations sur ce qui se passe
    # avec la population
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # Gestion de la fonction fitness et du nombre de fois qu'on
    # l'a fait passer
    winner = population.run(main, 50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)