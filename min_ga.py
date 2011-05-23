#!/usr/bin/python3

from random import randint, random
import math

class Genome:
    def __init__(self):
        self.val = 0
        self.mutateProb = 0.1
    def randomize(self):
        #assign a random 16 bit value
        self.val = randint(0, 1<<16)
    def breed(self, other):
        #cross over by picking two random points and splicing the bits
        i1, i2 = randint(0, 15), randint(0, 15)
        if i1 > i2:
            i1, i2 = i2, i1

        #print("{0} to {1}".format(i1, i2))

        mask2 = (1 << i2-i1)-1 << 16-i2
        mask1 = ~mask2 & ((1 << 16) - 1)
        #print("Mask 1: {0:016b}".format(mask1))
        #print("Mask 2: {0:016b}".format(mask2))
        newVal = self.val & mask1 | other.val & mask2
        new = Genome()
        new.val = newVal

        new.mutate()
        return new
    def mutate(self):
        #iterate over every bit, randomly mutating them
        mask = 0
        for i in range(16):
            if random() < self.mutateProb:
                mask |= 1
            mask <<= 1
        mask >>= 1
        #print("Val:  {0:016b} {0}".format(self.val))
        #print("Mask: {0:016b} {0}".format(mask))
        self.val ^= mask
        #print("Val:  {0:016b} {0}".format(self.val))
    def __str__(self):
        return "{0:016b} {0:5d}".format(self.val)
    def __repr__(self):
        return "Genome({0})".format(self.val)

class Generation():
    def __init__(self, n):
        self.n = n
        self.genomes = []
        self.scores = None
        if n == 0:
            self.randomize()
    def randomize(self):
        self.genomes = [Genome() for i in range(10)]
        for genome in self.genomes:
            genome.randomize()
    def score(self, fitness):
        self.scores = [fitness(genome) for genome in self.genomes]
        #sort by scores
        arr = list(zip(self.scores, self.genomes))
        arr.sort(key=lambda v: v[0])
        self.scores, self.genomes = list(zip(*arr))
    def generateNext(self):
        nextGen = Generation(self.n+1)
        for i in range(5):
            a, b = self.genomes[i:i+2]
            nextGen.genomes.append(a.breed(b))
            nextGen.genomes.append(b.breed(a))
        return nextGen
    def __str__(self):
        return 'Generation {0}\n{1}'.format(
            self.n,
            '\n'.join(['{0} ({1:.4f})'.format(
                        str(genome),
                        score) for genome, score in zip(self.genomes, self.scores)]))

def fitness_cos(genome):
    x = genome.val
    return 0.5*((math.cos((x/65535)*math.pi*7)+1)*(1-x/65535)*.5+(1-x/65535))

def fitness_cos2(genome):
    opp = Genome()
    opp.val = 65535-genome.val
    return (fitness_cos(genome) + fitness_cos(opp))*2-1

def main():
    elite = []
    for iGen in range(10000):
        gen = Generation(0)
        gen.score(fitness_cos2)
        for i in range(100):
            gen = gen.generateNext()
            gen.score(fitness_cos2)
        print(gen.genomes[0])
        elite.append(gen.genomes[0])
    elite.sort(key=lambda genome: genome.val)
    print(elite)
    for genome in elite:
        if genome.val > 20000 and genome.val < 50000:
            print("Found local min: {0}".format(genome))





def main_testGenerations():
    gen = Generation(0)
    gen.score(fitness_cos2)
    print(gen)
    for i in range(100):
        gen = gen.generateNext()
        gen.score(fitness_cos2)
        print(gen)


def main_testGenome():
    a, b = Genome(), Genome()
    a.randomize()
    b.randomize()
    print(a)
    print(b)
    c = a.breed(b)
    print(c)

if __name__ == '__main__':
    main()

