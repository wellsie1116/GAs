#!/usr/bin/env python2
#-*- coding:utf-8 -*-

import sys

from random import randint, random
import math

import gobject
import gtk
import cairo

class Genome:
    def __init__(self, width, height):
        self.grid = [[False for x in range(width)] for y in range(height)]
        #self.grid[0][2] = True
        #self.grid[1][2] = True
        #self.grid[2][2] = True
        #self.grid[2][1] = True
        #self.grid[1][0] = True
        self.width = width
        self.height = height
    def randomize(self):
        for x in range(self.width):
            for y in range(self.height):
               self.grid[x][y] = random() < .01
    def breed(self, other):
        def cross(self, other, p1, p2):
            newGenome = Genome(self.width, self.height)
            for x in range(self.width):
                for y in range(self.height):
                    newGenome.grid[x][y] = self.grid[x][y]
            for x in range(p1[0], p2[0]):
                for y in range(p1[1], p2[1]):
                    newGenome.grid[x][y] = other.grid[x][y]
            return newGenome
        def randIndex(size):
            i1, i2 = randint(0, size), randint(0, size)
            if i1 > i2:
                return i2, i1
            return i1, i2
        p1, p2 = zip(randIndex(self.width), randIndex(self.height))
        newGenomes = cross(self, other, p1, p2), cross(other, self, p1, p2)
        for genome in newGenomes:
            genome.mutate()
        return newGenomes
    def mutate(self):
        for x in range(self.width):
            for y in range(self.height):
                if random() < 0.01:
                    self.grid[x][y] = not self.grid[x][y] 

class Board:
    def __init__(self, genome):
        self.grid = [list(row) for row in genome.grid]
        self.width = genome.width
        self.height = genome.height
        self.isAlive = True

    def getCell(self, x, y):
        if x < 0 or x > self.width - 1 or y < 0 or y > self.height - 1:
            return False
        return self.grid[x][y]

    def setCell(self, x, y, val):
        if x < 0 or x > self.width - 1 or y < 0 or y > self.height - 1:
            return
        self.grid[x][y] = val

    def getPopAdjCells(self, x, y):
        cnt = 0
        cnt += self.getCell(x - 1, y - 1)
        cnt += self.getCell(x, y - 1)
        cnt += self.getCell(x + 1, y - 1)
        
        cnt += self.getCell(x - 1, y)
        cnt += self.getCell(x + 1, y)        

        cnt += self.getCell(x - 1, y + 1)
        cnt += self.getCell(x, y + 1)
        cnt += self.getCell(x + 1, y + 1)
        return cnt

    def calcNextGrid(self):
        nextgrid = [[False for x in range(self.width)] for y in range(self.height)]
        for x in range(self.width):
            for y in range(self.height):
                cnt = self.getPopAdjCells(x, y)
                if self.grid[x][y]:
                    nextgrid[x][y] = cnt == 2 or cnt ==3
                else:
                    nextgrid[x][y] = cnt == 3
        return nextgrid
                
    def step(self):
        self.grid = self.calcNextGrid()

    def __hash__(self):
        hashCode = 0
        i = 3
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y]:
                    hashCode += ((x << 8) | (y << 8)) * i
                    i += 2
        return hashCode
        #return hash(tuple([tuple(row) for row in self.grid]))
    
    def __eq__(self, other):
        def cellsEqual():
            for x in range(self.width):
                for y in range(self.height):
                    if self.grid[x][y] != other.grid[x][y]:
                        return False
            return True

        return self.width == other.width and self.height == other.height and cellsEqual()

class Generation:
    def __init__(self, n):
        self.n = n
        self.genomes = []
        self.scores = None
    def randomize(self, count, width, height):
        self.genomes = [Genome(width, height) for i in range(count)]
        for genome in self.genomes:
            genome.randomize()
    def score(self, fitness):
        self.scores = [fitness(genome) for genome in self.genomes]
        #sort by scores (not necessary, but prettier printing)
        arr = list(zip(self.scores, self.genomes))
        arr.sort(key=lambda v: v[0])
        self.scores, self.genomes = list(zip(*arr))
    def generateNext(self):
        #generate a breeding pool, by facing each genome off with a randomly chosen one
        pool = []
        for i1 in range(len(self.genomes)):
            i2 = randint(0, len(self.genomes)-2)
            if i2 >= i1:
                i2 += 1
            pool.append(self.genomes[i1] if self.scores[i1] > self.scores[i2] else self.genomes[i2])

        #randomly pair off genomes from the breeding pool
        def genPairs(count):
            pairs = []
            while len(pairs) < count:
                i1 = randint(0, len(pool)-1)
                i2 = randint(0, len(pool)-2)
                if i2 >= i1:
                    i2 += 1
                pair = pool[i1], pool[i2]
                if pair not in pairs:
                    pairs.append(pair)
            return pairs
        count = int(len(self.genomes)/2)
        if len(self.genomes) % 2 == 1:
            count += 1
        pairs = genPairs(count)

        #breed the pairs
        nextGen = Generation(self.n+1)
        for pair in pairs:
            a, b = pair
            nextGen.genomes.extend(a.breed(b))

        #keep lengths the same (for odd sized generations)
        while len(nextGen.genomes) > len(self.genomes):
            nextGen.genomes.pop(randint(0, len(nextGen.genomes)-1))

        return nextGen

def main():
    import lifegui
    lifegui.main()

if __name__ == '__main__':
    main()


