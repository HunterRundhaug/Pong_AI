from pong import PongGame
import pygame
import neat
import os
import pickle


class Pong:
    def __init__(self, width=1000, height=600):
        self.game = PongGame(width, height)
        self.left_paddle = self.game.opponent
        self.right_paddle = self.game.player
        self.ball = self.game.ball

    def ai_vs_ai(self, genome1, genome2, config):
        net = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
        run = True

        while run:

            clock = pygame.time.Clock()
            clock.tick(60)

            self.game.update() # update method call methods like draw and move ball

            #keys = pygame.key.get_pressed()

            # Move Player 1
            '''
            if keys[pygame.K_UP] == True:
                self.game.move_player_1(1)
            elif keys[pygame.K_DOWN] == True:
                self.game.move_player_1(-1)
            '''

            #Player 2 [AI]
            output = net.activate((self.left_paddle.y, self.ball.y, abs(self.left_paddle.x - self.ball.x)))
            decision = output.index(max(output)) # Gives Index
            if decision == 0:
                pass
            elif decision == 1:
                self.game.move_player_2(1)
            else:
                self.game.move_player_2(-1)

            #Player 1 [AI]
            output2 = net.activate((self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))
            decision2 = output2.index(max(output2)) # Gives Index
            if decision2 == 0:
                pass
            elif decision2 == 1:
                self.game.move_player_1(1)
            else:
                self.game.move_player_1(-1)

            '''
            # Move Player 2
            if keys[pygame.K_LEFT] == True:
                self.game.move_player_1(-1)
            elif keys[pygame.K_RIGHT] == True:
                self.game.move_player_1(1)
            '''

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

        pygame.quit() # Quit Game after While loop

    def test_ai(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        run = True

        while run:

            clock = pygame.time.Clock()
            clock.tick(60)

            self.game.update() # update method call methods like draw and move ball

            keys = pygame.key.get_pressed()

            # Move Player 1
            if keys[pygame.K_UP] == True:
                self.game.move_player_1(1)
            elif keys[pygame.K_DOWN] == True:
                self.game.move_player_1(-1)
            

            #Player 2 [AI]
            output = net.activate((self.left_paddle.y, self.ball.y, abs(self.left_paddle.x - self.ball.x)))
            decision = output.index(max(output)) # Gives Index
            if decision == 0:
                pass
            elif decision == 1:
                self.game.move_player_2(1)
            else:
                self.game.move_player_2(-1)

            '''
            # Move Player 2
            if keys[pygame.K_LEFT] == True:
                self.game.move_player_1(-1)
            elif keys[pygame.K_RIGHT] == True:
                self.game.move_player_1(1)
            '''

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

        pygame.quit() # Quit Game after While loop

    # END OF Test Ai Method ---------------------

    def train_ai(self, genome1, genome2, config):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            #Player 2
            output1 = net1.activate((self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))
            decision1 = output1.index(max(output1)) # Gives Index
            if decision1 == 0:
                genome1.fitness -= 1
                pass
            elif decision1 == 1:
                move = self.game.move_player_1(1)
                if move == False:
                    genome1.fitness -= 1
            else:
                move = self.game.move_player_1(-1)
                if move == False:
                    genome1.fitness -= 1
            
            #Player 1
            output2 = net2.activate((self.left_paddle.y, self.ball.y, abs(self.left_paddle.x - self.ball.x)))
            decision2 = output2.index(max(output2)) # Gives Index
            if decision2 == 0:
                genome2.fitness -= 1
                pass
            elif decision2 == 1:
                move = self.game.move_player_2(1)
                if move == False:
                    genome2.fitness -= 1
            else:
                move = self.game.move_player_2(-1)
                if move == False:
                    genome2.fitness -= 1

            print(output1, output2)

            self.game.update_train_mode()
            
            if self.game.p1_miss >= 1 or self.game.p2_miss >= 1 or self.game.p1_hits > 50: #Stops singular game after criteria met
                self.calculate_fitness(genome1, genome2)
                break
    
    def calculate_fitness(self, genome1, genome2):
        genome1.fitness += self.game.p1_hits * 10
        genome2.fitness += self.game.p2_hits * 10

       


def eval_genomes(genomes, config):
    
    for i, (genome_id1, genome1) in enumerate(genomes): # Every genome plays against every other genome.
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            game = Pong()
            game.train_ai(genome1, genome2, config)

def run_neat(config):
    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-17')   #--used if starting at a checkpoint
    #p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True)) # Shows data gathered from training
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(2)) # Saves Every Generation of neural network

    winner = p.run(eval_genomes, 10) 

    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

def test_ai(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    
    game = Pong()
    game.test_ai(winner, config)

def ai_vs_ai(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    
    game = Pong()
    game.ai_vs_ai(winner, winner, config)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    #run_neat(config)
    test_ai(config)
    #ai_vs_ai(config)



