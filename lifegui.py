#!/usr/bin/python2

from life import *

class BoardView(gtk.DrawingArea):
    __gsignals__ = {"expose-event": "override"}

    def __init__(self, width, height):
        gtk.DrawingArea.__init__(self)
        self.width = width
        self.height = height
        self.grid = None
    
    def do_expose_event(self, event):
        g = self.window.cairo_create()
        g.paint()
        g.set_line_width(1.0)
        
        w, h = self.window.get_size()
        stepx = float(w) / self.width
        stepy = float(h) / self.height

        g.set_antialias(cairo.ANTIALIAS_NONE)

        if self.grid:
            for x in range(self.width):
                for y in range(self.height):
                    val = self.grid.getCell(x, y)
                    if val > 0:
                        if self.grid.isAlive:
                            g.set_source_rgb(0.5, 0.5, 0.5)
                        else:
                            g.set_source_rgb(0.8, 0.2, 0.2)
                        g.rectangle(x * stepx, y * stepy, stepx, stepy)
                        g.fill_preserve()
                        g.stroke()
                      
        if self.grid and not self.grid.isAlive:
            g.set_source_rgb(0.1, 0.1, 0.25)
        else:
            g.set_source_rgb(0.2, 0.2, 0.5)
        
        for x in range(self.width + 1):
            g.move_to((float(x) / self.width) * w, 0)
            g.line_to((float(x) / self.width) * w, h)

        for y in range(self.height + 1):
            g.move_to(0, (float(y) / self.height) * h)
            g.line_to(w, (float(y) / self.height) * h)

        g.stroke()
            

class MainWindow(gtk.Window):

    def __init__(self, rows, cols, width, height):
        gtk.Window.__init__(self)
        self.set_title('Life GA')
        vbox = gtk.VBox()

        self.rows = rows
        self.cols = cols

        self.table = gtk.Table(rows, cols)

        self.views = [[BoardView(width, height) for x in range(cols)] for y in range(rows)]

        for x in range(cols):
            for y in range(rows):
                self.table.attach(self.views[x][y], x, x+1, y, y+1, xpadding=2, ypadding=2)

        vbox.pack_start(self.table, True, True)

        self.add(vbox)
        vbox.show_all()

        self.set_size_request(300, 300)

    def setBoards(self, boards):
        for x in range(self.cols):
            for y in range(self.rows):
                self.views[x][y].grid = boards[y*self.cols + x]
        self.queue_draw()

def main():
    rows = 5
    cols = 5
    count = rows * cols

    width = 16
    height = 16
        
    win = MainWindow(rows, cols, width, height)
    win.connect('destroy', gtk.main_quit)
    win.show()

    gen = Generation(0)
    gen.randomize(count, width, height)

    def testNextGeneration(gen):
        gen = gen.generateNext()
        testGeneration(gen)

    def testGeneration(gen):
        boards = [Board(genome) for genome in gen.genomes]
        genomeToBoard = dict(zip(gen.genomes, boards))

        win.setBoards(boards)

        prevBoards = {}
        for genome in gen.genomes:
            prevBoards[genome] = set()

        def fitness(genome):
            return len(prevBoards[genome])

        def step():
            alive = False
            for genome in gen.genomes:
                board = genomeToBoard[genome]
                if board not in prevBoards[genome]:
                    prevBoards[genome].add(Board(board))
                    board.step()
                    alive = True
                else:
                    board.isAlive = False
            win.queue_draw()
            if not alive:
                gen.score(fitness)
                print("{0:3d}: {1}".format(gen.n, list(reversed(gen.scores))))
                gobject.timeout_add(50, testNextGeneration, gen)
                return 0
            return 1

        gobject.timeout_add(50, step, priority=gobject.PRIORITY_HIGH_IDLE+30)

    testGeneration(gen)

    gtk.main()

if __name__ == '__main__':
    main()

